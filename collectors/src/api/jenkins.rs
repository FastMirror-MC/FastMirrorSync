use serde::Deserialize;
use anyhow::{Result, Error, Ok};

use libcollector::{manifest::Manifest, http::client, datetime::from_timestamp, utils::split_once};

//这里可以限制数量
const QUERY_STRING: &'static str = "tree=allBuilds[number,displayName,result,building,timestamp,artifacts[*]]{,20}";

// struct define
#[derive(Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct Modules {
    all_builds: Vec<Api>
}

#[derive(Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Api {
    pub artifacts: Vec<Asset>,
    pub building: bool,
    pub number: i32,
    pub display_name: String,
    pub result: String,
    pub timestamp: i64
}

#[derive(Deserialize, Debug, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Asset {
    pub display_path: String,
    pub file_name: String,
    pub relative_path: String
}

pub struct Builder {
    host: String,
    filetype: String,
    jobs: Vec<&'static str>,
    get_version: fn(&'static str, &Api, &Asset) -> Result<(String, String)>,
    select_asset: fn(&Api) -> Result<Asset>
}
// struct definde end

pub trait AsCoreVersion {
    fn as_core_version(&self) -> String;
}

impl AsCoreVersion for i32 {
    fn as_core_version(&self) -> String { format!("build{self}") }
}

impl AsCoreVersion for u32 {
    fn as_core_version(&self) -> String { format!("build{self}") }
}

impl Builder {
    pub fn append_job(mut self, job_name: &'static str) -> Self {
        self.jobs.push(job_name);
        self
    }
    pub fn filetype(mut self, filetype: &str) -> Self { self.filetype = filetype.to_string(); self }

    pub fn version_selector(mut self, f: fn(&'static str, &Api, &Asset) -> Result<(String, String)>) -> Self { self.get_version = f; self }
    pub fn asset_selector(mut self, f: fn(& Api) -> Result<Asset>) -> Self { self.select_asset = f; self }

    pub fn build(self) -> Result<impl Iterator<Item = Manifest>> {
        let mut result: Vec<Manifest> = Vec::new();

        for job_name in self.jobs {

            let client = client();
            let url = format!("{}/job/{job_name}", self.host);
            let list_url = format!("{url}/api/json?{QUERY_STRING}");
            println!("try download release list from {list_url}");

            let releases = client.get(list_url).send()?
                .json::<Modules>()?.all_builds;
            println!("download successful.");
            
            for api in releases {

                let asset = (self.select_asset)(&api)?;
                let (mc_version, core_version) = (self.get_version)(&job_name, &api, &asset)?;
                let timestamp = api.timestamp;

                let metadata = Manifest::new()
                    .set_mc_version(mc_version.to_string())
                    .set_core_version(core_version)
                    .set_filetype(self.filetype.to_string())
                    .set_update_time(from_timestamp(timestamp / 1000)?)
                    .set_download_url(format!("{url}/{}/artifact/{}", api.number, asset.relative_path));

                result.push(metadata);
            }
        }
        
        Ok(result.into_iter())
    }
}

pub fn builder(host: &str) -> Builder { Builder { 
    host: host.to_string(), 
    filetype: "jar".to_string(), 
    jobs: Vec::new(), 
    get_version: default_get_core_version, 
    select_asset: default_get_asset 
} }

fn default_get_core_version(job: &'static str, api: &Api, _: &Asset) -> Result<(String, String)> {
    let mc_version = split_once(job, "-")
        .or(split_once(job, "/"))?.1;
    Ok((mc_version.to_string(), api.number.as_core_version()))
}
fn default_get_asset(api: &Api) -> Result<Asset> { Ok(
api.artifacts
    .first()
    .ok_or(Error::msg("assets not found."))?
    .to_owned()
)}