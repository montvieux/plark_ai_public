import requests
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.evaluation import evaluate_policy
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
import helper
import logging
from gym_plark.envs import plark_env,plark_env_guided_reward,plark_env_top_left
import datetime
from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv
%matplotlib inline
%load_ext autoreload
%autoreload 2

display(HTML(data="""
<style>
    div#notebook-container    { width: 95%; }
    div#menubar-container     { width: 65%; }
    div#maintoolbar-container { width: 99%; }
</style>
"""))

def retrain(mean_reward, target_reward, count, env, model):
    if mean_reward < target_reward:
        count = count + 1
        model.learn(50)
        mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
        if mean_reward < target_reward:
            retrain(mean_reward, target_reward, count, env, model)

    return True

if __name__ == "__main__":
    
    ## The basepath of where the models are to be stored.
    basepath = '/data/agents/models'

    ## Define the game configuration file names to be used in the multi-stage training approach.
    very_easy_config = "/Components/plark-game/plark_game/game_config/10x10/pelican_very_easy.json"
    easy_config = "/Components/plark-game/plark_game/game_config/10x10/pelican_easy.json"
    medium_config = "/Components/plark-game/plark_game/game_config/10x10/pelican_medium.json"

    ## Define the logging level
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    ## Define the player type we are training.
    modelplayer = "PELICAN"
    
    ## Define the type of RL algorithm you are using.
    modeltype = "DQN"
    
    ## Used the format to get date
    basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    ## Stage thresholds these are based on mean reward values which are calculated when evaluating the module
    ## These will be switched out if using a custom evaluation process.
    stage_one_threshold = 5
    stage_two_threshold = 7
    stage_three_threshold = 10

    print("Stage 1 Training Started")
    env = plark_env_guided_reward.PlarkEnvGuidedReward(config_file_path=very_easy_config)
    model = DQN('CnnPolicy', env)
    model.learn(50)
    logger.info('STARTING STAGE 1 INITIAL EVALUATION')
    stg1_mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
    logger.info('FINISHING STAGE 1 INITIAL EVALUATION')
    stage1result = retrain(stg1_mean_reward, stage_one_threshold, 0 ,env, model)
    logger.info("Stage One Threshold Met")
    if stage1result == True:
        logger.info("Stage 2 Training Started")
        env = plark_env_guided_reward.PlarkEnvGuidedReward(config_file_path=easy_config)
        model.set_env(env)
        model.learn(50)
        logger.info('STARTING STAGE 2 INITIAL EVALUATION')
        stg2_mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
        logger.info('FINISHING STAGE 2 INITIAL EVALUATION')
        stage2result = retrain(stg2_mean_reward, stage_two_threshold, 0 ,env, model)
        logger.info("Stage Two Threshold Met")
        if stage2result == True:
            logger.info("Stage 3 Training Started")
            env = plark_env_guided_reward.PlarkEnvGuidedReward(config_file_path=medium_config)
            model.set_env(env)
            model.learn(50)
            logger.info('STARTING STAGE 3 EVALUATION')
            stg3_mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=1, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
            logger.info('FINISHED STAGE 3 EVALUATION')
            stage3result = retrain(stg3_mean_reward, stage_three_threshold, 0 ,env, model)
            if stage3result == True:
                logger.info("Stage Three Threshold Met")
                logger.info("Multi-Stage-Training-Complete")
    model_path,model_dir, modellabel = helper.save_model_with_env_settings(basepath,model,modeltype,env,basicdate)
