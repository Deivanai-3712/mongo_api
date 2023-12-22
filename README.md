# **Retrieve data's from MongoDB to display them in Outsystem**

**/single_conversation (POST)**
1. Receives limit as Json Data.
2. Connect MongoDB based on credentials mentioned in ENV.
3. Filter records based on is_completed as True.
4. Return list of records.

**/single_conversation_filter (POST)**
1. Receives limit and email_address as Json Data.
2. Connect MongoDB based on credentials mentioned in ENV.
3. Filter records based on is_completed as True and email_address from either to or cc filed.
4. Return list of records.

**/email_summary (POST)**
1. Receives email_id, email_summary, email_summary_first, draft_message, is_completed as Json Data.
2. Update mongo db data based on email_id.


#### To build & deploy docker image

Login to the specific docker account from the machine where the code is developed
```shell
docker login --username <username> --password <password>
docker build -t <image_name> .
docker push <image_name>
```

**To deploy in server**

##### Option - 1

1. Switch to the required directory
2. Pull the docker image from the hub

```shell
docker pull <image_name>
docker run -d -p <host_port>:<service_port> <image_name>
docker ps
```

##### Option - 2

1. Switch to the required directory
2. Create a docker-compose.yml for integrating more details within
3. Sample docker-compose.yml file attached in root directory

```shell
docker-compose up -d
docker ps
```

To check docker running status

```shell
docker logs <container_id>
```

**Docker log monitoring**

```shell
docker exec -it <container_id> bash
/usr/workspace/mongo#
cd media/log
cat error.log
cat info.log
```