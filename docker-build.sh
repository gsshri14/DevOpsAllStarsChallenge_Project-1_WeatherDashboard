#!/bin/bash

# Build the Docker image
docker build -t weather-dashboard:latest -f Dockerfile .
