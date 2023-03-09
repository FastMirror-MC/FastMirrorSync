use libcollector::{Collector, utils::split_once};
use collectors::api::github::builder;

use anyhow::Result;

const PROJECT_NAME: &str = "Arclight";

fn main() -> Result<()> {
    let github = builder("IzzelAliz/Arclight")
        .version_selector(|api| {
            let binding = api.tag_name.to_string();
            let (mc, core) = split_once(&binding, "/")?;
            match mc.to_lowercase().as_str() {
                "greathorn" => return Ok(("1.19.3".to_string(), core.to_owned())),
                // "horn"      => return Ok(("1.19".to_string(), core.to_owned())),
                _           => return Ok((mc.to_owned(), core.to_owned()))
            }
        });
    
    Collector::new(PROJECT_NAME)?.run(github.build()?)
}
