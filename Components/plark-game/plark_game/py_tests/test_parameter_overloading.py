from ..classes import *
import sys
import os
import gym
from plark_game import classes
import gym_plark

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

#
# Game settings tests
#

def test_class_env_parameter_overload_maximum_turns():
    # Overloads the maximum turn count of the game, this is seperate from the bingo state value. 

    maximum_turns = 1 
    kwargs = {
                'maximum_turns': maximum_turns
    }

    env = Environment()
    env.createNewGame(**kwargs)
    
    game = env.activeGames[len(env.activeGames)-1]
    assert game.maxTurns == maximum_turns

def test_gym_env_parameter_overload_maximum_turns():
    # Overloads the maximum turn count of the game, this is seperate from the bingo state value. 

    maximum_turns = 1 
    kwargs = {
                'maximum_turns': maximum_turns
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.maxTurns == maximum_turns


def test_class_env_parameter_overload_map_width():
    # Overloads the map width, the starting location of the pelican and panther need to be within the available width
    # for this test to pass

    map_width = 2 
    kwargs = {
                'map_width': map_width,
                'panther_start_col': 0,
                'panther_start_row': 0,
                'pelican_start_col': 0,
                'pelican_start_row': 0
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.map_width == map_width


def test_gym_env_parameter_overload_map_width():
    # Overloads the map width, the starting location of the pelican and panther need to be within the available width
    # for this test to pass

    map_width = 2 
    kwargs = {
                'map_width': map_width,
                'panther_start_col': 0,
                'panther_start_row': 0,
                'pelican_start_col': 0,
                'pelican_start_row': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.map_width == map_width

def test_class_env_parameter_overload_map_height():
    # Overloads the map height, the starting loation of the pelican and panther need to be within the available width
    # for this test to pass

    map_height = 2 
    kwargs = {
                'map_height': map_height,
                'panther_start_col': 0,
                'panther_start_row': 0,
                'pelican_start_col': 0,
                'pelican_start_row': 0
    }


    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.map_height == map_height

def test_gym_env_parameter_overload_map_height():
    # Overloads the map height, the starting loation of the pelican and panther need to be within the available width
    # for this test to pass

    map_height = 2 
    kwargs = {
                'map_height': map_height,
                'panther_start_col': 0,
                'panther_start_row': 0,
                'pelican_start_col': 0,
                'pelican_start_row': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]

    assert game.map_height == map_height

def test_class_env_parameter_overload_driving_agent_panther():
    # this test overloads the driving agent to be panther, this test requires a pelican agent to be set
 
    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
    }


    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.driving_agent == 'panther'

def test_gym_env_parameter_overload_driving_agent_panther():
    # this test overloads the driving agent to be panther, this test requires a pelican agent to be set
 
    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]

    
    assert game.driving_agent == 'panther'

def test_class_env_parameter_overload_driving_agent_pelican():
    # this test overloads the driving agent to be pelican, this test requires a panther agent to be set

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
               
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.driving_agent == 'pelican'

def test_gym_class_parameter_overload_driving_agent_pelican():
    # this test overloads the driving agent to be pelican, this test requires a panther agent to be set

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
               
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]

    
    assert game.driving_agent == 'pelican'
   

# #
# # Render settings
# # 

def test_class_env_parameter_overload_render_hex_scale():
    # this test overloads the hex scale parameter.

    kwargs = {
                'hex_scale':10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.hexScale == 10

def test_gym_env_parameter_overload_render_hex_scale():
    # this test overloads the hex scale parameter.

    kwargs = {
                'hex_scale':10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.hexScale == 10

def test_class_envparameter_overload_render_output_view_all():
    # this test overloads the output_view_all parameter. This overrides the view state to allow 
    # for debugging, easier training and to view both agents for evaluation

    kwargs = {
                'output_view_all':False
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.output_view_all == False

def test_gym_env_parameter_overload_render_output_view_all():
    # this test overloads the output_view_all parameter. This overrides the view state to allow 
    # for debugging, easier training and to view both agents for evaluation

    kwargs = {
                'output_view_all':False
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.output_view_all == False
# #
# # Panther parameters tests
# #

def test_class_env_parameter_overload_panther_move_limit():
    # this test overloads the panther move limit, a pelican agent and panther move limit must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_move_limit': 0
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.panther_parameters['move_limit'] == 0

def test_gym_env_parameter_overload_panther_move_limit():
    # this test overloads the panther move limit, a pelican agent and panther move limit must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_move_limit': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.panther_parameters['move_limit'] == 0    

def test_class_env_parameter_overload_panther_start_col():
    # this test overloads the panther start col, a pelican agent and panther start col must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_start_col': 0
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pantherPlayer.col == 0

def test_gym_env_parameter_overload_panther_start_col():
    # this test overloads the panther start col, a pelican agent and panther start col must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_start_col': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pantherPlayer.col == 0    

def test_class_env_parameter_overload_panther_start_row():
    # this test overloads the panther start row, a pelican agent and panther start row must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_start_row': 0
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pantherPlayer.row == 0

def test_gym_env_parameter_overload_panther_start_row():
    # this test overloads the panther start row, a pelican agent and panther start row must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_start_row': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pantherPlayer.row == 0

def test_class_env_parameter_overload_panther_render_height():
    # this test overloads the panther render height, a pelican agent and panther render height must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_render_height': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert  game.panther_parameters['render_height'] == 10

def test_gym_env_parameter_overload_panther_render_height():
    # this test overloads the panther render height, a pelican agent and panther render height must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_render_height': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert  game.panther_parameters['render_height'] == 10

def test_class_envparameter_overload_panther_render_width():
    # this test overloads the panther render width, a pelican agent and panther render width must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_render_width': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert  game.panther_parameters['render_width'] == 10

def test_gym_env_parameter_overload_panther_render_width():
    # this test overloads the panther render width, a pelican agent and panther render width must be provided. 

    kwargs = {
                'driving_agent': 'panther',
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_render_width': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert  game.panther_parameters['render_width'] == 10

# #
# # Pelican paramater tests
# #

def test_class_env_parameter_overload_pelican_move_limit():
    # this test overloads the pelican move limit, a panther agent and pelican move limit must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_move_limit': 0
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pelican_parameters['move_limit'] == 0

def test_gym_env_parameter_overload_pelican_move_limit():
    # this test overloads the pelican move limit, a panther agent and pelican move limit must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_move_limit': 0
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pelican_parameters['move_limit'] == 0    

def test_class_env_parameter_overload_pelican_madman_range():
    # this test overloads the pelican madman sensor range, a panther agent and madman_range must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'madman_range': 5
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pelican_parameters['madman_range'] == 5

def test_gym_env_parameter_overload_pelican_madman_range():
    # this test overloads the pelican madman sensor range, a panther agent and madman_range must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'madman_range': 5
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pelican_parameters['madman_range'] == 5

def test_class_env_parameter_overload_pelican_default_torps():
    # this test overloads the pelicans default torpedos, a panther agent and default_torps must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'default_torps': 5
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pelican_parameters['default_torps'] == 5

def test_gym_env_parameter_overload_pelican_default_torps():
    # this test overloads the pelicans default torpedos, a panther agent and default_torps must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'default_torps': 5
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pelican_parameters['default_torps'] == 5

def test_class_env_parameter_overload_pelican_default_sonobuoys():
    # this test overloads the pelicans default sonobuoys, a panther agent and default_sonobuoys must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'default_sonobuoys': 2
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.pelican_parameters['default_sonobuoys'] == 2

def test_gym_env_parameter_overload_pelican_default_sonobuoys():
    # this test overloads the pelicans default sonobuoys, a panther agent and default_sonobuoys must be provided. 
    map_height = 2 
    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'default_sonobuoys': 2
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.pelican_parameters['default_sonobuoys'] == 2

def test_class_env_parameter_overload_pelican_render_height():
    # this test overloads the pelican render height, a panther agent and pelican render height must be provided. 

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_render_height': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert  game.pelican_parameters['render_height'] == 10

def test_gym_env_parameter_overload_pelican_render_height():
    # this test overloads the pelican render height, a panther agent and pelican render height must be provided. 

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_render_height': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert  game.pelican_parameters['render_height'] == 10

def test_class_env_parameter_overload_pelican_render_width():
    # this test overloads the pelican render width, a panther agent and pelican render width must be provided. 

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_render_width': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert  game.pelican_parameters['render_width'] == 10


def test_gym_env_parameter_overload_pelican_render_width():
    # this test overloads the pelican render width, a panther agent and pelican render width must be provided. 

    kwargs = {
                'driving_agent': 'pelican',
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'pelican_render_width': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert  game.pelican_parameters['render_width'] == 10
# #
# # Torpedo parameters test
# #

def test_class_env_parameter_overload_torpedos_turn_limit():
    # this test overloads the torpedo turn limit. 

    kwargs = {
                'torpedos_turn_limit': 5
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.torpedo_parameters['turn_limit'] == 5

def test_gym_env_parameter_overload_torpedos_turn_limit():
    # this test overloads the torpedo turn limit. 

    kwargs = {
                'torpedos_turn_limit': 5
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.torpedo_parameters['turn_limit'] == 5

def test_class_env_parameter_overload_torpedos_hunt():
    # this test overloads the torpedo turn parameter. 

    kwargs = {
                'torpedos_hunt': False
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.torpedo_parameters['hunt'] == False


def test_gym_env_parameter_overload_torpedos_hunt():
    # this test overloads the torpedo turn parameter. 

    kwargs = {
                'torpedos_hunt': False
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.torpedo_parameters['hunt'] == False

def test_class_env_parameter_overload_torpedos_speed():
    # this test overloads the torpedo speed parameter.

    kwargs = {
                'torpedos_speed': [1,1,1,1,1]
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.torpedo_parameters['speed'] == [1,1,1,1,1]

def test_gym_env_parameter_overload_torpedos_speed():
    # this test overloads the torpedo speed parameter.

    kwargs = {
                'torpedos_speed': [1,1,1,1,1]
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.torpedo_parameters['speed'] == [1,1,1,1,1]

def test_class_env_parameter_overload_torpedos_search_range():
    # this test overloads the torpedo search range parameter.

    kwargs = {
                'torpedos_search_range': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.torpedo_parameters['search_range'] == 10

def test_gym_env_parameter_overload_torpedos_search_range():
    # this test overloads the torpedo search range parameter.

    kwargs = {
                'torpedos_search_range': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.torpedo_parameters['search_range'] == 10
# #
# # Sonobouy settings tests
# #

def test_class_env_parameter_overload_sonobuoy_active_range():
    # this test overloads the sonobuoy active range parameter.

    kwargs = {
                'sonobuoy_active_range': 10
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.sonobuoy_parameters['active_range'] == 10

def test_gym_env_parameter_overload_sonobuoy_active_range():
    # this test overloads the sonobuoy active range parameter.

    kwargs = {
                'sonobuoy_active_range': 10
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.sonobuoy_parameters['active_range'] == 10


def test_class_env_parameter_overload_sonobuoy_display_range():
    # this test overloads the sonobuoy display range parameter. 
    # This either shows the sb range on the map or not 

    kwargs = {
                'display_range': False
    }

    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    assert game.sonobuoy_parameters['display_range'] == False

def test_gym_env_parameter_overload_sonobuoy_display_range():
    # this test overloads the sonobuoy display range parameter. 
    # This either shows the sb range on the map or not 

    kwargs = {
                'display_range': False
    }

    gym_env = gym.make('plark-env-v0', **kwargs)
    game = gym_env.env.activeGames[len(gym_env.env.activeGames)-1]
    
    assert game.sonobuoy_parameters['display_range'] == False