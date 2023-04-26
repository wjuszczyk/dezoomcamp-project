variable "project" {
  description = "Your GCP Project ID"
  default = "dtc-spotifyandyoutube"
  type= string
}

variable "gcs_name" {
  description = "Google Cloud Storage name"
  default = "sandy_bucket"
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "europe-central2"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "bq_dataset_staging" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  default = "sandy_staging"
  type = string
}