# Please make sure that your dbt profile has correct entries accordingly to [environment](../environment) file!

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