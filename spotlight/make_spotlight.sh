#!/bin/bash
sudo docker pull dbpedia/spotlight-japanese
sudo docker build -f Dockerfile  -t dbpedia/spotlight-japanese .
sudo docker run -i -p 2250:80 dbpedia/spotlight-japanese spotlight.sh
