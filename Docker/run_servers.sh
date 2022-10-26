#!/bin/bash
# Example usage
# sh run_servers.sh
pip install -e /Components/plark-game
pip install -e /Components/gym-plark
pip install -e /Components/agent-training

echo "*********************"
echo "Starting Jupyter:"
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root --NotebookApp.iopub_data_rate_limit=1000000 --NotebookApp.token='' & 

echo "*********************"
echo "Export flask app:"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=/Components/plark_ai_flask/plark_ai_flask.py 
export FLASK_ENV=development
echo "*********************"
echo "Run flask:"
flask run --host=0.0.0.0 &
