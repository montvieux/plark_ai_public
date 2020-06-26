docker build -t plark_ai_angular Components/web-ui
docker run -v "$PWD"/Components/plark_ai_flask/builtangularSite/:/output plark_ai_angular
chmod -R 777 "$PWD"/Components/plark_ai_flask/builtangularSite/