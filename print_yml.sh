#!/bin/bash

echo "app:
 build: .
 command: python tagCloud.py $1 $2
 volumes:
  - .:/code
 links: 
  - redis

redis:
 image: redis
 expose: 
  - \"6379\"" > docker-compose.yml
