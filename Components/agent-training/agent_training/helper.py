import os
import sys
import datetime
import json
import logging
import imageio
import PIL.Image
import numpy as np
from plark_game import classes
from gym_plark.envs import plark_env

from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.vec_env import VecEnv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def model_label(modeltype,basicdate,modelplayer):
    label = modeltype + "_" + str(basicdate) + "_" + modelplayer
    return label

def make_new_model(model_type,policy,env, tensorboard_log=None):
    if model_type.lower() == 'dqn':
        model = DQN(policy,env,tensorboard_log=tensorboard_log)
    elif model_type.lower() == 'ppo':
        model = PPO(policy,env,tensorboard_log=tensorboard_log)
    elif model_type.lower() == 'a2c':
        model = A2C(policy,env,tensorboard_log=tensorboard_log)
    return model

def train_until(model, env, victory_threshold=0.8, victory_trials=10, max_seconds=120, testing_interval=200, tb_writer=None, tb_log_name=None):
    model.set_env(env)
    steps = 0
    max_victory_fraction = 0.0
    initial_time = datetime.datetime.now()
    current_time = datetime.datetime.now()
    elapsed_seconds = (current_time - initial_time).total_seconds()
    while elapsed_seconds < max_seconds:
        logger.info("Training for {} steps".format(testing_interval))
        before_learning = datetime.datetime.now()
        model.learn(testing_interval)
        after_learning = datetime.datetime.now()
        steps = steps + testing_interval

        logger.info("Learning took {:.2f} seconds".format((after_learning - before_learning).total_seconds()))
        
        logger.info("Checking victory")
        victory_count, avg_reward = check_victory(model, env, trials=victory_trials)
        after_check = datetime.datetime.now()
        logger.info("Victory check took {:.2f} seconds".format((after_check - after_learning).total_seconds()))
        victory_fraction = float(victory_count)/victory_trials
        logger.info("Won {} of {} evaluations ({:.2f})".format(victory_count, victory_trials, victory_fraction))
        max_victory_fraction = max(max_victory_fraction, victory_fraction)

        if tb_writer is not None and tb_log_name is not None:
            tb_writer.add_scalar('{}_avg_reward'.format(tb_log_name), avg_reward, steps)
            tb_writer.add_scalar('{}_victory_count'.format(tb_log_name), victory_count, steps)
            tb_writer.add_scalar('{}_victory_fraction'.format(tb_log_name), victory_fraction, steps)
        
        current_time = datetime.datetime.now()
        elapsed_seconds = (current_time - initial_time).total_seconds()
        
        if victory_fraction >= victory_threshold:
            logger.info("Achieved victory threshold after {} steps".format(steps))
            break
    logger.info("Achieved max victory fraction {:.2f} after {} seconds ({} steps)".format(max_victory_fraction, elapsed_seconds, steps))
    achieved_goal = max_victory_fraction >= victory_threshold
    return achieved_goal, steps, elapsed_seconds

def check_victory(model,env,trials = 10):
    victory_count = 0
    list_of_reward, n_steps, victories = evaluate_policy(model, env, n_eval_episodes=trials, deterministic=False, render=False, callback=None, reward_threshold=None, return_episode_rewards=True)

    victory_count = len([v for v in victories if v == True])
    logger.info('victory_count = '+ str(victory_count))        
    avg_reward = float(sum(list_of_reward))/len(list_of_reward)
    logger.info('avg_reward = '+ str(avg_reward))        
    return victory_count, avg_reward

def evaluate_policy(model, env, n_eval_episodes=4, deterministic=True, render=False, callback=None, reward_threshold=None, return_episode_rewards=False):
    """
    Modified from https://stable-baselines.readthedocs.io/en/master/_modules/stable_baselines/common/evaluation.html#evaluate_policy
    to return additional info
    """
    logger.debug("Evaluating policy")
    episode_rewards, episode_lengths, victories = [], [], []
    for ep in range(n_eval_episodes):
        logger.debug("Evaluating episode {} of {}".format(ep, n_eval_episodes))
        obs = env.reset()
        ep_done, state = False, None

        episode_length = 0
        episode_reward = 0.0
        if isinstance(env, VecEnv):
            episodes_reward = [0.0 for _ in range(env.num_envs)]
        else:
            episodes_reward = [0.0]

        victory = False

        while not ep_done:
            action, state = model.predict(obs, state=state, deterministic=deterministic)
            obs, rewards, dones, _infos = env.step(action)

            if not isinstance(env, VecEnv):
                rewards = [rewards]
                dones = np.array([dones])
                _infos = [_infos]

            episode_length += 1
            for i in range(len(rewards)):
                episodes_reward[i] += rewards[i]

            if callback is not None:
                callback(locals(), globals())

            if episode_length > 1000:
                logger.warning("Episode over 1000 steps.")
                
            if render:
                env.render()
            if any(dones):
                first_done_index = dones.tolist().index(True)
                info = _infos[first_done_index]
                victory = info['result'] == "WIN"
                episode_reward = episodes_reward[first_done_index]
                ep_done = True
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        victories.append(victory)

    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    if reward_threshold is not None:
        assert mean_reward > reward_threshold, "Mean reward below threshold: {:.2f} < {:.2f}".format(mean_reward, reward_threshold)

    if return_episode_rewards:
        return episode_rewards, episode_lengths, victories
    return mean_reward, std_reward, victories

# Save model base on env
def save_model_with_env_settings(basepath,model,modeltype,env,basicdate=None):
    if basicdate is None:
        basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    if isinstance(env, VecEnv):
        modelplayer = env.get_attr('driving_agent')[0]
        render_height = env.get_attr('render_height')[0]
        render_width = env.get_attr('render_width')[0]
        image_based = env.get_attr('image_based')[0]
    else:
        modelplayer = env.driving_agent 
        render_height = env.render_height
        render_width = env.render_width
        image_based = env.image_based
    model_path,model_dir, modellabel = save_model(basepath,model,modeltype,modelplayer,render_height,render_width,image_based,basicdate)
    return model_path,model_dir, modellabel

# Saves model and metadata
def save_model(basepath,model,modeltype,modelplayer,render_height,render_width,image_based,basicdate=None):
    if basicdate is None:
        basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    modellabel = model_label(modeltype,basicdate,modelplayer)
    model_dir = os.path.join(basepath, modellabel)
    logger.info("Checking folder: " + model_dir)
    os.makedirs(model_dir, exist_ok=True)
    os.chmod(model_dir, 0o777)
    logger.info("Saving Metadata")
    save_model_metadata(model_dir,modeltype,modelplayer,basicdate,render_height,render_width,image_based)

    logger.info("Saving Model")
    model_path = os.path.join(model_dir, modellabel + ".zip")
    model.save(model_path)
    logger.info('model_dir: '+model_dir)  
    logger.info('model_path: '+model_path) 
    
    return model_path,model_dir, modellabel

## Used for generating the json header file which holds details regarding the model.
## This will be used when playing the game from the GUI.
def save_model_metadata(model_dir,modeltype,modelplayer,dateandtime,render_height,render_width,image_based):
    
    jsondata = {}
    jsondata['algorithm'] =  modeltype
    jsondata['date'] = str(dateandtime)
    jsondata['agentplayer'] = modelplayer
    jsondata['render_height'] = render_height
    jsondata['render_width'] = render_width
    jsondata['image_based'] = image_based
    json_path = os.path.join(model_dir, 'metadata.json')
    with open(json_path, 'w') as outfile:
        json.dump(jsondata, outfile)    

    logger.info('json saved to: '+json_path)

    
## Custom Model Evaluation Method for evaluating Plark games. 
## Does require changes to how data is passed back from environments. 
## Instead of using return ob, reward, done, {} use eturn ob, reward, done, {game.state}
def custom_eval(model, env, n_eval_episodes=10, deterministic=True,
                    render=False, callback=None, reward_threshold=None,
                    return_episode_rewards=False, player_type="PELICAN"):
    """
    Runs policy for `n_eval_episodes` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a `VecEnv`
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (bool) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when `return_episode_rewards` is True
    """
    
    if player_type == "PELICAN":
        WINCONDITION = "PELICANWIN"
    if player_type == "PANTHER":
        WINCONDITION = "PANTHERWIN"
        
    if isinstance(env, VecEnv):
        assert env.num_envs == 1, "You must pass only one environment when using this function"
    totalwin = 0
    episode_rewards, episode_lengths = [], []
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        while not done:
            action, state = model.predict(obs, state=state, deterministic=deterministic)
            obs, reward, done, _info = env.step(action)
            episode_reward += reward
            if callback is not None:
                callback(locals(), globals())
            episode_length += 1
            if render:
                env.render()
            if WINCONDITION in _info:
                totalwin = totalwin + 1
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    if reward_threshold is not None:
        assert mean_reward > reward_threshold, 'Mean reward below threshold: '\
                                         '{:.2f} < {:.2f}'.format(mean_reward, reward_threshold)
    if return_episode_rewards:
        return episode_rewards, episode_lengths, totalwin
    return mean_reward, std_reward, totalwin


def og_load_driving_agent_make_video(pelican_agent_filepath, pelican_agent_name, panther_agent_filepath, panther_agent_name, config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',video_path='/Components/plark_ai_flask/builtangularSite/dist/assets/videos'):
    """
    Method for loading and agent, making and environment, and making a video. Mainly used in notebooks. 
    """
    logger.info("Load driving agent make viedo - pelican agent filepast = " + pelican_agent_filepath)
    basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    video_file = basicdate+'.mp4' 
    video_file_path = os.path.join(video_path, video_file) 
    os.makedirs(video_path, exist_ok=True)
    files = os.listdir(pelican_agent_filepath)
    if len(files) > 0:
        for f in files:
            if '.zip' in f:
                # load model
                metadata_filepath = os.path.join(pelican_agent_filepath, 'metadata.json')
                agent_filepath = os.path.join(pelican_agent_filepath, f)
                

                with open(metadata_filepath) as f:
                    metadata = json.load(f)
                logger.info('Playing against:'+agent_filepath)	
                if metadata['agentplayer'] == 'pelican':	
                    pelican_agent = classes.Pelican_Agent_Load_Agent(agent_filepath, metadata['algorithm'])
                    pelican_model = pelican_agent.model

                    env = plark_env.PlarkEnv(driving_agent='pelican',panther_agent_filepath=panther_agent_filepath, panther_agent_name=panther_agent_name, config_file_path=config_file_path)
                    basewidth,hsize = make_video(pelican_model,env,video_file_path)
                    logger.info("This is the environment variable " + str(env))

                elif metadata['agentplayer'] == 'panther':
                    raise ValueError('No Pelican agent found in ', pelican_agent_filepath) 
            
    else:
        raise ValueError('no agent found in ', files)

    return video_file, env.status,video_file_path

def load_driving_agent_make_video(pelican_agent_filepath, pelican_agent_name, panther_agent_filepath, panther_agent_name, config_file_path='/Components/plark-game/plark_game/game_config/10x10/balanced.json',video_path='/Components/plark_ai_flask/builtangularSite/dist/assets/videos',basic_agents_filepath='/Components/plark-game/plark_game/agents/basic',  renderWidth=None, renderHeight=None):
    """
    Method for loading and agent, making and environment, and making a video. Mainly used from flask server.
    """
    basicdate = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    video_file = basicdate+'.mp4' 
    video_file_path = os.path.join(video_path, video_file) 
    os.makedirs(video_path, exist_ok=True)

    kwargs = {
    'driving_agent': "pelican",
    'panther_agent_filepath': panther_agent_filepath,
    'panther_agent_name': panther_agent_name,
    }

    game_env = classes.Environment()
    game_env.createNewGame(config_file_path, **kwargs)
    game = game_env.activeGames[len(game_env.activeGames)-1]
    
    agent = classes.load_agent(pelican_agent_filepath,pelican_agent_name,basic_agents_filepath,game,**kwargs)

    if renderHeight is None:
        renderHeight = game.pelican_parameters['render_height']
    if renderHeight is None:
        renderWidth = game.pelican_parameters['render_width']
    
    basewidth, hsize = new_make_video(agent, game, video_file_path, renderWidth, renderHeight)

    return video_file, game.gameState ,video_file_path


def make_video(model,env,video_file_path,n_steps = 10000,fps=10,deterministic=False,basewidth = 512,verbose =False):
    # Test the trained agent
    # This is when you have a stable baselines model and an gym env
    obs = env.reset()
    writer = imageio.get_writer(video_file_path, fps=fps) 
    hsize = None
    for step in range(n_steps):
        image = env.render(view='ALL')
        action, _ = model.predict(obs, deterministic=deterministic)
        action = action.tolist()

        obs, reward, done, info = env.step(action)
        if verbose:
            logger.info("Step: "+str(step)+" Action: "+str(action)+' Reward:'+str(reward)+' Done:'+str(done))

        if hsize is None:
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
        res_image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        writer.append_data(np.copy(np.array(res_image)))
        if done:
            if verbose:
                logger.info("Goal reached:, reward="+ str(reward))
            break
    writer.close()  
    return basewidth,hsize      
    
def new_make_video(agent,game,video_file_path,renderWidth, renderHeight, n_steps = 10000,fps=10,deterministic=False,basewidth = 512,verbose =False):
    # Test the trained agent
    # This is when you have a plark game agent and a plark game 
    game.reset_game()
    writer = imageio.get_writer(video_file_path, fps=fps) 
    hsize = None
    for step in range(n_steps):
        image = game.render(renderWidth, renderHeight, view='ALL')
        game_state_dict = game._state("PELICAN")
        action = agent.getAction(game_state_dict)
        game.game_step(action)
       
        if hsize is None:
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
        res_image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        writer.append_data(np.copy(np.array(res_image)))

        if game_state_dict['game_state'] == "PELICANWIN" or game_state_dict['game_state'] == "WINCHESTER" or game_state_dict['game_state'] == "ESCAPE": 
            break
    writer.close()  
    return basewidth,hsize  

