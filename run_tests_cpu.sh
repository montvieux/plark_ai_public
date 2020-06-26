set -e
#Ensure in directory where code is. 
cd $(dirname $0)
echo "$PWD"
#BUILD ANGULAR 
sh build_angular.sh
#BUILD MAIN CONTAINER 
docker build -t plark_ai -f "$PWD"/Docker/DockerfileCPU  "$PWD"/Docker
## GET TEST DATA
mkdir -p "$PWD"/data
#mc mirror gpupc/plarkai/ "$PWD"/data/
#BUILD PACKAGED CONTAINER
docker build -t packaged_plark_ai -f "$PWD"/Components/packaged_plark_ai/Dockerfile "$PWD"/ --build-arg CACHEBUST=$(date +%s)
