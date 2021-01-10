# futuristick
Twitter bot for tweeting news articles from RSS feeds.

## Pre-requisites
* Docker (version 18.09.2 or higher)

## Installation
1. `docker build -f etc/docker/Dockerfile -t futuristick . --build-arg CRON=[CRONTAB]`  
where `[CRONTAB]` is the crontab value to be used for scheduling. For example: `*/5 * * * *`
2. `docker run -d --name futuristick-app futuristick`

## Configuration
The bot can be configured via the `properties.json` file. As the script is executed on-demand via crontab, changes to the properties file will take effect on the subsequent run
if the changes are made within the container. If changes are made outside of the container in the source files, then the image must be rebuilt and the container recreated as 
described in the Installation step.
