hostname=$(uname -n)
docker run --rm --privileged ketirepo/beacon $(hostname)
