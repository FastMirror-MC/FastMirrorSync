use std::{env, collections::HashSet};
use anyhow::{Result, Error};

use manifest::Manifest;
use bytes::Bytes;
use checker::Metadata;
use http::{client, HttpClient};
use sha1_smol::Sha1;
use utils::split_once;

use crate::datetime::ISO8601;

pub mod http;
pub mod manifest;
pub mod fastmirror;
pub mod datetime;
pub mod utils;
mod checker;

pub struct Collector {
    project_name: String,
    records: HashSet<Metadata>,
    client: HttpClient,
    remote_host: String,
    username: String,
    password: String,
    exception_handler: fn (Error)
}

fn default_exception_handler(error: Error) {
    eprintln!("{}: \n{}", error, error.backtrace());
    std::process::exit(1);
}

fn helper(name: &String) {
    println!(r#"usage: {name} [--host=<remote host>] [(--username|-u)=<username>] [(--password|-p)=<password>] [--help|-h]"#);
    std::process::exit(0);
}

impl Collector {
    pub fn new(project_name: &str) -> Result<Self> {
        let mut remote_host: String = env::var("COLLECTOR_REMOTE_HOST").unwrap_or(String::default());
        let mut username: String = env::var("COLLECTOR_USERNAME").unwrap_or(String::default());
        let mut password: String = env::var("COLLECTOR_PASSWORD").unwrap_or(String::default());

        let mut args = env::args().collect::<Vec<String>>();
        let app_name = args.remove(0);

        for arg in args {
            let (key, value) = match split_once(&arg, "=") {
                Ok((a, b)) => (a, b),
                Err(_) => (arg.as_str(), "")
            };
            match key.to_lowercase().as_str() {
                "--host"     => { remote_host = value.to_string(); }
                "--username" => { username = value.to_string(); }
                "-u"         => { username = value.to_string(); }
                "--password" => { password = value.to_string(); }
                "-p"         => { password = value.to_string(); }
                "--help"     => helper(&app_name),
                "-h"         => helper(&app_name),
                _            => helper(&app_name)
            }
        }

        Ok(Self {
            project_name: project_name.to_string().to_owned(),
            records: HashSet::new(),
            client: client(), 
            remote_host,
            username,
            password,
            exception_handler: default_exception_handler
        })
    }

    pub fn remote_host(mut self, remote_host: &str) -> Self { self.remote_host = remote_host.to_string(); self }
    pub fn authorization(mut self, username: &str, password: &str) -> Self {
        self.username = username.to_string();
        self.password = password.to_string();
        self
    }

    fn downloader(&self, manifest: &Manifest) -> Result<Bytes> {
        let id = manifest.id();

        println!("start download {id}");
        let result = Ok(self.client.get(manifest.download_url()).send()?.bytes()?);
        println!("{id} download successful.");

        result
    }

    fn uncatched_single_task(&mut self, manifest: Manifest) -> Result<bool> {
        if self.up_to_date(&manifest)? { return Ok(false); }

        let name = &self.project_name;
        let file = self.downloader(&manifest)?;

        let manifest = manifest.set_sha1( {
            let mut digest = Sha1::new();
            digest.update(&file[..]);
            let bytes = digest.digest().bytes();
            hex::encode(&bytes)
        } );

        // create task
        let task = match self.create_task(&manifest) {
            Ok(ret) => ret,
            Err(e) => {
                println!("{e}");
                return Ok(false)
            }
        };

        println!("{name} detected a new version: {}", manifest.id());

        let url = {
            if let Some(tmp) = &task["upload_uri"] { tmp }
            else                               { return Ok(true); }
        };

        let total_size = file.len();
        let mut uploaded = 0;

        // upload file
        println!("start upload file {}", manifest.filename());
        let mut iterator = file.chunks_exact(480 * 1024);

        while let Some(chunk) = iterator.next() {
            let result = self.upload(url, chunk, uploaded, total_size)?;

            uploaded += chunk.len();

            let expired = datetime::parse(&result.expired_time, ISO8601)?;
            if expired < datetime::now() { return Err(Error::msg("upload timeout.")); }
        }
        
        let chunk = iterator.remainder();
        self.upload(url, chunk, uploaded, total_size)?;
        uploaded += chunk.len();
        assert!(uploaded == total_size);

        println!("upload finished.");

        // close task
        self.close_task(&manifest)?;
        
        self.append_record(&manifest)?;

        Ok(true)
    }

    pub fn run<I>(&mut self, generator: I) -> Result<()> where I: Iterator<Item=Manifest> {
        for manifest in generator {
            let manifest = manifest.set_name(self.project_name.to_string());
            let id = manifest.id();

            match self.uncatched_single_task(manifest) {
                Ok(status) => { if status { println!("{id} upload successful.") } else { println!("{id} skipped.") } },
                Err(e) => (self.exception_handler)(e),
            }
        }
        Ok(())
    }
}
