import PIL.Image
from IPython.display import display,clear_output,HTML
from IPython.display import Image as DisplayImage
import base64
import json
from io import StringIO
import ipywidgets as widgets
import sys
import time
import datetime
import imageio
import numpy as np
import io
import os
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.vec_env import SubprocVecEnv
from plark_game import classes
#from gym_plark.envs import plark_env,plark_env_guided_reward,plark_env_top_left
from gym_plark.envs.plark_env_sparse import PlarkEnvSparse
from gym_plark.envs.plark_env import PlarkEnv
import datetime

from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv

from tensorboardX import SummaryWriter


import helper 

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_agent(exp_path,model,env,testing_interval,max_steps,model_type,basicdate,tb_writer,tb_log_name,early_stopping=True, previous_steps=0):
    steps = 0
    logger.info("Beginning training for {} steps".format(max_steps))
    model.set_env(env)
    
    while steps < max_steps:
        logger.info("Training for {} steps".format(testing_interval))
        model.learn(testing_interval)    
        steps = steps + testing_interval
        agent_filepath,_,_=   helper.save_model_with_env_settings(exp_path,model,model_type,env,basicdate)
        if early_stopping:
            victory_count, avg_reward = helper.check_victory(model,env,trials = 10)
            if tb_writer is not None and tb_log_name is not None:
                tb_steps = steps+previous_steps
                logger.info("Writing to tensorboard for {} after {} steps".format(tb_log_name, tb_steps))
                tb_writer.add_scalar('{}_avg_reward'.format(tb_log_name), avg_reward, tb_steps)
                tb_writer.add_scalar('{}_victory_count'.format(tb_log_name), victory_count, tb_steps)
            if victory_count > 7:
                logger.info("Stopping training early")
                break #Stopping training as winning
    #Save agent
    logger.info('steps = '+ str(steps))    
    agent_filepath,_,_=   helper.save_model_with_env_settings(exp_path,model,model_type,env,basicdate)
    agent_filepath = os.path.dirname(agent_filepath)
    return agent_filepath,steps

def run_self_play(exp_name,exp_path,basicdate,
                    pelican_testing_interval=100,pelican_max_initial_learning_steps=10000,
                    panther_testing_interval=100,panther_max_initial_learning_steps=10000,
                    self_play_testing_interval=100,self_play_max_learning_steps_per_agent=10000,self_play_iterations=10000,
                    model_type='PPO2',log_to_tb=False,image_based=True,num_parallel_envs=1):
    pelican_training_steps = 0
    panther_training_steps = 0
    
    
    pelican_model_type = model_type
    panther_model_type = model_type

    if log_to_tb:
        writer = SummaryWriter(exp_path)
        pelican_tb_log_name = 'pelican'
        panther_tb_log_name = 'panther'
    else:
        writer = None
        pelican_tb_log_name = None
        panther_tb_log_name = None    
            
    policy = 'CnnPolicy'
    if image_based is False:
        policy = 'MlpPolicy'

    parallel = False
    if model_type.lower() == 'ppo2':
        parallel = True
    #Train initial pelican vs rule based panther
    
    if parallel:
        pelican_env = SubprocVecEnv([lambda:PlarkEnv(driving_agent='pelican',config_file_path='/Components/plark-game/plark_game/game_config/10x10/pelican_easy.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3) for _ in range(num_parallel_envs)])
    else:
        pelican_env = PlarkEnv(driving_agent='pelican',config_file_path='/Components/plark-game/plark_game/game_config/10x10/pelican_easy.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3)
    
    pelican_model = helper.make_new_model(model_type,policy, pelican_env)
    logger.info('Training initial pelican')
    pelican_agent_filepath, steps = train_agent(exp_path,pelican_model,pelican_env,pelican_testing_interval,pelican_max_initial_learning_steps,pelican_model_type,basicdate,writer,pelican_tb_log_name)
    pelican_training_steps = pelican_training_steps + steps

    # Train initial panther agent vs initial pelican agent
    if parallel:
        panther_env = SubprocVecEnv([lambda:PlarkEnv(driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3) for _ in range(num_parallel_envs)])
    else:
        panther_env = PlarkEnv(driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3)
    panther_model = helper.make_new_model(model_type,policy, panther_env)        
    logger.info('Training initial panther')
    panther_agent_filepath, steps = train_agent(exp_path,panther_model,panther_env,panther_testing_interval,panther_max_initial_learning_steps,panther_model_type,basicdate,writer,panther_tb_log_name)
    panther_training_steps = panther_training_steps + steps

    # Train agent vs agent
    logger.info('Self play')
    
    for i in range(self_play_iterations):
        logger.info('Self play iteration '+str(i)+' of '+str(self_play_iterations))
        logger.info('Training pelican')
        if parallel:
            pelican_env = SubprocVecEnv([lambda:PlarkEnvSparse(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3) for _ in range(num_parallel_envs)])
        else:
            pelican_env = PlarkEnvSparse(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3)
        
        pelican_agent_filepath, steps = train_agent(exp_path,pelican_model,pelican_env,self_play_testing_interval,self_play_max_learning_steps_per_agent,pelican_model_type,basicdate,writer,pelican_tb_log_name, previous_steps=pelican_training_steps)
        pelican_training_steps = pelican_training_steps + steps

        logger.info('Training panther')
        if parallel:
            panther_env = SubprocVecEnv([lambda:PlarkEnvSparse(driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3) for _ in range(num_parallel_envs)])
        else:
            panther_env = PlarkEnvSparse(driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',image_based=image_based,random_panther_start_position=True,max_illegal_moves_per_turn=3)
        
        panther_agent_filepath, steps = train_agent(exp_path,panther_model,panther_env,self_play_testing_interval,self_play_max_learning_steps_per_agent,panther_model_type,basicdate,writer,panther_tb_log_name, previous_steps=panther_training_steps)    
        panther_training_steps = panther_training_steps + steps

    logger.info('Training pelican total steps:'+str(pelican_training_steps))
    logger.info('Training panther total steps:'+str(panther_training_steps))
    # Make video 
    video_path =  os.path.join(exp_path, 'test_self_play.mp4') 
    basewidth,hsize = helper.make_video(pelican_model,pelican_env,video_path)
    return video_path, basewidth, hsize

if __name__ == '__main__':
    basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    basepath = '/data/agents/models'
    exp_name = 'test_' + basicdate
    exp_path = os.path.join(basepath, exp_name)

    logger.info(exp_path)

    # run_self_play(exp_name,exp_path,basicdate)
    run_self_play(exp_name,exp_path,basicdate,
                    pelican_testing_interval=1000,pelican_max_initial_learning_steps=50000,
                    panther_testing_interval=1000,panther_max_initial_learning_steps=50000,
                    self_play_testing_interval=1000,self_play_max_learning_steps_per_agent=50000,self_play_iterations=200,
                    model_type='PPO2',log_to_tb=True,image_based=False)
    # python sefl_play.py 