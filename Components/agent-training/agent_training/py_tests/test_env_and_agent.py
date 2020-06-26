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

from plark_game import classes
from gym_plark.envs import plark_env,plark_env_guided_reward,plark_env_top_left, plark_env_non_image_state


from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv
from gym import spaces

from .. import helper 
import datetime
import os
import gym_plark
import signal
import gym

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)



def test_base_env():
    # env = plark_env.PlarkEnv()
    env = gym.make('plark-env-v0')
    check_env(env)

def test_base_env_reward():
    # env = plark_env.PlarkEnv(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0')
    env.reset()
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #plant sonobuoy
    obs, reward, done, info = env.step(6)
    assert reward == env.buoy_far_apart_reward
    #illegal plant sonobuoy
    obs, reward, done, info = env.step(6)
    assert reward == env.illegal_move_reward
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #too close plant sonobuoy
    obs, reward, done, info = env.step(6)
    assert reward == env.buoy_too_close_reward
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #move no reward
    obs, reward, done, info = env.step(3)
    assert reward == 0
    #plant sonobuoy
    obs, reward, done, info = env.step(6)
    assert reward == env.buoy_far_apart_reward

def test_guided_env():
    # env = plark_env_guided_reward.PlarkEnvGuidedReward()
    env = gym.make('plark-env-guided-reward-v0')
    check_env(env)
    
    assert "PlarkEnvGuidedReward" in str(type(env))
    


def test_env_and_agent():
    # env = plark_env.PlarkEnv(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0')
    check_env(env)
    
    training_steps = 10
    model = PPO2('CnnPolicy', env)
    model.learn(training_steps)

    n_eval_episodes = 2
    mean_reward, n_steps, victories = helper.evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)
    
    assert "PlarkEnv" in str(type(env))
    assert "PPO2" in str(type(model))
    
def test_video_of_agents_manual():
    video_path = '/data/test_video/'
    os.makedirs(video_path, exist_ok=True)
    video_file_path =  os.path.join(video_path, 'test_self_play.mp4') 
    panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/'

    # pelican_env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    pelican_env = gym.make('plark-env-v0', driving_agent='pelican',panther_agent_filepath=panther_agent_filepath)
    
    pelican_load_path = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_pelican/PPO2_20200325_184254_pelican.zip'
    pelican_model = PPO2.load(pelican_load_path)

    basewidth,hsize = helper.make_video(pelican_model,pelican_env,video_file_path)

def test_video_of_agents():
    video_path = '/data/test_video/'
    os.makedirs(video_path, exist_ok=True)
    pelican_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_pelican/'
    pelican_agent_name = ''
    panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/'
    panther_agent_name = ''
    helper.load_driving_agent_make_video(pelican_agent_filepath, pelican_agent_name, panther_agent_filepath, panther_agent_name, config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',video_path=video_path)

def test_env_and_pre_trained_agent():
    panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/' #This model is in minio or the package.
    # env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0', driving_agent='pelican',panther_agent_filepath=panther_agent_filepath)       
    check_env(env)
    
    training_steps = 500
    model = PPO2('CnnPolicy', env)
    model.learn(training_steps)

    n_eval_episodes = 2
    mean_reward, n_steps, victories = helper.evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=False)

def test_env_result():
    panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/' #This model is in minio or the package.
    # env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0', driving_agent='pelican',panther_agent_filepath=panther_agent_filepath)    
    check_env(env)

    training_steps = 500
    model = PPO2('CnnPolicy', env)
    model.learn(training_steps)

    n_eval_episodes = 5
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        victory = False
        while not done:
            action, state = model.predict(obs, state=state, deterministic=False)
            obs, reward, done, _info = env.step(action)
            if done:
                assert 'result' in _info, "Info should contain result when game is done"
                assert _info['result'] in ["WIN", "LOSE"], "result should be WIN or LOSE"

def test_illegal_move_limit_driving_pelican():
    panther_agent_filepath = '/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py' #This model is in minio or the package.
    # env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath, panther_agent_name='Panther_Agent_Move_North',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0', driving_agent='pelican',panther_agent_filepath=panther_agent_filepath, panther_agent_name='Panther_Agent_Move_North')    
    check_env(env)
    env.reset()
    # Repeat illegal move (illegal move limit - 1) times
    for i in range(9):
        obs, reward, done, info = env.step(0)
        assert info['illegal_move'] == True, "Should have made illegal move"
        assert info['turn'] == 0, "Should still be on first turn"
    # Next illegal move should end turn    
    obs, reward, done, info = env.step(0)
    assert info['illegal_move'] == True
    assert info['turn'] == 1

def test_illegal_move_limit_driving_panther():
    pelican_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_pelican/' #This model is in minio or the package.
    # env = plark_env.PlarkEnv(driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    env = gym.make('plark-env-v0', driving_agent='panther',pelican_agent_filepath=pelican_agent_filepath)  
    check_env(env)
    env.reset()
    # Repeat illegal move (illegal move limit - 1) times
    for i in range(9):
        obs, reward, done, info = env.step(3)
        assert info['illegal_move'] == True, "Should have made illegal move"
        assert info['turn'] == 0, "Should still be on first turn"
    # Next illegal move should end turn    
    obs, reward, done, info = env.step(0)
    assert info['illegal_move'] == False
    assert info['turn'] == 1

def test_illegal_move_limit_non_driving_pelican():
    def handler(signum, frame):
        raise TimeoutError("Timed out after 30 seconds. This probably means an infinite loop of illegal moves was allowed")

    # Raise an exception if this method gets stuck
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    
    try:
        # env = plark_env.PlarkEnv(driving_agent='panther',pelican_agent_filepath='/Components/plark-game/plark_game/agents/basic/PelicanAgentIllegalMove.py', pelican_agent_name='PelicanAgentIllegalMove',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced_panther_multi_move.json')
        env = gym.make('plark-env-v0', driving_agent='panther',pelican_agent_filepath='/Components/plark-game/plark_game/agents/basic/PelicanAgentIllegalMove.py', pelican_agent_name='PelicanAgentIllegalMove',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced_panther_multi_move.json')  
        check_env(env)
        env.reset()
        game = env.env.activeGames[-1]
        pelicanAgent = game.pelicanAgent
        pelicanAgent.reset_moves_taken()

        assert game.pelicanPlayer.row == 0, "Pelican should start at the top of the map"

        assert pelicanAgent.moves_taken == 0, "Pelican should not have taken any moves before start of game"

        for turn in [0, 1]:
            # Make moves until turn is about to end
            for move in range(4):
                # Alternately move up/down
                action = 0 if move % 2 == 0 else 3
                obs, reward, done, info = env.step(action)
                assert info['turn'] == turn, "Should still be on turn {}".format(turn)
                assert game.illegal_pelican_move == True, "Pelican should have made an illegal move"
                assert pelicanAgent.moves_taken == (turn+1)*game.max_illegal_moves_per_turn, "Pelican should have exhausted illegal moves for this turn"
                assert game.pelicanPlayer.row == 0, "Pelican should remain at the top of the map"
            
            # Next move should end turn
            obs, reward, done, info = env.step(0)
            assert info['turn'] == turn + 1, "Turn should have ended"
            assert pelicanAgent.moves_taken == (turn+1)*game.max_illegal_moves_per_turn, "pelican should have exhausted illegal moves this turn"
            assert game.pelicanPlayer.row == 0, "Pelican should remain at the top of the map"
    finally:
        # Cancel timer if test has finished executing (successful or not)
        signal.alarm(0)

def test_illegal_move_limit_non_driving_panther():
    def handler(signum, frame):
        raise TimeoutError("Timed out after 30 seconds. This probably means an infinite loop of illegal moves was allowed")

    # Raise an exception if this method gets stuck
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)

    try:
        # env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath='/Components/plark-game/plark_game/agents/basic/PantherAgentIllegalMove.py', panther_agent_name='PantherAgentIllegalMove',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
        env = gym.make('plark-env-v0',driving_agent='pelican',panther_agent_filepath='/Components/plark-game/plark_game/agents/basic/PantherAgentIllegalMove.py', panther_agent_name='PantherAgentIllegalMove')
        check_env(env)
        env.reset()
        game = env.env.activeGames[-1]
        pantherAgent = game.pantherAgent
        pantherAgent.reset_moves_taken()

        assert game.pantherPlayer.row == 9, "Panther should start at the bottom of the map"

        for turn in [0, 1]:
            # Make moves until turn is about to end
            for move in range(9):
                # Alternately move down/up
                action = 3 if move % 2 == 0 else 0
                obs, reward, done, info = env.step(action)
                assert info['turn'] == turn, "Should still be on turn {}".format(turn)
                assert pantherAgent.moves_taken == turn*game.max_illegal_moves_per_turn, "Panther should not have taken any moves yet this turn"
                assert game.pantherPlayer.row == 9, "Panther should remain at the bottom of the map"
            
            # Next move should end turn
            obs, reward, done, info = env.step(0)
            assert info['turn'] == turn + 1, "Turn should have ended"
            assert game.illegal_panther_move == True, "Panther should have made an illegal move"
            assert pantherAgent.moves_taken == (turn+1)*game.max_illegal_moves_per_turn, "panther should have exhausted illegal moves this turn"
            assert game.pantherPlayer.row == 9, "Panther should remain at the bottom of the map"
    finally:
        # Cancel timer if test has finished executing (successful or not)
        signal.alarm(0)

def test_non_image_env():
    env = plark_env_non_image_state.PlarkEnvNonImageState(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json', driving_agent='pelican')
    observation_space = env.observation_space
    observation_space_size =  observation_space.shape[0]
    
    obs = env.reset()
    actual_observation_space_size = len(obs)
    assert observation_space_size == actual_observation_space_size

