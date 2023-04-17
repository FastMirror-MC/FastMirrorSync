use std::collections::HashMap;

use anyhow::{Result, Error};

use libcollector::{http::client, manifest::Manifest, datetime::{self, ISO8601}};
use serde::Deserialize;

// struct define
#[derive(Deserialize, Debug)]
struct ApiResponse<T> {
    #[serde(flatten)]
    body: T
}

#[derive(Deserialize, Debug)]
struct McVersions { versions: Vec<String> }
#[derive(Deserialize, Debug)]
struct Builds { builds: Vec<i32> }

#[derive(Deserialize, Debug)]
struct Downloads {
    time: String,
    downloads: HashMap<String, Application>
}
#[derive(Deserialize, Debug)]
struct Application { name: String }

pub struct Builder {
    project_name: String,
    take: usize
}

impl Builder {
    pub fn take(mut self, take: i32) -> Self { self.take = take as usize; self }

    fn walk_build(&self, url: &String, mc_version: &String, build: i32, result: &mut Vec<Manifest>) -> Result<()> {
        let client = client();
        
        let __url__ = format!("{url}/versions/{}/builds/{build}", mc_version);
        let core_version = format!("build{build}");

        let res = client.get(__url__)
            .send()?
            .json::<ApiResponse<Downloads>>()?
            .body;
        let update_time = datetime::parse(&res.time, ISO8601)?;

        let record = res.downloads
            .get("application")
            .ok_or(Error::msg("field `application` not found."))?;
        
        let artifact = Manifest::new()
            .set_name(self.project_name.to_string())
            .set_mc_version(mc_version.to_string())
            .set_core_version(core_version)
            .set_filetype("jar".to_string())
            .set_update_time(update_time)
            .set_download_url(format!("{url}/versions/{mc_version}/builds/{build}/downloads/{}", record.name));

        result.push(artifact);
        Ok(())
    }

    fn walk_mc_version(&self, url: &String, mc_version: &String, result: &mut Vec<Manifest>) -> Result<()> {
        let client = client();
        
        let builds = {
            let __url__ = format!("{url}/versions/{mc_version}");
            println!("try download release list of {mc_version} from {__url__}");
            let builds = client.get(__url__)
                .send()?
                .json::<ApiResponse<Builds>>()?.body.builds;
            let take_from = if builds.len() <= self.take { 0 } else { builds.len() - self.take };
            builds[take_from..].to_vec()
        };
        
        for build in builds {
            self.walk_build(url, mc_version, build, result)?;
        }

        Ok(())
    }

    pub fn build(self) -> Result<impl Iterator<Item = Manifest>> {
        let client = client();
        let url = &format!("https://papermc.io/api/v2/projects/{}", self.project_name.to_lowercase());
        
        let mc_versions = client.get(url).send()?
            .json::<ApiResponse<McVersions>>()?.body.versions;
        
        let mut result: Vec<Manifest> = Vec::new();

        for mc_version in mc_versions {
            self.walk_mc_version(url, &mc_version, &mut result)?;
        }

        Ok(result.into_iter())
    }
}

pub fn builder(project_name: &str) -> Result<Builder> { Ok(Builder { 
    project_name: project_name.to_string(),
    take: 10
}) }
