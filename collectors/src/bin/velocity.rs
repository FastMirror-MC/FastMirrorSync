use anyhow::Result;
use collectors::api::papermc::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "Velocity";

fn main() -> Result<()> {
    let papermc = builder(PROJECT_NAME)?;

    Collector::new(PROJECT_NAME)?.run(papermc.build()?)
}