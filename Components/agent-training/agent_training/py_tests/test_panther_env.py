import requests
from io import BytesIO
import PIL.Image
import base64
import json
from io import StringIO

import sys
import time
import imageio
import numpy as np
import io

from stable_baselines.common.env_checker import check_env
from stable_baselines.common.evaluation import evaluate_policy

from plark_game import classes
from gym_plark.envs import panther_env_reach_top
import gym


from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv

from tensorboardX import SummaryWriter

from .. import helper
import datetime
import os

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_running_pather():
    # Create an istance of panther env reach top for testing
    # env = panther_env_reach_top.PantherEnvReachTop(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('panther-env-reach-top-v0')
    model = PPO2('CnnPolicy', env)

    assert "panther_env_reach_top" in str(type(env))
    assert "PPO2" in str(type(model))
    assert len(env.action_index) == 7

def test_reward_score_odd_col():
    """
        This test requires the reward function in the panther_env_reach_top to be
        +0.5 for moving up the board
        -0.2 for moving down the board
    """

    # Create an istance of panther env reach top for testing
    # env = panther_env_reach_top.PantherEnvReachTop(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',panther_start_col=5)
    env = gym.make('panther-env-reach-top-v0', panther_start_col=5)

    model = PPO2('CnnPolicy', env)

    # Manually move the panther up and down and check that it gets the correct reward score
    # Move the panther up
    obs, reward, done, info = env.step(0)
    assert reward == 0.5
    # Move the panther up and right
    obs, reward, done, info = env.step(1)
    assert reward == 0.5
    # Move the panther down and right
    obs, reward, done, info = env.step(2)
    assert reward == -0.2
    # Move the panther down
    obs, reward, done, info = env.step(3)
    assert reward == -0.2
    # Move the panther down and left
    obs, reward, done, info = env.step(4)
    assert reward == -0.2
    # Move the panther up and left
    obs, reward, done, info = env.step(5)
    assert reward == 0.5

def test_reward_score_even_col():
    # Create an istance of panther env reach top for testing
    # env = panther_env_reach_top.PantherEnvReachTop(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json', panther_start_col=6)
    env = gym.make('panther-env-reach-top-v0', panther_start_col=6)
    model = PPO2('CnnPolicy', env)

    # Manually move the panther up and down and check that it gets the correct reward score
    # Move the panther up
    obs, reward, done, info = env.step(0)
    assert reward == 0.5
    # Move the panther up and right
    obs, reward, done, info = env.step(1)
    assert reward == 0.5
    # Move the panther down and right
    obs, reward, done, info = env.step(2)
    assert reward == -0.2
    # Move the panther down
    obs, reward, done, info = env.step(3)
    assert reward == -0.2
    # Move the panther down and left
    obs, reward, done, info = env.step(4)
    assert reward == -0.2
    # Move the panther up and left
    obs, reward, done, info = env.step(5)
    assert reward == 0.5



