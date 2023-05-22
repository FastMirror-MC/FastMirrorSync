use anyhow::Result;
use libcollector::{http::client, manifest::Manifest, datetime::{self, ISO8601}, Collector};
use serde::Deserialize;


#[derive(Deserialize, Debug)]
struct VanillaManifests { versions: Vec<VanillaManifest> }
#[derive(Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct VanillaManifest {
    id: String,
    #[serde(alias = "type")]
    manifest_type: String,
    url: String,
    release_time: String
}
#[derive(Deserialize, Debug)]
struct VanillaMetadatas { downloads: Downloads }
#[derive(Deserialize, Debug)]
struct Downloads { server: VanillaMetadata }
#[derive(Deserialize, Debug)]
struct VanillaMetadata { sha1: String, url: String }

const PROJECT_NAME: &str = "Vanilla";

fn main() -> Result<()> {
    let client = client();
    let manifsets = client.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
        .send()?
        .json::<VanillaManifests>()?.versions;
    let mut result: Vec<Manifest> = Vec::new();
    for v_manifest in manifsets {
        let v_meta = client.get(v_manifest.url).send()?
            .json::<VanillaMetadatas>()?.downloads.server;
        let core_version = format!("{}-{}", v_manifest.id, &v_meta.sha1[..6]);

        let artifact = Manifest::new()
            .set_mc_version(v_manifest.manifest_type)
            .set_core_version(core_version)
            .set_update_time(datetime::parse(&v_manifest.release_time, ISO8601)?)
            .set_sha1(v_meta.sha1)
            .set_download_url(v_meta.url);

        result.push(artifact);
    }

    Collector::new(PROJECT_NAME)?.run(result.into_iter())
}