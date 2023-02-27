use collectors::api::sponge::builder;
use libcollector::Collector;
use anyhow::Result;

const PROJECT_NAME: &str = "SpongeVanilla";

fn main() -> Result<()> {
    let sponge = builder(PROJECT_NAME, 10)?;

    Collector::new(PROJECT_NAME)?.run(sponge.build()?)
}