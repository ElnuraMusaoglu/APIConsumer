# APIConsumer

## FastAPI Rest Application with unstable REST API

### Run project with docker-compose in the folder where the yml file is located:

```
docker-compose up -d --build
docker-compose up -d 

docker-compose logs web_cluster

docker-compose logs web

docker-compose exec web pytest .

```

## Project Structure : 


![project_structure](https://user-images.githubusercontent.com/79086158/207971241-487979f7-a2bf-4536-90ad-5ca788cf4fda.png)



### Summary
```
Solution with My Assumptions:

There is a cluster Rest API with POST GET DELETE methods to create get and delete groups. 
But the API is unstable and if an error occurs while creating 
or deleting groups the operation should be rollbacked.
The Rest API take parameters to create, get or delete the groups and sends a HTTP request to the cluster API. 
If an error occurs while sending create a group request to the cluster API, 
the API records it with the transaction id to the groupdelete table. 
If an error occurs while sending delete a group request to the cluster API, 
the API also records it with the transaction id to the groupdelete table to delete the data anyway. 
There is a background repeated task working every 30 seconds. 
When background job works, it gets transactions from groupdelete table 
and sends delete request to the cluster API. 
If the cluster API is still unstable, the operation is postponed to be done later. Otherwise, 
if the cluster API is stable, delete operation is carried out. 
If data doesn't exists in the cluster API or deleted successfully, 
the cluster API sends 200 or 204 HTTP response and the  API deletes the transaction from groupdelete table, 
and with this way rollback operation is carried out successfully.
There is also a producer (sender) application for API with Pika library 
to send rollback transaction operations to the cluster. 
In cluster API there is consumer (receiver) to get transactions and deletes the groups if exist via AMQP. 
But the message broker rollback operations were not used to sends the transactions via HTTP.
In Docker Compose there are two web services for the Group Rest API (Main Rest API) and cluster fake Rest API. 
And there is a PostgreSQL cluster. The database was not allocated because the cluster was added as fake.

```
### TODO :
```
-> Data Consistency with Kafka

-> Log to ELK

-> Timestamp record with transaction to uniqueness

-> More Pytest
```