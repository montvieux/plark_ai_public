from ..classes import *
import sys
import os

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

def test_panther_gamestate_bingo():
    # Tests the BINGO gamestate from the panthers perspective
    # BINGO state a set amount of turns before the pelican need to return to base for fuel  
    # 
    # Any pelican agent can be used as this test only requires the panther to end its turns.

    bingo_limit = 1 # Bingo limit must be set to 1 as 0 disables the rule

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'bingo_limit': bingo_limit
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    # Perform required game steps
    game.game_step('end') # ends panther turn 0
    game.game_step('end') # ends panther turn 1

    # assess the game 
    assert game.gameState == 'BINGO'

def test_pelican_gamestate_bingo():
    # Tests the BINGO gamestate from the pelicans perspective
    # BINGO state a set amount of turns before the pelican need to return to base for fuel  
    # 
    # Any panther agent can be used as this test only requires the pelican to end its turns.
    
    bingo_limit = 1 # Bingo limit must be set to 1 as 0 disables the rule

    # Game parameters
    kwargs = {
                'driving_agent': "pelican",
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'bingo_limit': bingo_limit
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    
    # Perform required game steps
    game.game_step('end') # ends panther turn 0
    game.game_step('end') # ends panther turn 1

    # assess the game 
    assert game.gameState == 'BINGO'

def test_panther_gamestate_winchester():
    # Tests the winchester gamestate from the panther perspective 
    # WINCHESTER state is when the aircraft has used all its torpedoes and all deployed torpedoes have finished running.
    # 
    # This test requires the Pelican_Agent_3_Bouys agent as the starting locations for both panther and pelican have been 
    # selected so the agent will deploy a torpedo. 
    # 
    # Torpedo hunt must be false.
    # Default torpedos must be set to 1.
    # Torpedo turn limit must be set to 1.
    # Panther start location must be col 2 row 3.
    # Pelican start location must be col 2 row 2.
    # Pelican move limit must be 0.

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'default_torps': 1,
                'torpedos_turn_limit': 1,
                'torpedos_hunt': False,
                'panther_start_col': 2,
                'panther_start_row': 3,
                'pelican_start_col': 2,
                'pelican_start_row': 2,
                'pelican_move_limit': 0
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('end') # ends panther turn 0, pelican deploys sonobuoy, sonobuoy gets triggered.
    game.game_step('end') # ends panther turn 1, pelican deploys torpedo. 
    game.game_step('end') # ends panther turn 2, torpedo reacher turn limit, WINCHESTER active 

    # assess the game 
    assert game.gameState == 'WINCHESTER'

def test_pelican_gamestate_winchester():
    # Tests the winchester gamestate from the pelican perspective
    # WINCHESTER state is when the aircraft has used all its torpedoes and all deployed torpedoes have finished running.
    # 
    # Torpedo hunt must be true.
    # Default torpedos must be set to 1.
    # Torpedo turn limit must be set to 1.


    # Game parameters
    kwargs = {
                'driving_agent': "pelican",
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'default_torps': 1,
                'torpedos_hunt': True,
                'torpedos_turn_limit': 1
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('drop_torpedo')
    game.game_step('end')

    # assess the game 
    assert game.gameState == 'WINCHESTER'

def test_panther_gamestate_escape_up_even():
    # Test the escape gamestate from the panther perspective in an even col moving up
    #  ESCAPE state is when the panther moves off the top edge of the map 

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 0,
                'panther_start_row': 0                
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('1') # move Up 

    # assess the game
    assert game.gameState == 'ESCAPE'

def test_panther_gamestate_escape_up_left_even():
    # Test the escape gamestate from the panther perspective in an even col moving up left
    #  ESCAPE state is when the panther moves off the top edge of the map 

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 0,
                'panther_start_row': 0
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('0') # move Up left

    # assess the game
    assert game.gameState == 'ESCAPE' 

def test_panther_gamestate_escape_up_right_even():
    # Test the escape gamestate from the panther perspective in an even col moving up right
    #  ESCAPE state is when the panther moves off the top edge of the map 

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 0,
                'panther_start_row': 0,
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('5') # move Up right

    # assess the game
    assert game.gameState == 'ESCAPE'

def test_panther_gamestate_escape_up_odd():
    # Test the escape gamestate from the panther perspective in an odd col moving up 
    #  ESCAPE state is when the panther moves off the top edge of the map 

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 1,
                'panther_start_row': 0,
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('1') # move Up 

    # assess the game
    assert game.gameState == 'ESCAPE'

def test_panther_gamestate_escape_up_left_odd():
    # Test the escape gamestate from the panther perspective in an even odd moving up left 
    #  ESCAPE state is when the panther moves off the top edge of the map
    # 
    # This should return "running" as odd cols have diagional up movements available in the map

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 1,
                'panther_start_row': 0,
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('0') # move Up left

    # assess the game
    assert game.gameState == 'Running' 

def test_panther_gamestate_escape_up_right_odd():
    # Test the escape gamestate from the panther perspective in an odd col moving up right
    #  ESCAPE state is when the panther moves off the top edge of the map 
    # 
    # This should return "running" as odd cols have diagional up movements available in the map

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys",
                'panther_start_col': 1,
                'panther_start_row': 0,
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('5') # move Up right

    # assess the game
    assert game.gameState == 'Running'

def test_pelican_gamestate_escape():
    # Test the escape gamestate from the pelican perspective
    # ESCAPE state is when the panther moves off the top edge of the map 
    # Game parameters

    kwargs = {
                'driving_agent': "pelican",
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'panther_start_col': 0,
                'panther_start_row': 0
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('end') # end the pelican turn

    # assess the game 
    assert game.gameState == 'ESCAPE'

def test_panther_gamestate_pelicanwin():
    # Tests the pelicanwin gamestate from the panther perspective
    # This test requires the Pelican_Agent_3_Bouys agent as the starting locations for both panther and pelican have been 
    # selected so the agent will deploy a torpedo. 
    # 
    # Panther start location must be col 2 row 2.
    # Pelican start location must be col 2 row 2.

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
                'pelican_agent_name': "Pelican_Agent_3_Bouys",
                'panther_start_col': 2,
                'panther_start_row': 2,
                'pelican_start_col': 2,
                'pelican_start_row': 2,
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('end') # ends panther turn 0, pelican deploys sonobuoy, sonobuoy gets triggered.
    game.game_step('end') # ends panther turn 1, pelican deploys torpedo. 
    game.game_step('end') # ends panther turn 2, torpedo reacher turn limit, PELICANWIN active 

    # assess the game 
    assert game.gameState == 'PELICANWIN'

def test_pelican_gamestate_pelicanwin():
    # Test the pelicanwin gamestate from the pelican perspective
    # 
    # Panther start location must be col 2 row 2.
    # Pelican start location must be col 2 row 2.

    # Game parameters
    kwargs = {
                'driving_agent': "pelican",
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North",
                'panther_start_col': 2,
                'panther_start_row': 2,
                'pelican_start_col': 2,
                'pelican_start_row': 2
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]

    # Perform required game steps
    game.game_step('drop_torpedo')
    game.game_step('end')

    # assess the game 
    assert game.gameState == 'PELICANWIN'