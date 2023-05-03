![dataset-cover.png](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/dataset-cover.png)

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
$ pip install -r requirements.txt
```
### Step 2: Setup GCP

1. Create new project on [Google Cloud Platform](https://console.cloud.google.com/projectcreate) and **remember the project's name**, it will be needed later. 

![gcp_project_setup.png](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/gcp-project-setup.PNG)

- Edit ```environment``` file and set *PROJECT_ID* parameter with the project's name.

```bash
$ grep ^PROJECT_ID environment
PROJECT_ID="sandy-dtc-project"
```

2. Create a Service Account:
    - Go to **IAM & Admin > Service accounts > Create service account** and create it

![gcp-iam1.png](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/gcp-iam1.PNG)

- Provide a service account name and grant the roles: **Viewer**, **BigQuery Admin**, **Storage Admin**, **Storage Object Admin**

![gcp-iam2.png](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/gcp-iam2.PNG)

- Create and download the Service Account key file (json format)

![gcp-iam3.png](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/gcp-iam3.PNG)

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

### Step 4: Kaggle setup

On [Kaggle](https://www.kaggle.com/) go to [Account Settings](https://www.kaggle.com/settings/account) and create new API token.
Put downloaded kaggle.json file in dezoomcap-project directory.

### Step 5: Prefect setup

1. Run Prefect server on second terminal window

```bash
$ conda activate sandy
$ prefect orion start
```

2. Open [Prefect dashboard](http://127.0.0.1:4200) and go to Blocks section

- Add new Block named "GCP Credentials" and fill it with name (same as in *GCP_CREDENTIALS* parameter in ```environment``` file) and paste content of GCP Service Account key json file on Service Account Info section.

![prefect-block1](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/prefect-block1.PNG)

- go back to Blocks and add another one - GCS Bucket. Fill the Block Name with *GCP_BUCKET* parameter in ```environment``` file, set name of bucket and set Gcp Credentials to Block created above.

![prefet-block2](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/prefect-block2.PNG)

3. Go to prefect directory and run both python files. All flows should be completed.

```bash
$ cd prefect
$ python etl_web_to_gcs.py
$ python etl_gcs_to_bq_param.py
```

### Step 6: DBT setup

1. Go to dbt directory and init it as below

```
$ dbt init
22:04:04  Running with dbt=1.5.0
22:04:04  Setting up your profile.
Which database would you like to use?
[1] bigquery

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 1
[1] oauth
[2] service_account
Desired authentication method option (enter a number): 2
keyfile (/path/to/bigquery/keyfile.json): d:\Workspace\sandy\dezoomcamp-project\sandy-dtc-project-e7869e1be3b1.json
project (GCP project id): sandy-dtc-project
dataset (the name of your dbt dataset): sandy_staging
threads (1 or more): 4
job_execution_timeout_seconds [300]:
[1] US
[2] EU
Desired location option (enter a number): 2
22:05:20  Profile spotify_and_youtube written to C:\Users\wj\.dbt\profiles.yml using target's profile_template.yml and your supplied values. Run 'dbt debug' to validate the connection.
```

2. Check if all settings are working fine. Output should be similar to as below.

```
$ dbt debug
22:06:12  Running with dbt=1.5.0
22:06:12  dbt version: 1.5.0
22:06:12  python version: 3.11.3
22:06:12  python path: D:\Programs\Anaconda3\envs\sandy\python.exe
22:06:12  os info: Windows-10-10.0.19045-SP0
22:06:12  Using profiles.yml file at C:\Users\wj\.dbt\profiles.yml
22:06:12  Using dbt_project.yml file at D:\Workspace\sandy\dezoomcamp-project\dbt\dbt_project.yml
22:06:12  Configuration:
22:06:13    profiles.yml file [OK found and valid]
22:06:13    dbt_project.yml file [OK found and valid]
22:06:13  Required dependencies:
22:06:13   - git [OK found]

22:06:13  Connection:
22:06:13    method: service-account
22:06:13    database: sandy-dtc-project
22:06:13    schema: sandy_staging
22:06:13    location: EU
22:06:13    priority: interactive
22:06:13    timeout_seconds: 300
22:06:13    maximum_bytes_billed: None
22:06:13    execution_project: sandy-dtc-project
22:06:13    job_retry_deadline_seconds: None
22:06:13    job_retries: 1
22:06:13    job_creation_timeout_seconds: None
22:06:13    job_execution_timeout_seconds: 300
22:06:13    gcs_bucket: None
22:06:16    Connection test: [OK connection ok]

22:06:16  All checks passed!
```

3. Install dependencies

```
$ dbt deps
22:07:38  Running with dbt=1.5.0
22:07:39  Installing dbt-labs/dbt_utils
22:07:40  Installed from version 0.8.0
22:07:40  Updated version available: 1.1.0
22:07:40
22:07:40  Updates available for packages: ['dbt-labs/dbt_utils']
Update your versions in packages.yml, then run dbt deps
```

4. Modify ```models/staging/schema.yml``` file and set databse setting to match your *GCP project ID*

```bash
$ grep database models/staging/schema.yml
    database: sandy-dtc-project
```

5. Run dbt, views should be created successfully

```bash
$ dbt run
22:17:35  Running with dbt=1.5.0
22:17:37  Found 2 models, 1 test, 0 snapshots, 0 analyses, 540 macros, 0 operations, 0 seed files, 1 source, 0 exposures, 0 metrics, 0 groups
22:17:37
22:17:38  Concurrency: 4 threads (target='dev')
22:17:38
22:17:38  1 of 2 START sql view model sandy_staging.stg_sandy_data ....................... [RUN]
22:17:40  1 of 2 OK created sql view model sandy_staging.stg_sandy_data .................. [CREATE VIEW (0 processed) in 1.80s]
22:17:40  2 of 2 START sql view model sandy_staging.facts_sandy .......................... [RUN]
22:17:42  2 of 2 OK created sql view model sandy_staging.facts_sandy ..................... [CREATE VIEW (0 processed) in 2.14s]
22:17:42
22:17:42  Finished running 2 view models in 0 hours 0 minutes and 5.09 seconds (5.09s).
22:17:42
22:17:42  Completed successfully
22:17:42
22:17:42  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2
```

![dbt2](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/dbt2.PNG)

6. If you have an error that dataset is not found in location EU (404 Not found) please change the location parameter in ~/.dbt/profiles.yml to data location where BigQuery dataset is:

```bash
$ grep location ~/.dbt/profiles.yml
      location: EU
```

![dbt1](https://github.com/wjuszczyk/dezoomcamp-project/blob/master/images/dbt1.PNG)

```bash
$ grep location ~/.dbt/profiles.yml
      location: europe-central2
```
