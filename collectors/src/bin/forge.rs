use anyhow::Result;
use libcollector::{http::client, manifest::Manifest, datetime::{self, ISO8601}, Collector, utils::split_once};
use roxmltree::{Document, ExpandedName};

const PROJECT_NAME: &str = "Forge";

fn get_node_str<'s>(doc: &'s Document, tag_name: &str) -> Result<&'s str> {
    Ok(doc.descendants()
        .find(|node| { node.tag_name() == tag_name.into() })
        .expect(format!("`{tag_name}` not found.").as_str())
        .first_child().unwrap()
        .text().unwrap())
}

fn convert_datetime<'t>(time: &'t str) -> String {
    let (year, month, day, hour, minute, second) = (
        &time[0..4], 
        &time[4..6], 
        &time[6..8], 
        &time[8..10], 
        &time[10..12], 
        &time[12..]
    );
    
    format!("{year}-{month}-{day}T{hour}:{minute}:{second}Z")
}

fn get_artifact(version: &str, mc_version: &str, core_version: &str, update_time: &String) -> Result<Manifest> {
    let download_url = format!("https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar");
    let update_time = &convert_datetime(&update_time);
    Ok(Manifest::new()
        .set_mc_version(mc_version.to_string())
        .set_core_version(core_version.to_string())
        .set_update_time(datetime::parse(update_time, ISO8601)?)
        .set_download_url(download_url))

}

fn full_dump(take: i32, minimum_mc_version: &str) -> Result<impl Iterator<Item = Manifest>> {
    let client = client();
    let text = client.get("https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml")
        .send()?
        .text()?;
    let doc = Document::parse(text.as_str())?;

    let tag_name: ExpandedName = "version".into();
    let versions = doc.descendants()
        .filter(|node| { node.tag_name() == tag_name });

    let mut list: Vec<Manifest> = Vec::new();
    let mut prev_version = "";
    let mut counter = 0;
    for node in versions {
        let version = node.first_child().expect("expect format.").text().unwrap();
        let (mc_version, core_version) = split_once(version, "-")?;
        
        if minimum_mc_version == mc_version { break; }
        if prev_version == mc_version && counter >= take { continue; }
        if prev_version != mc_version { prev_version = mc_version; counter = 0; }

        counter += 1;
        
        let update_time = {
            let xml = client
                .get(format!("https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/maven-metadata.xml"))
                .send()?
                .text()?;

            let doc = Document::parse(xml.as_str())?;
            get_node_str(&doc, "lastUpdated")?.to_string()
        };

        let artifact = get_artifact(version, mc_version, core_version, &update_time)?;

        list.push(artifact);
    }

    Ok(list.into_iter())
}

fn get_latest() -> Result<impl Iterator<Item = Manifest>> {
    let client = client();
    let text = client.get("https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml")
        .send()?
        .text()?;
    let doc = Document::parse(text.as_str())?;
    let version = get_node_str(&doc, "latest")?;
    let update_time = get_node_str(&doc, "lastUpdated")?;
    let (mc_version, core_version) = split_once(version, "-")?;

    let artifact = get_artifact(version, mc_version, core_version, &update_time.to_string())?;

    Ok(vec![artifact].into_iter())
}

fn main() -> Result<()> {
    let forge = full_dump(10, "1.7.10")?;

    Collector::new(PROJECT_NAME)?.run(forge)
}