use anyhow::{Result, Error};
use collectors::api::jenkins::{builder, AsCoreVersion};
use libcollector::Collector;

const PROJECT_NAME: &str = "BungeeCord";

fn main() -> Result<()> {
    let jenkins = builder("https://ci.md-5.net")
        .append_job("BungeeCord")
        .version_selector(|_, api, _| { Ok(("general".to_string(), api.number.as_core_version())) })
        .asset_selector(|api| { Ok(
            api.artifacts.iter()
                .find(|a| { a.file_name.to_lowercase() == "bungeecord.jar" })
                .ok_or(Error::msg("asset not found."))?
                .to_owned()
        ) });
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
