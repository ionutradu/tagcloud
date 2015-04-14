# tagcloud
Fetch and parse Twitter data to find the most used words.

To start the application inside the containers:
	
	start.sh SECONDS MAXWORDS
		- SECONDS => time of receiving sample data from Twitter
		- MAXWORDS => number of words in the top


To run the application without containers (but you need a running Redis server):

	python2.7 tagCloud.py SECONDS MAXWORDS
		- SECONDS => time of receiving sample data from Twitter
		- MAXWORDS => number of words in the top

