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
import time
import imageio
import numpy as np
import io

from stable_baselines.common.env_checker import check_env
from stable_baselines.common.evaluation import evaluate_policy

from plark_game import classes
from gym_plark.envs import panther_env_reach_top


from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv

from tensorboardX import SummaryWriter

import helper
import datetime
import os

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#################
## Train Agent ##
#################
def train_agent(exp_path,
                model,
                env,
                testing_interval,
                max_steps,
                model_type,
                basicdate,
                tb_writer,
                tb_log_name,
                reward_margin,
                early_stopping=True, 
                previous_steps=0,
                n_eval_episodes=5
                ):
    steps = 0
    model.set_env(env)
    logger.info("Beginning training for {} steps".format(max_steps))

    best_avg_reward = None

    while steps < max_steps:
        logger.info("Training for {} steps".format(testing_interval))
        model.learn(testing_interval)    
        steps = steps + testing_interval
        avg_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)

        if best_avg_reward is None:
            best_avg_reward = avg_reward
            save_model(exp_path, model, model_type, env, basicdate)

        logger.info('avg_reward = '+ str(avg_reward))    
        logger.info('best_avg_reward = '+ str(best_avg_reward))   

        if tb_writer is not None and tb_log_name is not None:
            tb_steps = steps+previous_steps
            logger.info("Writing to tensorboard for {} after {} steps".format(tb_log_name, tb_steps))
            tb_writer.add_scalar('{}_avg_reward'.format(tb_log_name), avg_reward, tb_steps)
            tb_writer.add_scalar('{}_best_avg_reward'.format(tb_log_name), best_avg_reward, tb_steps)

        if avg_reward > best_avg_reward :
            best_avg_reward = avg_reward
            save_model(exp_path, model, model_type, env, basicdate)

##################
## Save Model   ##
## Create Video ##
##################
def save_model(exp_path, model, model_type, env, basicdate):
    logger.info("Saving model")

    # helper.save_model(exp_path, model, model_type, env.driving_agent, env.render_height, env.render_width, basicdate)
    helper.save_model_with_env_settings(exp_path,model,model_type,env,basicdate)

    video_path = os.path.join(exp_path, 'training.mp4')
    helper.make_video(model,env,video_path)

##################
## Run Training ##
##################
def run_panther_training(
                    exp_name,exp_path,
                    basicdate,
                    model_type='PPO2',
                    n_eval_episodes=10,
                    training_intervals=100,
                    max_steps=10000,
                    reward_margin=10,
                    log_to_tb=False):

    # set up logging 
    if log_to_tb:
        writer = SummaryWriter(exp_path)
        tb_log_name = 'panther_training'
    else:
        writer = None
        tb_log_name = None

    # Instantiate the env and model
    env = panther_env_reach_top.PantherEnvReachTop(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    model = PPO2('CnnPolicy', env)

    # Start training 
    train_agent(exp_path,model,env,training_intervals,max_steps,model_type,basicdate,writer,tb_log_name,reward_margin)
                
    # Evaluate
    mean_reward, n_steps = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
    logger.info('Evaluation finished')
    logger.info('Mean Reward is ' + str(mean_reward))
    logger.info('Number of steps is ' + str(n_steps))

#####################
## If Name == Main ##
#####################
if __name__ == '__main__':
    basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    basepath = '/data/agents/models'
    exp_name = 'test_' + basicdate
    exp_path = os.path.join(basepath, exp_name)

    logger.info(exp_path)

    run_panther_training(exp_name,exp_path,basicdate,model_type='PPO2',n_eval_episodes=10,training_intervals=100,max_steps=1000,log_to_tb=True,reward_margin=25)
