import requests
from io import BytesIO
import PIL.Image
from IPython.display import display,clear_output,HTML
from IPython.display import Image as DisplayImage
import base64
import json
from io import StringIO
import ipywidgets as widgets
import sys
from plark_game import classes
import time
import imageio
import numpy as np
import matplotlib.pyplot as plt
import io
import os, sys

from stable_baselines.common.env_checker import check_env
from stable_baselines.common.evaluation import evaluate_policy
from gym_plark.envs import plark_env,plark_env_guided_reward,plark_env_top_left

import datetime
basepath = '/data/agents/models'
from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv
import helper

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

display(HTML(data="""
<style>
    div#notebook-container    { width: 95%; }
    div#menubar-container     { width: 65%; }
    div#maintoolbar-container { width: 99%; }
</style>
"""))

env = plark_env_guided_reward.PlarkEnvGuidedReward()


# It will check your custom environment and output additional warnings if needed
check_env(env)

## Define the player type we are training.
modelplayer = "PELICAN"
## Define the type of RL algorithm you are using.
modeltype = "DQN"
## Specify the date and time for this training.
basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
## location where models will be saved

# Instantiate the env
env = plark_env_guided_reward.PlarkEnvGuidedReward()

model = DQN('CnnPolicy', env)
#model = A2C('CnnPolicy', env)
model.learn(50)

retrain_iter = []
retrain_values = []

logger.info('****** STARTING EVALUATION *******')

mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
retrain_iter.append(str(0))
retrain_values.append(mean_reward)

def save():
    logger.info(str(retrain_iter))
    logger.info(str(retrain_values))
    
    plt.figure(figsize=(9, 3))
    plt.subplot(131)
    plt.bar(retrain_iter, retrain_values)
    plt.subplot(132)
    plt.scatter(retrain_iter, retrain_values)
    plt.subplot(133)
    plt.plot(retrain_iter, retrain_values)
    plt.suptitle('Retraining Progress')
    image_based = False 
    model_path,model_dir, modellabel = helper.save_model_with_env_settings(basepath,model,modeltype,env,image_based,basicdate)
    fig_path = os.path.join(model_dir, 'Training_Progress.png')
    plt.savefig(fig_path)
    print('Model saved to ', model_path)


def retrain(mean_reward, target_reward, count):
    if mean_reward < target_reward:
        count = count + 1
        retrain_iter.append(str(count))
        
        model.learn(50)
        
        mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
        retrain_values.append(mean_reward)
        
        if mean_reward >= target_reward:
            save()
        if mean_reward < target_reward:
            retrain(mean_reward, target_reward, count)

    logger.info('Model Training Reached Target Level')

retrain(mean_reward, 2, 1)
