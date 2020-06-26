import logging
import gym
from gym.envs.registration import register
from .envs import *
# from gym_plark.envs.plark_env_sonobuoy_deployment import PlarkEnvSonobuoyDeployment 

logger = logging.getLogger(__name__)


def register(id, entry_point, force=True, kwargs=None):
    env_specs = gym.envs.registry.env_specs
    if id in env_specs.keys():
        if not force:
            return
        del env_specs[id]
    gym.register(
        id=id,
        entry_point=entry_point,
        kwargs = kwargs
    )
    
register(
    id='plark-env-v0',
    entry_point='gym_plark.envs:PlarkEnv',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-non-image-v0',
    entry_point='gym_plark.envs:PlarkEnvNonImageState',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-sparse-v0',
    entry_point='gym_plark.envs:PlarkEnvSparse',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-guided-reward-v0',
    entry_point='gym_plark.envs:PlarkEnvGuidedReward',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-illegal-move-v0',
    entry_point='gym_plark.envs:PlarkEnvIllegalMove',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-sonobuoy-deployment-v0',
    entry_point='gym_plark.envs:PlarkEnvSonobuoyDeployment',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='plark-env-top-left-v0',
    entry_point='gym_plark.envs:PlarkEnvTopLeft',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'pelican'
    }
)

register(
    id='panther-env-reach-top-v0',
    entry_point='gym_plark.envs:PantherEnvReachTop',
    kwargs={
        'config_file_path':'/Components/plark-game/plark_game/game_config/10x10/balanced.json',
        'driving_agent':'panther'
    }
)
