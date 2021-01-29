#!/usr/bin/env bash


docker run --name technicals-mongo -v .mongo-data:/data/db -p 27017:27017 -d mongo
