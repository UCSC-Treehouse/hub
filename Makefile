up:
	docker-compose up

down:
	docker-compose down

letsencrypt:
	sudo letsencrypt certonly --standalone \
		-d www.scellucsc.net \
		-d xena.scellucsc.net \
		-d ga4gh.scellucsc.net \
		-d jupyter.scellucsc.net \
		-d nbviewer.scellucsc.net \
		-d tensorboard.scellucsc.net

load:
	docker exec scell_xena_1 java -jar /ucsc_xena/cavm-0.21.0-standalone.jar --load /root/xena/files/$(file)
