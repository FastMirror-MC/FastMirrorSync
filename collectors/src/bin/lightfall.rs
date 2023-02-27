use collectors::api::github::builder;
use anyhow::Result;
use libcollector::Collector;

const PROJECT_NAME: &str = "lightfall";

fn main() -> Result<()> {
    let github = builder("ArclightPowered/lightfall");

    Collector::new(PROJECT_NAME)?.run(github.build()?)
}