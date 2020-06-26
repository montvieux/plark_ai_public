from flask import Flask, send_file, request, jsonify, abort, render_template
import os
import argparse
import random
import sys
import numpy as np
import pickle
from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace
from io import BytesIO
from io import StringIO
import base64
import uuid
import json
import base64

import importlib

from plark_game import classes


from agent_training import helper 

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/',
            static_folder='builtangularSite/dist/', template_folder='builtangularSite/dist/')

trained_agents_filepath = '/data/agents/models'
basic_agents_filepath = '/Components/plark-game/plark_game/agents/basic'
config_filepath = '/Components/plark-game/plark_game/game_config'

additional_basic_agents = '/data/agents/basic'
additional_config_files = '/data/config'

env = classes.Environment()


web_ui_render_width = 1260
web_ui_render_height = 1000


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def encode_pil_image(pil_img):
    buffered = BytesIO()
    pil_img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = str(img_str, "utf-8")
    return img_str


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_game_configs', methods=['GET'])
def get_game_configs():
    
    def search_for_config(config_dir, result):
        gamesizes = [d for d in sorted(os.listdir(config_dir)) if os.path.isdir(
           os.path.join(config_dir, d))]
        if len(gamesizes) == 0 and len(os.listdir(config_dir)) > 0:
            gamesizes = ['custom']  

        for gamesize in gamesizes:
            configs = sorted(os.listdir(os.path.join(config_dir, gamesize)))
            if len(configs) > 0:
                tmp = []
                for config in configs:
                   tmp.append({
                       'name': config.split('.')[0],
                       'filepath': os.path.join(config_dir, gamesize, config)
                       })
            result.append({
                    "size": gamesize,
                    "configs": tmp
                    })

    config_files = []

    search_for_config(config_filepath, config_files)

    # Search for additional user config
    if os.path.exists(additional_config_files):
        search_for_config(additional_config_files, config_files)

    return jsonify(config_files)

@app.route('/get_config_json', methods = ['POST'])
def get_config_json():
    config_path = request.json['configPath']

    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r') as f:
                configData = json.load(f)
            return jsonify(configData)
        except:
            raise ValueError('Error loading config file')
    else:
        return("No config file found")   

@app.route('/get_agents', methods =['GET'])
def get_agents():
    agents = []
    if not os.path.exists(trained_agents_filepath):
        os.makedirs(trained_agents_filepath)

    # Search for trained agents in the trained agents driectory
    agent_files = []
    for folder, subs, files in os.walk(trained_agents_filepath):
        agent_files.append(str(folder))
    for agent in agent_files:
        #Each agent is a folder. 
        metadata_file = os.path.join(agent, 'metadata.json')
        if os.path.isfile(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    agent_metadata = json.load(f)
                    
                    agent_name = os.path.basename(agent)
                    logger.info("Metadata file found for agent in: "+ agent)
                    logger.info("Agentname: "+ agent_name)
                    agents.append({
                        "name": agent_name,
                        "agent_type" : agent_metadata['agentplayer'],
                        "filepath" : agent 
                    })
            except:
                raise ValueError('Error loading agent metadata file : ', metadata_file)
        else:
            logger.info("No metadata file found for agent in: "+ agent)

    # Search for basic agents in the basic agents directory
    search_for_agents(basic_agents_filepath, agents)

    # Search for additional user basic agents in the additional_basic_agents
    if os.path.exists(additional_basic_agents):
        search_for_agents(additional_basic_agents, agents)
                                            
    return jsonify(agents)

@app.route('/get_agent_json', methods = ['POST'])
def get_agent_json():
    filepath = request.json['filepath']
    meta_filepath = os.path.join(filepath, 'metadata.json')
    logger.info("Laoding metadata from: "+ meta_filepath)
    if os.path.isfile(meta_filepath):
        try:
            with open(meta_filepath, 'r') as f:
                metaData = json.load(f)
            return jsonify(metaData)
        except:
            raise ValueError('Error loading metadata')
    else:
        return jsonify("No metadata found")
        
@app.route('/new_game', methods=['POST'])
def new_game():
    env.stopAllGames()
    kwargs = dict(request.json['settings']['kwargs'])
    try:
        config_file_path = request.json['settings']['config_file_path']
    except:
        config_file_path = None
 
    if config_file_path:
        env.createNewGame(config_file_path=config_file_path, **kwargs)
    else:
        env.createNewGame(**kwargs)
 
    view = env.activeGames[len(env.activeGames)-1].gamePlayerTurn
    pil_image = env.activeGames[len(env.activeGames)-1].render(web_ui_render_width,web_ui_render_height,view)
    return serve_pil_image(pil_image)  

@app.route('/reset_game', methods=['POST'])
def reset_game():
    env.activeGames[len(env.activeGames)-1].reset_game()
 
    view = env.activeGames[len(env.activeGames)-1].gamePlayerTurn
    pil_image = env.activeGames[len(env.activeGames)-1].render(web_ui_render_width,web_ui_render_height,view)
    return serve_pil_image(pil_image)  

@app.route('/make_video', methods=['POST'])
def make_video():

    kwargs = dict(request.json['settings']['kwargs'])
    try:
        config_file_path = request.json['settings']['config_file_path']
    except:
        config_file_path = None

    pelican_agent_filepath = kwargs.get('pelican_agent_filepath', None)
    pelican_agent_name = kwargs.get('pelican_agent_name', None)
    panther_agent_filepath = kwargs.get('panther_agent_filepath', None)
    panther_agent_name = kwargs.get('panther_agent_name', None) 
    


    if config_file_path:
        file_name, result_json, _ = helper.load_driving_agent_make_video(pelican_agent_filepath, pelican_agent_name, panther_agent_filepath, panther_agent_name, config_file_path,video_path='/Components/plark_ai_flask/builtangularSite/dist/assets/videos', basic_agents_filepath=basic_agents_filepath, renderWidth= web_ui_render_width, renderHeight=web_ui_render_height)
    else:
        file_name, result_json, _ = helper.load_driving_agent_make_video(pelican_agent_filepath, pelican_agent_name, panther_agent_filepath, panther_agent_name,video_path='/Components/plark_ai_flask/builtangularSite/dist/assets/videos',basic_agents_filepath=basic_agents_filepath, renderWidth= web_ui_render_width, renderHeight=web_ui_render_height)
   
 
    return_video = '/assets/videos/' + file_name

    return {'videoURL': return_video,'gameState': result_json}


@app.route('/game_step', methods=['POST'])
def game_step():
    action = request.json['action']
    gameState,uioutput = env.activeGames[len(env.activeGames)-1].game_step(action)
    view = env.activeGames[len(env.activeGames)-1].gamePlayerTurn
    pil_image = env.activeGames[len(env.activeGames)-1].render(web_ui_render_width,web_ui_render_height,view)

    if gameState == 'Running':
        return serve_pil_image(pil_image)

    else:
        return {
            "gameState": gameState,
            "image": encode_pil_image(pil_image)
        }

@app.route('/output_view', methods=['POST'])  
def update_output_view():
    new_view = request.json['view']
    env.activeGames[len(env.activeGames)-1].outputView = new_view
    view = env.activeGames[len(env.activeGames)-1].gamePlayerTurn
    pil_image = env.activeGames[len(env.activeGames)-1].render(web_ui_render_width,web_ui_render_height,view)

    return serve_pil_image(pil_image)

def search_for_agents(agent_dir, results):
    for agent in os.listdir(agent_dir):
        if os.path.splitext(agent)[1] == ".py":
            # look only in the modpath directory when importing
            oldpath, sys.path[:] = sys.path[:], [agent_dir]

            try:
                module = __import__(agent[:-3])

            except ImportError as err:
                raise ValueError("Couldn't import", agent, ' - ', err )
                continue
            finally:    # always restore the real path
                sys.path[:] = oldpath

            for attr in dir(module):
                cls = getattr(module, attr)

                if isinstance(cls, type) and ( (issubclass(cls, classes.Panther_Agent) and cls!= classes.Panther_Agent ) or (issubclass(cls, classes.Pelican_Agent)and cls!= classes.Pelican_Agent ) and "plark_game" not in str(cls) ) :
                    instance = cls()
                    logger.info(cls)
                    agent_type = ""
                    if issubclass(cls, classes.Panther_Agent):
                        agent_type = 'panther'
                    elif issubclass(cls, classes.Pelican_Agent):
                        agent_type = 'pelican'

                    if attr not in ["Panther_Agent", "Pelican_Agent"]:
                        results.append({
                                "name": attr,
                                "agent_type" : agent_type,
                                "filepath" : os.path.join(agent_dir, agent)
                            })
                        
