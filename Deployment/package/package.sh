#!/bin/bash
# Example usage
# sh package.sh /srv/plark_ai/code_drop

cd $(dirname $0)
if [ -d $1 ]; then
    echo "Package location:$1"
else
    echo "Package location:$1 does not exist "
    echo "Example use: sh package.sh /srv/plark_ai/code_drop"
    exit 1
fi

date=$(date +"%y%m%d")

PRE_PACKAGE_DIR="$1/${date}"
mkdir ${PRE_PACKAGE_DIR}
PACKAGE_DIR="$1/${date}/plark_ai"
echo "${PACKAGE_DIR}"
 
mkdir ${PACKAGE_DIR}

mkdir ${PACKAGE_DIR}/Components

# move documentation to correct dir

echo "Copy readme:"
cp ../../README.md ${PACKAGE_DIR}/README.md
cp ./add_licence.sh ${PACKAGE_DIR}/add_licence.sh
cp ./licence.txt ${PACKAGE_DIR}/licence.txt


mkdir ${PACKAGE_DIR}/Docker
# Copy docker. 
cp -r ../../Docker ${PACKAGE_DIR}

mkdir ${PACKAGE_DIR}/Documentation
cp -r ../../Documentation ${PACKAGE_DIR}

#Copy supporting files
cp ../../build_angular.sh ${PACKAGE_DIR}/build_angular.sh
cp ../../docker-compose.yml ${PACKAGE_DIR}/docker-compose.yml
cp ../../robot_testing_readme.md ${PACKAGE_DIR}/robot_testing_readme.md
cp ../../run_tests_cpu.sh ${PACKAGE_DIR}/run_tests_cpu.sh
cp ../../run_tests.sh ${PACKAGE_DIR}/run_tests.sh

# move code to correct dir
echo "Copy code:"
cp -r ../../Components/agent-training ${PACKAGE_DIR}/Components
cp -r ../../Components/gym-plark ${PACKAGE_DIR}/Components
cp -r ../../Components/packaged_plark_ai ${PACKAGE_DIR}/Components
cp -r ../../Components/plark_ai_flask ${PACKAGE_DIR}/Components
cp -r ../../Components/plark-game ${PACKAGE_DIR}/Components
cp -r ../../Components/stable-baselines ${PACKAGE_DIR}/Components
cp -r ../../Components/web-ui ${PACKAGE_DIR}/Components

# move data from minio
echo "Copy data:"
mkdir ${PACKAGE_DIR}/data

#Copy trained agent models into data 
#mc mirror gpupc/plarkai/ ${PACKAGE_DIR}/data/

#add licence information to all of the python files
echo "Adding licence to python files:"
find ${PACKAGE_DIR}/ -type f -name *.py -exec ${PACKAGE_DIR}/add_licence.sh '{}' \;

echo "Build documentation"
docker run --rm --volume ${PACKAGE_DIR}:/data --user `id -u`:`id -g` pandoc/latex README.md -o Documentation/Hunting_The_Plark.pdf -V geometry:margin=1in -V linkcolor:blue -V geometry:a4paper --indented-code-classes=code

# Build angular docker and build website.
echo "Building webpage:"
docker build -t plark_ai_angular ../../Components/web-ui
docker run -v ${PACKAGE_DIR}/Components/plark_ai_flask/builtangularSite/:/output plark_ai_angular

# Build containers 
echo "Build containers:"
mkdir ${PACKAGE_DIR}/Containers 

echo "Build CPU container:"
docker build -t plark_ai -f ${PACKAGE_DIR}/Docker/DockerfileCPU  ${PACKAGE_DIR}/Docker
echo "Save GPU container:"
docker save -o ${PACKAGE_DIR}/Containers/plark_ai_cpu.tar plark_ai
echo "Build Packaged CPU container:"
docker build -t packaged_plark_ai -f ${PACKAGE_DIR}/Components/packaged_plark_ai/Dockerfile ${PACKAGE_DIR}/
echo "Save Packaged CPU container:"
docker save -o ${PACKAGE_DIR}/Containers/packaged_plark_ai_cpu.tar packaged_plark_ai

echo "Build GPU container:"
docker build -t plark_ai -f ${PACKAGE_DIR}/Docker/Dockerfile  ${PACKAGE_DIR}/Docker
echo "Save GPU container:"
docker save -o ${PACKAGE_DIR}/Containers/plark_ai.tar plark_ai
echo "Build Packaged GPU container:"
docker build -t packaged_plark_ai -f ${PACKAGE_DIR}/Components/packaged_plark_ai/Dockerfile ${PACKAGE_DIR}/
echo "Save Packaged GPU container:"
docker save -o ${PACKAGE_DIR}/Containers/packaged_plark_ai.tar packaged_plark_ai

