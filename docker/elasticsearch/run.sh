#!/usr/bin/env bash

#docker run -p 9200:9200 -p 9300:9300 -d -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0
docker-compose up -d
