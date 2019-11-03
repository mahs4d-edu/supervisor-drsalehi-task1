# Supervisor Task By Dr.Salehi, Telegram Crawler

this project has two separate programs, crawler and indexer which are connected through rabbitmq.

the crawler program connects to telegram with a bot session generated earlier and listens for new messages. each new message is decrypted to sender name and message text and sent on the rabbitmq channel to be indexed by indexer.

indexer program receives new messages from rabbitmq channel and indexes it on elasticsearch.

the project is structured in this manner (microservices with async communication among them) so that we could replicate as much as crawler or indexer instances as we want through separate physical or virtual servers, as long as they all can access the underlying rabbitmq and elasticsearch servers. the structure completly scalable for both horizontal scaling of microservices (crawler and indexer) and for adding new microservices to the system as none of the services are aware of the other services existance. so for instance if we want to add a new microservice to the system which saves the messages in a remote filesystem or that raises an alarm for a certain message, we can do it without modifying any of crawler or indexer parts. the new service can be plugged in to the system only by listening to the same channel that crawler publishes to or querying the elasticsearch directly.

# Run the Project

to run and test the project you can use the docker-compose file provided. simply run following commands:

`docker-compose build`

`docker-compose up`

after some time the system reaches a stable state where you can send messages to **@telecrawlbot** in telegram for them to be indexed. there is a kibana service added to docker-compose so that you can query and view indexed data easily by access the dashboard through [here](http://localhost:5691)
