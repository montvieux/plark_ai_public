from ..classes import *
import sys
import os

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)


def test_load_basic_pelican_agent():
    env = Environment()

    # Game parameters
    kwargs = {
                'driving_agent': "panther",
                'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_5_buoys.py",
                'pelican_agent_name': "Pelican_Agent_5_Bouys"
    }

    # # create test agent
    oldpath, sys.path[:] = sys.path[:], [os.path.join(
        '/Components/plark-game/plark_game/agents/basic')]
    module = __import__('pelicanAgent_5_buoys')
    cls = getattr(module, 'Pelican_Agent_5_Bouys')

    # create new game with set agent
    env.createNewGame(**kwargs)
    agent = env.activeGames[len(env.activeGames)-1].pelicanAgent

    assert type(agent) == cls


def test_load_basic_panther_agent():
    env = Environment()

    # Game parameters
    kwargs = {
                'driving_agent': "pelican",
                'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
                'panther_agent_name': "Panther_Agent_Move_North"
    }
    # # create test agent
    oldpath, sys.path[:] = sys.path[:], [os.path.join(
        '/Components/plark-game/plark_game/agents/basic')]
    module = __import__('pantherAgent_move_north')
    cls = getattr(module, 'Panther_Agent_Move_North')

    # create new game with set agent
    env.createNewGame(**kwargs)
    agent = env.activeGames[len(env.activeGames)-1].pantherAgent

    assert type(agent) == cls


def test_sonobuoy_activation_Hot_panther():
    # tests that a deployed sonobuoy is triggered by the panther. The below setting are selected to place a panther and pelican in the 
    # same location ensuring 
    kwargs = {
        'map_width': 10,
        'map_height': 10,
        'driving_agent': "panther",
        'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
        'pelican_agent_name': "Pelican_Agent_3_Bouys",
        'panther_start_col': 2,
        'panther_start_row': 2,
        'pelican_start_col': 2,
        'pelican_start_row': 2,
        'default_torps': 0,
        'default_sonobuoys': 1
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]


    # Perform required game steps
    game.game_step('end') # ends panther turn 0, pelican deploys sonobuoy, sonobuoy gets triggered.

    assert game.globalSonobuoys[0].state == 'HOT'

def test_sonobuoy_activation_Hot_pelican():

    kwargs = {
        'map_width': 10,
        'map_height': 10,
        'driving_agent': "pelican",
        'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
        'panther_agent_name': "Panther_Agent_Move_North",
        'panther_start_col': 2,
        'panther_start_row': 2,
        'pelican_start_col': 2,
        'pelican_start_row': 2,
        'default_torps': 0,
        'default_sonobuoys': 1
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]


    # Perform required game steps
    game.game_step('drop_buoy')
    game.game_step('end') # ends pelican turn.

    assert game.globalSonobuoys[0].state == 'HOT'

def test_sonobuoy_activation_Cold_panther():
    # tests that a deployed sonobuoy is triggered by the panther. The below setting are selected to place a panther and pelican in the 
    # same location ensuring 
    kwargs = {
        'map_width': 10,
        'map_height': 10,
        'driving_agent': "panther",
        'pelican_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pelicanAgent_3_buoys.py",
        'pelican_agent_name': "Pelican_Agent_3_Bouys",
        'panther_start_col': 9,
        'panther_start_row': 9,
        'pelican_start_col': 2,
        'pelican_start_row': 2,
        'default_torps': 0,
        'default_sonobuoys': 1
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]


    # Perform required game steps
    game.game_step('end') # ends panther turn 0, pelican deploys sonobuoy, sonobuoy gets triggered.

    assert game.globalSonobuoys[0].state == 'COLD'

def test_sonobuoy_activation_Cold_pelican():

    kwargs = {
        'map_width': 10,
        'map_height': 10,
        'driving_agent': "pelican",
        'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
        'panther_agent_name': "Panther_Agent_Move_North",
        'panther_start_col': 9,
        'panther_start_row': 9,
        'pelican_start_col': 2,
        'pelican_start_row': 2,
        'default_torps': 0,
        'default_sonobuoys': 1
    }

    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]


    # Perform required game steps
    game.game_step('drop_buoy')
    game.game_step('end') # ends pelican turn.

    assert game.globalSonobuoys[0].state == 'COLD'

def test_driving_pelican_turn():
    """
    Check that a driving pelican agent can take several moves before 
    the panther gets a turn
    """
    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
    game = env.activeGames[-1]

    pelican_move = 0
    # Pelican should get 10 moves
    for i in range(9):
        # Alternately move up & down to use up moves with legal moves
        action = '4' if i % 2 == 0 else '1'
        game.game_step(action)
        assert game.turn_count == 0, "Should still be on first turn"
        assert game.pelican_move_in_turn == pelican_move + 1, "Pelican move should have advanced"
        pelican_move = game.pelican_move_in_turn
        assert game.pantherPlayer.col == 5, "Non-driving Panther should not  have moved"
        assert game.pantherPlayer.row == 9, "Non-driving Panther should not  have moved"

    # Next move should end turn and allow panther to move
    game.game_step('1')
    assert game.turn_count == 1, "Turn should have ended"
    panther_loc = (game.pantherPlayer.col, game.pantherPlayer.row)
    assert panther_loc != (5, 9), "Non-driving Panther should have moved"

def test_driving_panther_turn():
    """
    Check that a driving panther agent can take several moves before 
    the pelican gets a turn
    """
    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    # Configure panther to have a move limit > 1 to check turn behaviour
    env.createNewGame(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json', driving_agent='panther', panther_move_limit=5)
    game = env.activeGames[-1]

    panther_move = 0

    # Panther move 1
    game.game_step('1')
    assert game.panther_move_in_turn == panther_move + 1, "Panther move should have advanced"
    panther_move = game.panther_move_in_turn

    # Pelican will take turn immediately before panther's first move
    # should not move after this until end of panther's turn
    pelican_loc_first_turn = (game.pelicanPlayer.col, game.pelicanPlayer.row)
    first_turn_sbs = len(game.globalSonobuoys)
    first_turn_torps = len(game.globalTorps)
    pelican_moved = pelican_loc_first_turn != (0, 9) or game.pelican_move_in_turn > 0
    pelican_dropped_something = first_turn_sbs > 0 or first_turn_torps > 0
    pelican_first_turn_moves = game.pelican_move_in_turn
    assert pelican_moved or pelican_dropped_something or game.illegal_pelican_move, "Non-driving Pelican should have done SOMETHING"

    # Panther moves 2-4 (of 5)
    # Pelican should do nothing for remainder of Panther's turn
    for i in range(3):
        # Keep moving up
        action = '1'
        game.game_step(action)
        assert game.turn_count == 0, "Should still be on first turn"
        assert game.panther_move_in_turn == panther_move + 1, "Panther move should have advanced"
        panther_move = game.panther_move_in_turn
        pelican_loc = (game.pelicanPlayer.col, game.pelicanPlayer.row)
        assert pelican_loc == pelican_loc_first_turn, "Non-driving Pelican should not have moved"
        assert game.pelican_move_in_turn == pelican_first_turn_moves, "Non-driving Pelican should not have moved"
        assert len(game.globalSonobuoys) == first_turn_sbs, "Non-driving Pelican should not have dropped any sonobuoys"
        assert len(game.globalTorps) == first_turn_torps, "Non-driving Pelican should not have dropped any torpedoes"

    # Next move should end turn and allow Pelican to move
    game.game_step('1')
    assert game.turn_count == 1, "Turn should have ended"

    # Pelican will not move until start of next step
    game.game_step('1')
    assert game.turn_count == 1, "Should still be on second turn"
    pelican_loc = (game.pelicanPlayer.col, game.pelicanPlayer.row)
    pelican_moved = pelican_loc != pelican_loc_first_turn or game.pelican_move_in_turn > 0
    pelican_dropped_something = len(game.globalSonobuoys) > first_turn_sbs or len(game.globalTorps) > first_turn_torps
    assert pelican_moved or pelican_dropped_something or game.illegal_pelican_move, "Non-driving Pelican should have done SOMETHING"

def test_non_driving_pelican_turn():
    """
    Check that a non-driving pelican agent can take several moves before 
    the panther gets a turn
    """
    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    # Configure panther to have a move limit > 1 to check turn behaviour
    env.createNewGame(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json', driving_agent='panther', panther_move_limit=5, pelican_agent_filepath='/Components/plark-game/plark_game/agents/test/PelicanAgentTestTurn.py', pelican_agent_name='PelicanAgentTestTurn')
    game = env.activeGames[-1]

    pelicanAgent = game.pelicanAgent
    assert pelicanAgent.moves_taken == 0, "Pelican should not have taken any moves before the game starts"

    # Pelican should take turn (make multiple moves) before Panther's first move
    game.game_step('1')
    assert game.turn_count == 0, "Should still be on first turn"
    assert pelicanAgent.moves_taken == game.pelican_parameters['move_limit'], "Non-driving Pelican should have made several moves"

    # Pelican should not move again until panther's turn is over
    game.game_step('1')
    assert game.turn_count == 0, "Should still be on first turn"
    assert pelicanAgent.moves_taken == game.pelican_parameters['move_limit'], "Non-driving Pelican should have waited for panther to finish turn"

    # Turn has ended but next turn not begun - pelican should still not have moved
    game.game_step('end')
    assert game.turn_count == 1, "Turn should have ended"
    assert pelicanAgent.moves_taken == game.pelican_parameters['move_limit'], "Non-driving Pelican should have waited for panther to finish turn"

    # Next move commences next turn - pelican should take turn first
    game.game_step('1')
    assert game.turn_count == 1, "Should still be on second turn"
    assert pelicanAgent.moves_taken ==  2*game.pelican_parameters['move_limit'], "Non-driving Pelican should have taken second turn"

    # Pelican should not move again until panther's turn is over
    game.game_step('1')
    assert game.turn_count == 1, "Should still be on second turn"
    assert pelicanAgent.moves_taken ==  2*game.pelican_parameters['move_limit'], "Non-driving Pelican should have waited for panther to finish turn"

def test_non_driving_panther_turn():
    """
    Check that a non-driving panther agent can take several moves before 
    the pelican gets its next turn
    """
    # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    # Configure panther to have a move limit > 1 to check turn behaviour
    env.createNewGame(config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json', driving_agent='pelican', panther_move_limit=5, panther_agent_filepath='/Components/plark-game/plark_game/agents/test/PantherAgentTestTurn.py', panther_agent_name='PantherAgentTestTurn')
    game = env.activeGames[-1]

    pantherAgent = game.pantherAgent
    assert pantherAgent.moves_taken == 0, "Pelican should not have taken any moves before the game starts"

    # Panther should wait until Pelican's first turn is over
    game.game_step('4')
    assert game.turn_count == 0, "Should still be on first turn"
    assert pantherAgent.moves_taken == 0, "Non-driving Panther should wait for Pelican's first turn to end"
    game.game_step('1')
    assert game.turn_count == 0, "Should still be on first turn"
    assert pantherAgent.moves_taken == 0, "Non-driving Panther should wait for Pelican's first turn to end"

    # End turn, which should trigger Panther to take turn
    game.game_step('end')
    assert game.turn_count == 1, "Turn should have ended"
    assert pantherAgent.moves_taken == game.panther_parameters['move_limit'], "Non-driving Panther should have taken turn now pelican's turn is over"

    # Next move commences next turn - pelican should take turn first
    game.game_step('4')
    assert game.turn_count == 1, "Should still be on second turn"
    assert pantherAgent.moves_taken ==  game.panther_parameters['move_limit'], "Non-driving Panther should wait for Pelican to finish turn"

    # Panther should not move again until Pelican's turn is over
    game.game_step('1')
    assert game.turn_count == 1, "Should still be on second turn"
    assert pantherAgent.moves_taken ==  game.panther_parameters['move_limit'], "Non-driving Panther should have waited for Pelican to finish turn"

    # End turn, which should trigger Panther to take turn
    game.game_step('end')
    assert game.turn_count == 2, "Turn should have ended"
    assert pantherAgent.moves_taken == 2*game.panther_parameters['move_limit'], "Non-driving Panther should have taken turn now pelican's turn is over"

def test_madman_trigger():
    """
    To test the activation of the madman sensor. 
    """

    kwargs = {
        'map_width': 5,
        'map_height': 5,
        'driving_agent': "pelican",
        'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
        'panther_agent_name': "Panther_Agent_Move_North",
        'panther_start_col': 3,
        'panther_start_row': 4,
        'pelican_start_col': 3,
        'pelican_start_row': 3,
    }

        # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    pelicanAgent = game.pelicanPlayer

    # Check that madman is false at the start of the game 
    assert pelicanAgent.madmanStatus == False

    # Perform required game steps
    game.game_step('4') # Down
    game.game_step('4') # Down
    game.game_step('end') # ends pelican turn.

    assert pelicanAgent.madmanStatus == True
    

def test_madman_reset():
    """
    To test the reset of the madman sensor. 
    """

    kwargs = {
        'map_width': 5,
        'map_height': 5,
        'driving_agent': "pelican",
        'panther_agent_filepath': "/Components/plark-game/plark_game/agents/basic/pantherAgent_move_north.py",
        'panther_agent_name': "Panther_Agent_Move_North",
        'panther_start_col': 3,
        'panther_start_row': 4,
        'pelican_start_col': 3,
        'pelican_start_row': 3,
    }

        # Create the test enviroment and activate the game using the kwargs
    env = Environment()
    env.createNewGame(**kwargs)
    game = env.activeGames[len(env.activeGames)-1]
    pelicanAgent = game.pelicanPlayer

    # Check that madman is false at the start of the game 
    assert pelicanAgent.madmanStatus == False
    # Perform required game steps
    game.game_step('4') # Down
    game.game_step('4') # Down
    game.game_step('end') # ends pelican turn.

    # Check that the madman has been triggered.
    assert pelicanAgent.madmanStatus == True

    # Move onto the next turn 
    game.game_step('end') # ends pelican turn.

    assert pelicanAgent.madmanStatus == False