use serde::Deserialize;

use crate::{manifest::Manifest, Collector, fastmirror::api::{get_data_from_response, ApiResponse}, datetime::{ISO8601, self}};
use anyhow::Result;


#[derive(Deserialize, Debug)]
pub(crate) struct SummaryBody {
    pub builds: Vec<Metadata>
}
#[derive(Hash, Eq, Deserialize, Debug, Clone)]
pub(crate) struct Metadata {
    name: String,
    mc_version: String,
    core_version: String,
    sha1: String,
    update_time: String,
}
impl PartialEq for Metadata {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name && self.mc_version == other.mc_version
    }
}

impl Collector {
    fn fetch(&mut self, mc_version: &String) -> Result<()> {
        let url = format!("{}/api/v3/{}/{mc_version}?limit=25", &self.remote_host, &self.project_name);
        println!("update {}-{mc_version} from {url}", self.project_name);

        get_data_from_response(
                self.client.get(url)
                .basic_auth(&self.username, Some(&self.password))
                .send()?
                .json::<ApiResponse<SummaryBody>>()?
            )?
            .builds
            .into_iter()
            .for_each(|i| { self.records.insert(i); });
        
        Ok(())
    }

    pub(crate) fn up_to_date(&mut self, manifest: & Manifest) -> Result<bool> {
        let mc_version = manifest.mc_version();
        let core_version = manifest.core_version();

        let any = self.records.iter().any(|i| &i.mc_version == mc_version);
        if !any { self.fetch(mc_version)?; }
        // println!("{:?}", self.records);
        
        let item = self.records.iter()
            .find(|item| &item.mc_version == mc_version && &item.core_version == core_version);

        if let Some(record) = item {
            let update_time = datetime::parse(&record.update_time, ISO8601)?;
            
            let time_equals = datetime::compare(&update_time, &manifest.update_time());
            
            if let Some(signature) = manifest.sha1() {
                return Ok(&record.sha1 == signature && time_equals);
            } else {
                return Ok(time_equals);
            }
        }
        
        Ok(false)
    }

    pub(crate) fn append_record(&mut self, manifest: &Manifest) -> Result<()> {
        let metadata = Metadata {
            name: manifest.name().to_string(),
            mc_version: manifest.mc_version().to_string(),
            core_version: manifest.core_version().to_string(),
            sha1: manifest.sha1().unwrap_or(&"".to_string()).to_string(),
            update_time: manifest.update_time().format(ISO8601)?
        };
        self.records.insert(metadata);
        Ok(())
    }
}
