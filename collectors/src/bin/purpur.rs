use libcollector::{http::client, manifest::Manifest, datetime, Collector};
use serde::Deserialize;
use anyhow::Result;

#[derive(Deserialize, Debug)]
struct Project { versions: Vec<String> }
#[derive(Deserialize, Debug)]
struct Version {
    builds: Builds
}
#[derive(Deserialize, Debug)]
struct Builds {
    all: Vec<String>
}
#[derive(Deserialize, Debug)]
struct Record {
    timestamp: i64,
    result: String
}

const PROJECT_NAME: &str = "Purpur";
const HOST: &str = "https://api.purpurmc.org/v2/purpur";

fn walk_mc_version(mc_version: &String, result: &mut Vec<Manifest>) -> Result<()> {
    let client = client();

    let url = &format!("{HOST}/{mc_version}");
    
    let builds = client.get(url).send()?
        .json::<Version>()?.builds.all;

    for build in builds {
        let record = client.get(format!("{HOST}/{mc_version}/{build}"))
            .send()?
            .json::<Record>()?;

        if record.result != "SUCCESS" { continue; }

        let artifact = Manifest::new()
            .set_mc_version(mc_version.to_string())
            .set_core_version(format!("build{build}"))
            .set_update_time(datetime::from_timestamp(record.timestamp)?)
            .set_download_url(format!("{HOST}/{mc_version}/{build}/download"));

        result.push(artifact);
    }    

    Ok(())
}

fn main() -> Result<()> {
    let client = client();
    let url = &HOST.to_string();

    let versions = client.get(url).send()?
        .json::<Project>()?.versions;

    let mut result: Vec<Manifest> = Vec::new();
    for mc_version in versions {
        walk_mc_version(&mc_version, &mut result)?;
    }

    Collector::new(PROJECT_NAME)?.run(result.into_iter())
}