use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::{Collector, utils::split_once};

const PROJECT_NAME: &str = "Spigot";

fn main() -> Result<()> {
    let jenkins = builder("http://localhost:14514")
        .append_job("makefile")
        .version_selector(|_, api, _| { 
            let (mc_version, core_version) = split_once(&api.display_name, "-")?;
            Ok((mc_version.to_string(), core_version.to_string()))
        });

    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}