use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "Mirai";
fn main() -> Result<()> {
    let jenkins = builder("https://ci.codemc.io/job/etil2jz")
        .append_job("Mirai-1.19");
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
