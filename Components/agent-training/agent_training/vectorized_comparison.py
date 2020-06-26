import argparse
from datetime import datetime
from gym_plark.envs import plark_env, plark_env_non_image_state
import helper
import logging
import os
from stable_baselines.common.vec_env import SubprocVecEnv
from tensorboardX import SummaryWriter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def createNonImageEnv():
	return plark_env_non_image_state.PlarkEnvNonImageState(driving_agent='pelican', config_file_path='/Components/plark-game/plark_game/game_config/10x10/panther_easy.json')

def createImageEnv():
	return plark_env.PlarkEnv(driving_agent='pelican', config_file_path='/Components/plark-game/plark_game/game_config/10x10/panther_easy.json')

def compare_envs(exp_name, base_path, tb_enabled, victory_threshold, victory_trials, max_seconds, testing_interval, num_parallel_envs, non_image):
	basicdate = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
	exp_name = "{}_{}".format(exp_name, basicdate)
	exp_path = os.path.join(base_path, exp_name)
	logger.info("Storing results in {}".format(exp_path))

	writer = None
	if tb_enabled:
		writer = SummaryWriter(exp_path)

	for parallel in [False, True]:
		algo = "PPO2"
		policy = "MlpPolicy" if non_image else "CnnPolicy"
		tb_log_name = "{}_parallel".format(algo) if parallel else algo
		logger.info("Evaluating {}; parallel: {}".format(algo, parallel))
		if parallel:
			logger.info("Evaluating using {} parallel environments".format(num_parallel_envs))
			env_fn = createNonImageEnv if non_image else createImageEnv
			env = SubprocVecEnv([env_fn for _ in range(num_parallel_envs)])
		else:	
			env = createNonImageEnv() if non_image else createImageEnv()

		model = helper.make_new_model(algo, policy, env)
		helper.train_until(model, env, victory_threshold, victory_trials, max_seconds, testing_interval, tb_writer=writer, tb_log_name=tb_log_name)
		helper.save_model_with_env_settings(exp_path, model, algo, env, basicdate)

	writer.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Compare performance of training with vectorized (parallel) environments vs a single environments")

	parser.add_argument("--exp-name", type=str, default="compare", help="Experiment name prefix")
	parser.add_argument("--victory-trials", type=int, default=10, help="Number of game trials to use when evaluating algorithm performance")
	parser.add_argument("--victory-threshold", type=float, default=0.8, help="Desired fraction of trials that should be won")
	# Default to 30 minutes
	parser.add_argument("--max-seconds", type=float, default=1800, help="Maximum time to train each algorithm for")
	parser.add_argument("--testing-interval", type=int, default=1000, help="Number of training steps between evaluations")
	parser.add_argument("--base-path", type=str, default="/data/agents/models", help="Directory to store trained models & logs in")
	parser.add_argument("--tb-enabled", type=bool, default=True, help="Whether to log to tensorboard")
	parser.add_argument("--num-parallel-envs", type=int, default=4, help="Number of parallel environments to use")
	parser.add_argument("--non-image", type=bool, default=True, help="Whether to use non-image observations")

	args = parser.parse_args()

	compare_envs(args.exp_name, args.base_path, args.tb_enabled, args.victory_threshold, args.victory_trials, args.max_seconds, args.testing_interval, args.num_parallel_envs, args.non_image)

	