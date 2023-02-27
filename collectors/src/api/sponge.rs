use std::collections::HashMap;

use anyhow::Result;
use libcollector::{http::client, manifest::Manifest, datetime};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct Response1 { tags: HashMap<String, Vec<String>> }

#[derive(Deserialize, Debug)]

struct Response2 { artifacts: HashMap<String, ResponseArtifact> }
#[derive(Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct ResponseArtifact { tag_values: TagValue }

#[derive(Deserialize, Debug)]
struct TagValue { minecraft: String }

#[derive(Deserialize, Debug)]
struct Asset { assets: Vec<HashMap<String, String>> }

pub struct Builder {
    project_name: String,
    take: u32
}
const HOST: &str = "https://dl-api-new.spongepowered.org/api/v2/groups/org.spongepowered/artifacts";

impl Builder {
    fn walk_mc_version(
        &self, host: &String, 
        mc_version: &String, 
        result: &mut Vec<Manifest>
    ) -> Result<()> {
        let client = client();
        let url = format!("{host}/versions?tags=minecraft:{mc_version}&offset=0&limit={}", self.take * 2);
        let builds = client.get(url).send()?
            .json::<Response2>()?.artifacts;

        let mut counter = 0;

        for (version, tag_value) in builds {
            if counter >= self.take { break; }
            let tag_value = tag_value.tag_values;

            if &tag_value.minecraft != mc_version { continue; }

            let url = &format!("{host}/versions/{version}");
            let assets = client.get(url).send()?
                .json::<Asset>()?.assets;
            
            let (download_url, sha1) = {
                let asset = assets.iter().find(|map| {
                    map.get("classifier").unwrap() == "universal"
                });
                if let Some(map) = asset {
                    (map.get("downloadUrl").unwrap(), map.get("sha1").unwrap())
                } else { continue; }
            };

            let core_version = &version[mc_version.len() + 1..];

            let artifact = Manifest::new()
                .set_name(self.project_name.to_string())
                .set_mc_version(mc_version.to_string())
                .set_core_version(core_version.to_string())
                .set_update_time(datetime::now())
                .set_sha1(sha1.to_string())
                .set_download_url(download_url.to_string());

            result.push(artifact);
            counter += 1;
        }
        Ok(())
    }
    
    pub fn build(self) -> Result<impl Iterator<Item = Manifest>> {
        let client = client();

        let url = &format!("{HOST}/{}", self.project_name.to_lowercase());
        println!("{}", url);
        let tags = client.get(url).send()?
            .json::<Response1>()?.tags;
        let mc_versions = tags.get("minecraft")
            .ok_or(anyhow::Error::msg("invalid response."))?;

        let mut result: Vec<Manifest> = Vec::new();
        for mc_version in mc_versions { 
            self.walk_mc_version(url, mc_version, &mut result)?; 
        }

        Ok(result.into_iter())
    }
}

pub fn builder(project_name: &str, take: u32) -> Result<Builder> { Ok(Builder { 
    project_name: project_name.to_string(),
    take
 }) }
