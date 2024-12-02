# pythonPerformanceCase

In this project, an attempt was made to find a solution to the case I mentioned below.
## Target Case
You should be able to get location, speed, etc. location information intensively to Rest API
services (you can think of 1 million of this data per day). You can store this data in a
database of your choice. The data coming to API services should be processed
asynchronously, so you need to use a queue management tool, we currently use RabbitMQ
or Celery. We should be able to access this data for a specic date range + you should create
Rest API services where we can only access the last data for a device.

 - can send location information with the Rest API Service. 
 - can access this data for a specific date range.
 - can only access the last data for a device. 

## Built With
- Python
- PyCharm or Visual Studio Code
- FastAPI
- PostgreSql
- RabbitMQ
- Docker

## Installation
1. Clone the repo [repo](https://github.com/taniltekdemir/pythonPerformanceCase.git)
2. Import the project to your IDE
3. In Project, Docker-compose.yml file is exist. You can start to project with this file.
    You can use the following commands: 
- docker-compose build
- docker-compose up -d
4. You can send requests using the postman and see the endpoints in Collection. It is added to code. (TruckData.postman_collection.json)
5. The project is running on the 8000 port by default. You can access the project run on the client side from http://localhost:8000
6. Related DB and DB table will create when you can start to project. PgAdmin is existed in docker-compose.yml. So, you can see it on http://localhost:5050/browser/
7. RabbitMQ dashboard will run on http://localhost:15672/   


## Some Highlights
- A test method that can create bulk requests under the /tests directory for performance 
and integration purposes was prepared in the project. In the current situation, it will prepare 
1000 record requests and send the request to the running project.


- You will see that the created requests are first taken to the truck_data_queue queue with RabbitMQ, and then consumed by the consumer called worker,
which is run with the project.


- You can get all records within a certain date range.


- You can also get the latest registration of a truck.



