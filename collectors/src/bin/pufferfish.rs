use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "Pufferfish";

fn main() -> Result<()> {
    let jenkins = builder("https://ci.pufferfish.host")
        .append_job("Pufferfish-1.18");
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
