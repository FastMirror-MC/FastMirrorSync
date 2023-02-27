use time::OffsetDateTime;

#[derive(Debug)]
pub struct Manifest {
    name: String,
    mc_version: String,
    core_version: String,
    filetype: String,
    sha1: Option<String>,
    update_time: OffsetDateTime,
    download_url: String
}

impl Default for Manifest {
    fn default() -> Self { Self { 
        name: Default::default(), 
        mc_version: Default::default(), 
        core_version: Default::default(), 
        filetype: Default::default(), 
        sha1: Default::default(),
        update_time: OffsetDateTime::now_utc(),
        download_url: Default::default()
    } }
}

impl Manifest {
    pub fn id(&self)           -> String  { format!("{}-{}-{}", &self.name, &self.mc_version, &self.core_version) }
    pub fn filename(&self)     -> String  { format!("{}.{}", self.id(), &self.filetype) }
    pub fn name(&self)         -> &String { &self.name }
    pub fn mc_version(&self)   -> &String { &self.mc_version }
    pub fn core_version(&self) -> &String { &self.core_version }
    pub fn filetype(&self)     -> &String { &self.filetype }
    pub fn update_time(&self)  -> &OffsetDateTime { &self.update_time }
    pub fn sha1(&self)         -> Option<&String> { self.sha1.as_ref() }
    pub fn download_url(&self) -> &String { &self.download_url }

    pub fn new() -> Self { Manifest::default() }

    pub fn set_name(mut self, name: String)                       -> Self { self.name = name; self }
    pub fn set_mc_version(mut self, mc_version: String)           -> Self { self.mc_version = mc_version; self }
    pub fn set_core_version(mut self, core_version: String)       -> Self { self.core_version = core_version; self }
    pub fn set_filetype(mut self, filetype: String)               -> Self { self.filetype = filetype; self }
    pub fn set_sha1(mut self, sha1: String)                       -> Self { self.sha1 = Some(sha1); self }
    pub fn set_update_time(mut self, update_time: OffsetDateTime) -> Self { self.update_time = update_time; self }
    pub fn set_download_url(mut self, url: String)                -> Self { self.download_url = url; self }
}

impl Into<Manifest> for &Manifest {
    fn into(self) -> Manifest { Manifest { 
        name: self.name.clone(), 
        mc_version: self.mc_version.clone(), 
        core_version: self.core_version.clone(), 
        filetype: self.filetype.clone(), 
        sha1: self.sha1.clone(), 
        update_time: self.update_time.clone(), 
        download_url: self.download_url.clone()
    } }
}
