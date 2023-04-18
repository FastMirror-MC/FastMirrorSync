use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "CatServer";
fn main() -> Result<()> {
    let jenkins = builder("https://jenkins.rbqcloud.cn:30011")
        .append_job("CatServer-1.12.2")
        .append_job("CatServer-1.16.5")
        .append_job("CatServer-1.18.2")
        // .asset_selector(|api| { Ok(api.artifacts.iter()
        //     .find(|asset| { asset.file_name.contains("server") })
        //     .ok_or(Error::msg("asset not found."))?
        //     .to_owned()
        // ) })
        ;
        
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}