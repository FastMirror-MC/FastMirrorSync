use serde::Deserialize;
use anyhow::{Result, Error};

use libcollector::{manifest::Manifest, http::client, datetime::{self, ISO8601}, utils::split_once};

// struct define
#[derive(Deserialize, Debug)]
pub struct Api {
    pub tag_name: String,
    pub name: String,
    pub prerelease: bool,
    pub published_at: String,
    pub assets: Vec<Asset>,
}

#[derive(Deserialize, Debug, Clone)]
pub struct Asset {
    pub name: String,
    pub content_type: String,
    pub browser_download_url: String
}

pub struct Builder {
    repo: String,
    filetype: String,
    get_version: fn(&Api) -> Result<(String, String)>,
    select_asset: fn(&Api) -> Result<Asset>
}
// struct definde end

impl Builder {
    pub fn filetype(mut self, filetype: &str) -> Self { self.filetype = filetype.to_string(); self }
    pub fn version_selector(mut self, f: fn(&Api) -> Result<(String, String)>) -> Self { self.get_version = f; self }
    pub fn asset_selector(mut self, f: fn(& Api) -> Result<Asset>) -> Self { self.select_asset = f; self }

    pub fn build(self) -> Result<impl Iterator<Item = Manifest>> {
        let client = client();
        let url = format!("https://api.github.com/repos/{}/releases", self.repo);

        println!("try download release list from {url}");
        let releases = client.get(url).send()?
            .json::<Vec<Api>>()?;
        println!("download successful.");

        let mut result = Vec::new();

        for release in releases {
            let asset = (self.select_asset)(&release)?;
            let (mc_version, core_version) = (self.get_version)(&release)?;
            let update_time = datetime::parse(&release.published_at, ISO8601)?;

            let artifact = Manifest::new()
                .set_mc_version(mc_version)
                .set_core_version(core_version)
                .set_update_time(update_time)
                .set_filetype(self.filetype.to_string())
                .set_download_url(asset.browser_download_url);
            result.push(artifact);
        }
        Ok(result.into_iter())
    }
}

fn default_get_version(api: &Api) -> Result<(String, String)> {
    let binding = api.tag_name.to_string();
    let split = split_once(&binding, "-")?;
    Ok((split.0.to_owned(), split.1.to_owned()))
}

fn default_select_asset(body: &Api) -> Result<Asset> {
    Ok(body.assets.first().ok_or(Error::msg("assets is empty."))?.to_owned())
}

pub fn builder(repo: &str) -> Builder { Builder { 
    repo: repo.to_string(),
    filetype: "jar".to_string(),
    get_version: default_get_version,
    select_asset: default_select_asset
} }