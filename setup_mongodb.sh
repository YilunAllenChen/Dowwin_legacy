#!bin/bash

name='mongodb'
mongo_volume="$HOME/docker/volumes/mongodb"
mongo="mongo:4.2.2"

{
# Make sure an existing docker isn't running.
if sudo docker ps -f name=$name | grep -q $name ; then
    echo "Mongodb is already running."
    exit 1
fi

if ! sudo docker image list | grep -q mongo; then
    echo "Pulling $mongo from docker hub..."
    sudo docker pull $mongo
    echo "Done."
fi


# Make sure our mount path isn't already in use.
if [ ! -d $mongo_volume ] ; then
    sudo mkdir -p $mongo_volume
fi
} || {
    echo "Failed to mount docker. Exiting..."
    exit 1
}


{
    echo "Docker mounted. Starting mongodb now on port 27017..."
    sudo docker run --rm -v /data/db:$mongo_volume --name mongodb -d -p 27017:27017 $mongo
} || {
    echo "Can't instantiate mongo docker."
    exit 1
}

sudo docker ps -f name=$name
echo "Docker is running as '$name'."