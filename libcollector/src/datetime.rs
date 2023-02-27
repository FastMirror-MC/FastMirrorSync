use std::fmt::Debug;

use time::{OffsetDateTime, format_description::{FormatItem, well_known::Iso8601}, parsing::Parsable, macros::{format_description, offset}, PrimitiveDateTime};
use anyhow::Result;

pub const ISO_DATE_TIME: &[FormatItem<'_>] = format_description!("[year]-[month]-[day]T[hour]:[minute]:[second]");
pub const ISO_INSTANT: &[FormatItem<'_>] = format_description!("[year]-[month]-[day]T[hour]:[minute]:[second]Z");
pub const ISO8601:&Iso8601<6651332276412969266533270467398074368> = &Iso8601::DEFAULT;

pub fn parse(time: &String, description: &(impl Parsable + ?Sized + Debug)) -> Result<OffsetDateTime> {
    Ok(PrimitiveDateTime::parse(time, description)?.assume_offset(offset!(UTC)))
}
pub fn from_timestamp(timestamp: i64) -> Result<OffsetDateTime> {
    Ok(OffsetDateTime::from_unix_timestamp(timestamp)?)
}

pub fn now() -> OffsetDateTime {
    OffsetDateTime::now_utc()
}

/// 比较时间，精确到秒
/// OffsetDateTime自带的时间比较精度太高了，服务器里面存的时间也才精确到秒。
pub fn compare(lhs: &OffsetDateTime, rhs: &OffsetDateTime) -> bool {
    lhs.unix_timestamp() == rhs.unix_timestamp()
}