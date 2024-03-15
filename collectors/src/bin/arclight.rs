use libcollector::{Collector, utils::split_once};
use collectors::api::github::builder;

use anyhow::Result;
use anyhow::anyhow;

const PROJECT_NAME: &str = "Arclight";

fn main() -> Result<()> {
    let github = builder("IzzelAliz/Arclight")
    .version_selector(|api| {
        let binding = api.tag_name.to_string();
        let (mc, core) = split_once(&binding, "/")?;
        return Ok((mc.to_owned(), format!("{}-{}", "forge", core)));
    })
    .asset_selector(|api| {
        api.assets.iter().find(|o| o.name["arclight-".len()..].starts_with("forge")).ok_or(anyhow!("")).cloned()
    });

    if let Err(err) = Collector::new(PROJECT_NAME)?.run(github.build()?) {
        println!("{}", err);
    }
    
    let github = builder("IzzelAliz/Arclight")
    .version_selector(|api| {
        let binding = api.tag_name.to_string();
        let (mc, core) = split_once(&binding, "/")?;
        return Ok((mc.to_owned(), format!("{}-{}", "fabric", core)));
    })
    .asset_selector(|api| {
        api.assets.iter().find(|o| o.name["arclight-".len()..].starts_with("fabric")).ok_or(anyhow!("")).cloned()
    });

    if let Err(err) = Collector::new(PROJECT_NAME)?.run(github.build()?) {
        println!("{}", err);
    }

    let github = builder("IzzelAliz/Arclight")
    .version_selector(|api| {
        let binding = api.tag_name.to_string();
        let (mc, core) = split_once(&binding, "/")?;
        return Ok((mc.to_owned(), format!("{}-{}", "neoforge", core)));
    })
    .asset_selector(|api| {
        api.assets.iter().find(|o| o.name["arclight-".len()..].starts_with("neoforge")).ok_or(anyhow!("")).cloned()
    });

    if let Err(err) = Collector::new(PROJECT_NAME)?.run(github.build()?) {
        println!("{}", err);
    }
    Ok(())
}
