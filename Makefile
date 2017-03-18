build:
	docker-compose build
	docker build -f Dockerfile.jupyter -t jupyter .

up:
	mkdir -p /data/jupyterhub /data/xena /data/notebooks /data/scratch
	docker-compose up

down:
	docker-compose down

load:
	docker exec hub_xena_1 java -jar /ucsc_xena/cavm-0.21.0-standalone.jar --load /root/xena/files/$(file)
