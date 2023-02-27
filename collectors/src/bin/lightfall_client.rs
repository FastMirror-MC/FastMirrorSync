use collectors::api::github::builder;
use anyhow::Result;
use libcollector::Collector;

const PROJECT_NAME: &str = "lightfall-client";

fn main() -> Result<()> {
    let github = builder("ArclightPowered/lightfall-client");

    Collector::new(PROJECT_NAME)?.run(github.build()?)
}