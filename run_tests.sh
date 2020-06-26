set -e
#Ensure in directory where code is. 
cd $(dirname $0)
echo "$PWD"
#BUILD ANGULAR 
sh build_angular.sh
#BUILD MAIN CONTAINER 
docker build -t plark_ai -f "$PWD"/Docker/Dockerfile  "$PWD"/Docker
#BUILD PACKAGED CONTAINER.
## Get test data
mkdir -p "$PWD"/data
#mc mirror gpupc/plarkai/ "$PWD"/data/
docker build -t packaged_plark_ai -f "$PWD"/Components/packaged_plark_ai/Dockerfile "$PWD"/ --build-arg CACHEBUST=$(date +%s)
