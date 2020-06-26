FROM plark_ai

ADD Components/agent-training/ /Components/agent-training/
ADD Components/gym-plark/ /Components/gym-plark/
ADD Components/plark_ai_flask/ /Components/plark_ai_flask/
ADD Components/plark-game/ /Components/plark-game/
ADD Components/stable-baselines/ /Components/stable-baselines/
ADD Components/web-ui/ /Components/web-ui/
ADD data /data/

RUN pip install -e /Components/plark-game
RUN pip install -e /Components/gym-plark
RUN pip install -e /Components/agent-training

# Do something random to ensure the tests are run
# ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache 
ARG CACHEBUST=1 
RUN echo "$CACHEBUST"

RUN pytest -v /Components/plark-game/plark_game 
RUN pytest -v /Components/agent-training/agent_training
