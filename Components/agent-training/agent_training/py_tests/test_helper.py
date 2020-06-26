from gym_plark.envs import plark_env
from .. import helper
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import PPO2
import os
import datetime

class MockEnv(plark_env.PlarkEnv):
	def __init__(self,driving_agent = 'pelican',config_file_path=None,pelican_agent_filepath=None,panther_agent_filepath=None, panther_agent_name=None, pelican_agent_name=None,render_width=310,render_height=250,verbose=False, **kwargs):
		
		self.kwargs = kwargs
		self.current_evaluation = 0
		self.num_steps = 0

		super(MockEnv, self).__init__(config_file_path,verbose, **kwargs)
		

	def reset(self):
		self.num_steps = 0
		return super(MockEnv, self).reset()

	def step(self, action):
		ob, reward, done, _info = super(MockEnv, self).step(action)

		self.num_steps += 1
		reward = 0
		done = False
		_info = {'result': "LOSE"}

		# Generate a mixture of rewards
		if self.num_steps % 2 == 0:
			reward = 1
		elif self.num_steps % 3 == 0:
			reward = -1
		else:
			reward = 0

		# Ensure episodes are different lengths
		if self.num_steps == 5 + self.current_evaluation:
			done = True
			self.current_evaluation += 1
			# Ensure mixture of win/lose results
			if self.current_evaluation % 2 == 0:
				_info['result'] = "WIN"
		return ob, reward, done, _info

def test_evaluate_policy():
	panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/' #This model is in minio or the package.
	env = MockEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	# check_env(env)

	model = PPO2('CnnPolicy', env)

	n_eval_episodes = 2
	episode_rewards, episode_lengths, victories = helper.evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=True)
	assert episode_rewards == [1.0,2.0]
	assert episode_lengths == [5, 6]
	assert victories == [False, True]

def test_evaluate_policy_with_vectorised_env():
	panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/' #This model is in minio or the package.
	def defineEnv():
		return MockEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	
	env = SubprocVecEnv([defineEnv for i in range(4)])

	model = PPO2('CnnPolicy', env)

	n_eval_episodes = 2
	episode_rewards, episode_lengths, victories = helper.evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=True)
	assert episode_rewards == [1.0,2.0]
	assert episode_lengths == [5, 6]
	assert victories == [False, True]

def test_train_until():
	panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/' #This model is in minio or the package.
	env = MockEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')

	model = PPO2('CnnPolicy', env)

	achieved_goal, steps, elapsed_seconds = helper.train_until(model, env, victory_threshold=0.501, victory_trials=2, max_seconds=30, testing_interval=50)
	# MockEnv only ever wins 50% of time
	assert achieved_goal == False
	# Should time out since won't have achieved goal
	assert elapsed_seconds >= 30

	achieved_goal, steps, elapsed_seconds = helper.train_until(model, env, victory_threshold=0.5, victory_trials=2, max_seconds=30, testing_interval=50)
	assert achieved_goal == True
	assert elapsed_seconds < 30

def test_make_new_model_PPO2():
	env = MockEnv(driving_agent='pelican',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	policy = "CnnPolicy"
	
	model = helper.make_new_model("PPO2",policy,env, None)
	
	if "PPO2" in str(type(model)):
		PPO = True
	assert PPO == True

def test_make_new_model_DQN():
	env = MockEnv(driving_agent='pelican',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	policy = "CnnPolicy"	
	model = helper.make_new_model("DQN",policy,env, None)
	
	if "DQN" in str(type(model)):
		DQN = True
	assert DQN == True

def test_make_new_model_A2C():
	env = MockEnv(driving_agent='pelican',config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	policy = "CnnPolicy"
	model = helper.make_new_model("A2C",policy,env, None)

	if "A2C" in str(type(model)):
		A2C = True
		
	assert A2C == True

def test_model_label():
	modeltype = "DQN"
	modelplayer = "PELICAN"
	basicdate = "00_33_00"
	newlabel = helper.model_label(modeltype,basicdate,modelplayer)
	assert newlabel == "DQN_00_33_00_PELICAN"
	
def test_save_model_with_env_settings():
	def defineEnv():
		panther_agent_filepath = '/data/agents/models/test_20200325_184254/PPO2_20200325_184254_panther/'
		return MockEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath,config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json')
	
	env1 = defineEnv()
	env2 = SubprocVecEnv([defineEnv for i in range(4)])

	model1 = PPO2('CnnPolicy', env1)
	model2 = PPO2('CnnPolicy', env2)

	basicdate1 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	testdir = "/tmp/testing"

	# Should handle regular envs
	helper.save_model_with_env_settings(testdir, model1, "ppo2", env1, basicdate1)
	model_label1 = helper.model_label("ppo2", basicdate1, 'pelican')
	expected_dir1 = os.path.join(testdir, model_label1)
	metadata_file1 = os.path.join(expected_dir1, "metadata.json")
	model_file1 = os.path.join(expected_dir1, model_label1 + ".zip")
	assert os.path.exists(expected_dir1)
	assert os.path.exists(metadata_file1)
	assert os.path.exists(model_file1)

	basicdate2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

	# Should handle VecEnv
	helper.save_model_with_env_settings("/tmp/testing", model2, "ppo2", env2, basicdate2)
	model_label2 = helper.model_label("ppo2", basicdate2, 'pelican')
	expected_dir2 = os.path.join(testdir, model_label2)
	metadata_file2 = os.path.join(expected_dir2, "metadata.json")
	model_file2 = os.path.join(expected_dir2, model_label2 + ".zip")
	assert os.path.exists(expected_dir2)
	assert os.path.exists(metadata_file2)
	assert os.path.exists(model_file2)
