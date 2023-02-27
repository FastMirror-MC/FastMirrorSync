use libcollector::Collector;
use collectors::api::github::builder;

use anyhow::{Result, Ok};

const PROJECT_NAME: &str = "PocketMine";

fn main() -> Result<()> {
    let github = builder("pmmp/PocketMine-MP")
        .version_selector(|api| { Ok(
            ("general".to_string(), api.tag_name.to_string())
        ) });
    
    Collector::new(PROJECT_NAME)?.run(github.build()?)
}
