#!/bin/bash

docker build . -t www.supercooleapp.com/nmd/donationbot:latest --no-cache

docker run --network=host --rm www.supercooleapp.com/nmd/donationbot:latest 

