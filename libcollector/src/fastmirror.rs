pub mod api {
    use std::collections::HashMap;

    use anyhow::{Result, Error};
    use map_macro::hash_map;
    use serde::{Serialize, Deserialize};
    use time::macros::offset;

    use crate::{manifest::Manifest, Collector, datetime::ISO_DATE_TIME};

    #[derive(Serialize, Deserialize, Debug, Default)]
    pub struct ApiResponse<T> {
        pub data: Option<T>,
        pub code: String,
        pub success: bool,
        pub message: String
    }

    #[derive(Serialize, Deserialize, Debug)]
    pub struct TaskReport {
        pub next_expected_range: Vec<String>,
        pub expired_time: String
    }

    pub fn get_data_from_response<T>(response: ApiResponse<T>) -> Result<T> {
        if !response.success { 
            return Err(Error::msg(format!("request failed.\n\tmsg = {}\n\tcode = {}\n", response.message, response.code))); 
        }
        response.data.ok_or(Error::msg("Unexcepted value: ApiResponse.data == `None`"))
    }

    impl Collector {

        pub(crate) fn create_task(&self, artifact: &Manifest) -> Result<HashMap<String, Option<String>>> {
            let host = &self.remote_host;
            let url = format!("{host}/api/v3/upload/session/create");
            
            let info = hash_map! {
                        "name" => artifact.name().to_string(),
                  "mc_version" => artifact.mc_version().to_string(),
                "core_version" => artifact.core_version().to_string(),
                 "update_time" => artifact.update_time().to_offset(offset!(+0)).format(ISO_DATE_TIME)?,
                        "sha1" => artifact.sha1().unwrap().to_string(),
                    "filetype" => artifact.filetype().to_string(),
            };
            let response = self.client
                .post(url)
                .basic_auth(&self.username, Some(&self.password))
                .json(&info)
                .send()?
                .json::<ApiResponse<HashMap<String, Option<String>>>>()?;
            get_data_from_response(response)
                .and_then(|o| { println!("task created."); Ok(o) })
        }

        fn internal_upload(&self, url: &String, chunk: &[u8], offset: usize, total_size: usize) -> Result<TaskReport> {
            let end = offset + chunk.len() - 1;
            let range = &format!("bytes {offset}-{end}/{total_size}");
            
            let action = || {
                let report = self.client.put(url)
                    .basic_auth(&self.username, Some(&self.password))
                    .body(chunk.to_vec())
                    .header("Content-Range", range)
                    .header("Content-Length", chunk.len().to_string().as_str())
                    .send()?
                    .json::<ApiResponse<TaskReport>>()?;
                print!("\rprogress: {:2.2}%", (offset as f64) / (total_size as f64) * (100 as f64));
                get_data_from_response(report)
            };

            for i in 0 .. 3 {
                let ret = action();
                match ret {
                    Ok(ret) => return Ok(ret),
                    Err(e) => {
                        println!("upload failed. retry={i}.\n\t{e}");
                        if i == 2 { return Err(e) }
                    }
                }
            }
            Err(Error::msg("unknown error."))
            
        }

        pub(crate) fn upload(&self, url: &String, chunk: &[u8], offset: usize, total_size: usize) -> Result<TaskReport> {
            self.internal_upload(url, chunk, offset, total_size)
        }

        pub(crate) fn close_task(&self, artifact: &Manifest) -> Result<()> {
            let host = &self.remote_host;
            let name = artifact.name();
            let mc_version = artifact.mc_version();
            let core_version = artifact.core_version();
            println!("close task {name}-{mc_version}-{core_version}.");

            let url = format!("{host}/api/v3/upload/session/close/{name}/{mc_version}/{core_version}");

            let _ = get_data_from_response(self.client.put(url)
                .basic_auth(&self.username, Some(&self.password))
                .send()?
                .json::<ApiResponse<Option<HashMap<String, String>>>>()?);
            Ok(())
        }
    }
}