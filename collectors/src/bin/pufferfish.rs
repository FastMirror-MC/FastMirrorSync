use anyhow::Result;
use collectors::api::jenkins::builder;
use libcollector::Collector;

const PROJECT_NAME: &str = "Pufferfish";

fn main() -> Result<()> {
    let jenkins = builder("https://ci.pufferfish.host")
        .append_job("Pufferfish-1.18")
        .append_job("Pufferfish-1.19")
        // .version_selector(|job: &'static str, api: &Api, _: &Asset| {
        //     let mc_version = match job {
        //         "Pufferfish-1.18" => "1.18.2",
        //         "Pufferfish-1.19" => "1.19.4",
        //         _ => return Err(anyhow::Error::msg(format!("unknown job name `{job}`")))
        //     };
        //     Ok((mc_version.to_string(), api.number.as_core_version()))
        // })
        ;
    
    Collector::new(PROJECT_NAME)?.run(jenkins.build()?)
}
