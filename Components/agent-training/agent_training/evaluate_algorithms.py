import argparse
from datetime import datetime
from gym_plark.envs import plark_env, plark_env_non_image_state
import helper
import logging
import os
from tensorboardX import SummaryWriter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def evaluate_algorithms(exp_name, base_path, tb_enabled, algorithms, victory_threshold, victory_trials, max_seconds, testing_interval, use_non_image):
	basicdate = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
	exp_name = "{}_{}".format(exp_name, basicdate)
	exp_path = os.path.join(base_path, exp_name)
	logger.info("Storing results in {}".format(exp_path))

	writer = None
	if tb_enabled:
		writer = SummaryWriter(exp_path)

	for algo in algorithms:
		tb_log_name = "{}_non_image".format(algo) if use_non_image else algo
		logger.info("Evaluating algorithm: {}; non-image: {}".format(algo, use_non_image))
		if use_non_image:
			image_based = False 
			env = plark_env_non_image_state.PlarkEnvNonImageState(driving_agent='pelican', config_file_path='/Components/plark-game/plark_game/game_config/10x10/panther_easy.json')
			policy = "MlpPolicy" # CnnPolicy doesn't work with MultiDiscrete observation space
		else:	
			image_based = True 
			env = plark_env.PlarkEnv(driving_agent='pelican', config_file_path='/Components/plark-game/plark_game/game_config/10x10/panther_easy.json')
			policy = "CnnPolicy"

		model = helper.make_new_model(algo, policy, env)
		helper.train_until(model, env, victory_threshold, victory_trials, max_seconds, testing_interval, tb_writer=writer, tb_log_name=tb_log_name)
		helper.save_model_with_env_settings(exp_path, model, algo, env, image_based, basicdate)

	writer.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Evaluate performance of different algorithms over a fixed time period")

	parser.add_argument("--exp-name", type=str, default="test", help="Experiment name prefix")
	parser.add_argument("--victory-trials", type=int, default=10, help="Number of game trials to use when evaluating algorithm performance")
	parser.add_argument("--victory-threshold", type=float, default=0.8, help="Desired fraction of trials that should be won")
	# Default to 30 minutes
	parser.add_argument("--max-seconds", type=float, default=1800, help="Maximum time to train each algorithm for")
	parser.add_argument("--testing-interval", type=int, default=1000, help="Number of training steps between evaluations")
	parser.add_argument("--base-path", type=str, default="/data/agents/models", help="Directory to store trained models & logs in")
	parser.add_argument("--tb-enabled", type=bool, default=True, help="Whether to log to tensorboard")
	parser.add_argument("--algorithms", nargs="+", type=str, default=["PPO2"], help="Which algorithm to evaluate")
	parser.add_argument("--use-non-image", type=bool, default=False, help="Whether to evaluate using non-image observations (direct game state)")

	args = parser.parse_args()

	evaluate_algorithms(args.exp_name, args.base_path, args.tb_enabled, args.algorithms, args.victory_threshold, args.victory_trials, args.max_seconds, args.testing_interval, args.use_non_image)

	