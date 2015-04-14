#!/bin/bash

if [ $# -eq 1 ]; then
	./print_yml.sh $1 10
	docker-compose up
elif [ $# -eq 2 ]; then
	./print_yml.sh $1 $2
	docker-compose up
else
	echo "Usage: ./start.sh SECONDS [MAXWORDS]
		SECONDS - number of seconds to receive messages from Twitter
		MAXWORDS - optional, default 10, number of words in top"
fi
