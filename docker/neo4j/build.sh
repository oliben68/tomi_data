#!/usr/bin/env bash

SERVICE_NAME=${PWD##*/}

docker build -t ${SERVICE_NAME}.local .