#!/usr/bin/env bash

SERVICE_NAME=${PWD##*/}

docker run -p 7474:7474 -p 7373:7373 -p 7687:7687 -d ${SERVICE_NAME}.local:latest