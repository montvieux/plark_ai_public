from .newgame import Newgame
import json
import logging
import os 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Environment():

    def __init__(self):
        self.activeGames = []
        self.numberOfActiveGames = 0

    # Triggers the creation of a new game
    def createNewGame(self, config_file_path= None, **kwargs):
        if config_file_path:
            self.game_config = self.load_game_configuration( config_file=config_file_path)
        else:
            self.game_config = self.load_game_configuration()

        gm = Newgame(self.game_config, **kwargs)
        self.activeGames.append(gm)
        self.numberOfActiveGames = self.numberOfActiveGames + 1
        logger.info('Game Created')

    # Stops all active games
    def stopAllGames(self):
        self.activeGames = []
        self.numberOfActiveGames = 0

    def load_game_configuration(self, config_file=None):
        try:
            if config_file is None:
                default_config = os.path.join(os.path.dirname(__file__), '../game_config/10x10/balanced.json')
                default_config = os.path.normpath(default_config)
                config_file = default_config
            logger.info('Opening config from:'+str(config_file))
            with open(config_file) as f:
                game_config = json.load(f)
                return game_config
        except IOError:
            raise ValueError('No configuration file provided')

