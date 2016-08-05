#!/bin/sh
./cpy.sh
docker run --rm -v ..:/usr/src/Atlassian -it atlas_cli