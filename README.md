# FTwitter Bot
Bot for tweeting news articles from RSS feeds.

## Pre-requisites
* Docker (version 18.09.2 or higher)

## Installation
1. `docker build -f etc/docker/Dockerfile -t futuristick . --build-arg CRON=[CRONTAB]`  
where `[CRONTAB]` is the crontab value to be used for scheduling. For example: `*/5 * * * *`

## Running
1. `docker run -d --name futuristick-app futuristick`

## Configuration
The bot uses 2 configuration files: `config/properties.json` and `config/rss.json`. If you modify the configuration files
within a docker container, then the changes are applied the next time that the bot is scheduled to be run.
If you modify the source files outside of a container, then you need to rebuild the image and create a new container as described
in the `Installation` and `Running` steps.

### properties.json
| Key | Description |
|---|---|
| `twitter` | Contains the Twitter API configuration |
| `constant_tags` | List of constants hashtags that that are attached to each tweet |
| `max_tags_per_post` | Maximum number of hashtags that can be attached to a tweet |
| `use_default_tags` | If enabled, appends `default_tags` from `rss.json` to a tweet |
| `max_post_count` | Maximum number of tweets that can be posted each time the bot runs |

### rss.json
| Key | Description |
|---|---|
| `url` | RSS feed link |
| `default_tags` | List of default tags that can be appended to a tweet if `use_default_tags` property is enabled |

## Common workflows

### JSON configuration changes

It is possible to modify the JSON configuration files within an existing container, 
eliminating the need for rebuilding the image and recreating the container. To do this:
1. `docker exec -it futuristick-app sh`
2. `cd ./futuristick/config`
3. `vi properties.json`
4. Make the necessary changes using vim, and save the changes.
5. `exit`

The next time the script is scheduled to run, the updated parameters will be used.

### Scheduling changes

The scheduled script execution within the container is done by using crontab. You can modify the
crontab by entering the container:
1. `docker exec -it futuristick-app sh`
2. `crontab -e`
3. Make changes to the crontab in vim as necessary and save.
4. `exit`

### Modifying source files

Changes within the container are lost if you need to rebuild the container. Therefore to make 
sure that important changes persist, it may be necessary to modify the actual source files. Once 
you have made the necessary changes you can rebuild the image and recreate the container:
1. `docker stop futuristick-app`
2. `docker rm -v futuristick-app`
3. `docker build -f etc/docker/Dockerfile -t futuristick . --build-arg CRON=[CRONTAB]`  
4. `docker run -d --name futuristick-app futuristick`

## Logging

The script logs all information to standard output, which can be accessed by:
1. `docker logs -f futuristick-app`
2. `Ctrl + C`
