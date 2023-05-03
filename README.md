<p align="center">
  <img width="30%" src="https://storage.googleapis.com/kaggle-datasets-images/3025170/5201847/a6f88fcaa0cef264f41bb96d1cb05b58/dataset-cover.png?t=2023-03-20-16-35-48"/>
</p>

# Data Engineering ZoomCamp 2023 Course Project - Spotify and Youtube dataset analysis / SandY 

## Preface

tbd

## Technologies used:
&emsp;Infrastructure as Code: [Terraform](https://www.terraform.io)      
&emsp;Workflow Orchestration: [Prefect](https://www.prefect.io)   
&emsp;Data Transformation: [dbt](https://www.getdbt.com)  
&emsp;Data Lake: [Google Cloud Storage](https://cloud.google.com/storage)     
&emsp;Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery)    
&emsp;Visualisation: [Looker Studio](http://lookerstudio.google.com/)  

## Architecture Diagram

tbd

## Dataset description

Dataset of songs of various artist in the world and for each song is present:
- Several statistics of the music version on spotify, including the number of streams
- Number of views of the official music video of the song on youtube.

It includes 26 variables for each of the songs collected from Spotify but for this project only below ones were chosen:

<div align="center">

|#|Attribute|Description|
|:-:|:-:|-|
|1|id|Unique identifier of the record.|
|2|artist|name of the artist.|
|3|track|name of the song, as visible on the Spotify platform.|
|4|album|the album in wich the song is contained on Spotify.|
|5|album_type|indicates if the song is relesead on Spotify as a single or contained in an album.|
|6|danceability| describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.|
|7|energy| is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.|
|8|tempo|the overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.|
|9|views|number of views on YouTube.|
|10|likes|number of likes on YouTube.|
|11|comments|number of comments on YouTube.|
|12|stream|number of streams of the song on Spotify.|
|13|dur_min|the duration of the track in minutes (generated)|

</div>

More information about this dataset is available on [Kaggle](https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube)

## Data visualization: Dashboards

tbd

## How to reproduce this Project

### Requirements

&emsp;1. [Pandas](https://pandas.pydata.org/)<br>
&emsp;2. [Git](https://git-scm.com/)<br>
&emsp;3. [Kaggle](https://www.kaggle.com/) free account<br>
&emsp;4. [Google Cloud Platform]() account<br>

### Step 1: Setup local Conda environment

1. Create conda environment and install pip
```bash
$ conda create --name sandy
$ conda activate sandy
$ conda install pip
```
2. Clone the project and change to project's directory
```bash
$ git clone git@github.com:tmaferreira/DataEngineeringZoomCampProject.git
$ cd datazoomcamp-project
```
3. Install rest of requirements
```bash
$ pip install -r 
```
### Step 2: Setup GCP

1. Create new project on [Google Cloud Platform](https://console.cloud.google.com/projectcreate) and **remember the project's name**, it will be needed later. 

<p align="center">
<img width="80%" src="images/gcp-project-setup.png"/>
</p>

- Edit ```environment``` file and set *PROJECT_ID* parameter with the project's name.

```bash
$ grep ^PROJECT_ID environment
PROJECT_ID="sandy-dtc-project"
```

2. Create a Service Account:
    - Go to **IAM & Admin > Service accounts > Create service account** and create it

<p align="center">
<img width="80%" src="images/gcp-iam1.png"/>
</p>

- Provide a service account name and grant the roles: **Viewer**, **BigQuery Admin**, **Storage Admin**, **Storage Object Admin**

<p align="center">
<img width="80%" src="images/gcp-iam2.png"/>
</p>

- Create and download the Service Account key file (json format)

<p align="center">
<img width="80%" src="images/gcp-iam3.png"/>
</p>

3. Edit ```environment``` file and set *GOOGLE_APPLICATION_CREDENTIALS* to point to location where downloaded json file exists.

```bash
$ grep ^GOOGLE_APP environment
GOOGLE_APPLICATION_CREDENTIALS="d:\Workspace\sandy\dezoomcamp-project\sandy-dtc-project-e7869e1be3b1.json"
```
4. Source the ```environment``` file.
```bash
$ . ./environment
```

### Step 3: Setup terraform

1. Install [Terraform](https://www.terraform.io) and place binary in path location
2. Modify terraform/variables.tf file and set GCP project ID. 

```bash
variable "project" {
  description = "Your GCP Project ID"
  default = "sandy-dtc-project"
  type= string
}
```

3. change directory to terraform and init it

```bash
$ cd terraform
$ terraform init
```

4. set up bucket and BigQuery structure

```bash
$ terraform plan
$ terraform apply
```


## Please make sure that your dbt profile has correct entries accordingly to [environment](../environment) file!

`$HOME/.dbt/profiles.yml`

`spotify_and_youtube:`<br>
&nbsp;`outputs:`<br>
&ensp;`dev:`<br>
&emsp;`dataset: sandy_staging`	***($GCP_TABLE)***<br>
&emsp;`job_execution_timeout_seconds: 300`<br>
&emsp;`job_retries: 1`<br>
&emsp;`keyfile: *.json` ***($GOOGLE_APPLICATION_CREDENTIALS)***<br>
&emsp;`location: europe-central2`<br>
&emsp;`method: service-account`<br>
&emsp;`priority: interactive`<br>
&emsp;`project: dtc-spotifyandyoutube` ***($PROJECT_ID)***<br>
&emsp;`threads: 4`<br>
&emsp;`type: bigquery`<br>
&ensp;`target: dev`<br>
```