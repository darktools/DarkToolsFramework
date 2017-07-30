#!/bin/bash

echo "This will clean out everything relating to docker on this endpoint (e.g. containers, images, etc...)"
read -p "Are you sure you (y/N)? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -q)
docker rmi -f $(docker images -q)
docker rmi -f $(docker images -q)

docker rmi $(docker images -f dangling=true -q)

# remove exited containers:
docker ps --filter status=dead --filter status=exited -aq | xargs -r docker rm -v

# remove unused images:
docker images --no-trunc | grep '<none>' | awk '{ print $3 }' | xargs -r docker rmi

# remove unused volumes:
find '/var/lib/docker/volumes/' -mindepth 1 -maxdepth 1 -type d | grep -vFf <(
  docker ps -aq | xargs docker inspect | jq -r '.[] | .Mounts | .[] | .Name | select(.)'
) | xargs -r rm -fr

docker images --no-trunc | grep '<none>' | awk '{ print $3 }' | xargs -r docker rmi
docker ps --filter status=dead --filter status=exited -aq | xargs docker rm -v
docker volume ls -qf dangling=true | xargs -r docker volume rm