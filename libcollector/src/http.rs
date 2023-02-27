use std::time::Duration;
use anyhow::Result;

use lazy_static::lazy_static;
use reqwest::blocking::Client;

pub type HttpClient = &'static Client;

fn build() -> Result<Client> {
    Ok(Client::builder()
    .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50")
    .cookie_store(true)
    .gzip(true)
    .deflate(true)
    .referer(true)
    .timeout(Duration::from_secs(360))
    .tcp_keepalive(Duration::from_secs(360))
    .build()?)
}

lazy_static! {
    static ref CLIENT: Result<Client> = build();
}

pub fn client() -> HttpClient { CLIENT.as_ref().unwrap() }
