# tagcloud
Fetch and parse Twitter data to find the most used words in a given amount of time.

# Requirements

Install python2.7:

	apt-get install python2.7
	apt-get install python2.7-dev

Install pip:

	https://pip.pypa.io/en/latest/installing.html

Install docker:

	http://docs.docker.com/installation/ubuntulinux/#installing-docker-on-ubuntu
	
Install docker-compose:

	pip install -U docker-compose

# Running the application
To start the application inside the containers:
	
	start.sh SECONDS MAXWORDS
		- SECONDS => time of receiving sample data from Twitter
		- MAXWORDS => number of words in the top


To run the application without containers (but you need a running Redis server):

	python2.7 tagCloud.py SECONDS MAXWORDS
		- SECONDS => time of receiving sample data from Twitter
		- MAXWORDS => number of words in the top

