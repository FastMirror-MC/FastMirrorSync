use anyhow::{Result, Error};

pub fn split_once<'v>(string: &'v str, delimiter: &str) -> Result<(&'v str, &'v str)> {
    string.split_once(delimiter).ok_or(Error::msg(format!("invalid format: {string}")))
}
