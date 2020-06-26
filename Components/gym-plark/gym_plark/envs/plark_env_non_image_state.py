from gym import spaces
from gym_plark.envs.plark_env import PlarkEnv
import logging

logger = logging.getLogger(__name__)

class PlarkEnvNonImageState(PlarkEnv):

	def __init__(self,config_file_path=None,verbose=False, **kwargs):
		if kwargs is None:
			kwargs = {}
		kwargs['image_based'] = False
		logger.info('non image kwargs: '+ str(kwargs))
		self.image_based = False
		super(PlarkEnvNonImageState, self).__init__(config_file_path,verbose, **kwargs)
		self.image_based = False


		
			
