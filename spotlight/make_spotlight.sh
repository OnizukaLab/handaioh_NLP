#!/bin/bash
docker pull dbpedia/spotlight-japanese
docker build -f Dockerfile  -t dbpedia/spotlight-japanese .
docker run -itd --name splotlight-jp -p 2250:80 dbpedia/spotlight-japanese spotlight.sh
