use anyhow::Result;
use collectors::api::jenkins::{builder, AsCoreVersion};
use libcollector::Collector;

const PROJECT_NAME: &str = "NukkitX";

fn main() -> Result<()> {
    let jenkins = builder("https://ci.opencollab.dev/job/NukkitX/job/Nukkit")
        .append_job("master")
        .version_selector(|_, api, _| { Ok(("general".to_string(), api.number.as_core_version())) });
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
