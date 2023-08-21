use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "Mohist";

fn main() -> Result<()> {
    let jenkins = builder("https://ci.codemc.io/job/MohistMC")
        .append_job("Mohist-1.12.2")
        .append_job("Mohist-1.16.5")
        .append_job("Mohist-1.18.2")
        .append_job("Mohist-1.19.2")
        .append_job("Mohist-1.19.4")
        .append_job("Mohist-1.20.1")
        ;
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
