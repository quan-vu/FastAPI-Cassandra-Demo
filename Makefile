export COMPOSE_PROJECT_NAME=fastapi-cassandra-demo
project=-p ${COMPOSE_PROJECT_NAME}

start-db:
	docker-compose up db_center_cassandra

build:
	docker-compose up -d --build

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v

restart:
	docker-compose restart 

test:
	docker-compose exec api bash -c "pytest" 

test-healcheck:
	curl --location --request GET 'http://localhost:8080/organizations/check' --header 'Content-Type: application/json' --data-raw '{"hello": "world"}'