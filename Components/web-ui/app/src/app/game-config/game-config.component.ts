import { Component, OnInit, ViewChild, Output, EventEmitter } from '@angular/core';
import { NgForm, FormGroup, FormControl, Validators } from '@angular/forms';

import { Services } from '../../services/services';

@Component({
  selector: 'app-game-config',
  templateUrl: './game-config.component.html',
  styleUrls: ['./game-config.component.scss']
})


export class GameConfigComponent implements OnInit {

  // game_config: FormObject
  // @ViewChild('gameSettings', { static: false }) gameSettings: NgForm;
  @Output() activateGame = new EventEmitter();

  gameSettings = new FormGroup({
    pantherController: new FormControl('Human'),
    pantherAgent: new FormControl('default'),
    pelicanController: new FormControl('Agent'),
    pelicanAgent: new FormControl('default'),
    config: new FormControl('default')
  });

  pelicanAgents;
  pantherAgents;

  pelicanAgentJson;
  pantherAgentJson;

  configs;
  configJson;

  constructor(private gameServices: Services) { }

  ngOnInit() {
    this.gameServices.getAgents().subscribe((data: Array<any>) => {
      this.pelicanAgents = data.filter(agent => agent.agent_type === 'pelican');
      this.pantherAgents = data.filter(agent => agent.agent_type === 'panther');
    });

    this.gameServices.getGameConfigs().subscribe((data: Array<any>) => {
      this.configs = data;
    });
  }

  start_game() {
    let kwargs = [];
    // Human panther player
    if (this.gameSettings.value.pantherController === 'Human') {
      kwargs.push(['driving_agent', 'panther']);

      // load agent if specified
      if (this.gameSettings.value.pelicanAgent !== 'default') {
        let tmp_agent = this.pelicanAgents.find(agent => agent.name === this.gameSettings.value.pelicanAgent);
        kwargs.push(['pelican_agent_filepath', tmp_agent.filepath]);
        kwargs.push(['pelican_agent_name', tmp_agent.name]);
      }

      // Human pelican player
    } else if (this.gameSettings.value.pelicanController === 'Human') {
      kwargs.push(['driving_agent', 'pelican']);

      // load agent if specified
      if (this.gameSettings.value.pantherAgent !== 'default') {
        let tmp_agent = this.pantherAgents.find(agent => agent.name === this.gameSettings.value.pantherAgent);
        kwargs.push(['panther_agent_filepath', tmp_agent.filepath]);
        kwargs.push(['panther_agent_name', tmp_agent.name]);
      }

      // agent vs agent
    } else {

      // load pelican agent if specified
      kwargs.push(['driving_agent', 'pelican']);
      if (this.gameSettings.value.pelicanAgent !== 'default') {
        let pelicanAgent = this.pelicanAgents.find(agent => agent.name === this.gameSettings.value.pelicanAgent);
        kwargs.push(['pelican_agent_filepath', pelicanAgent.filepath]);
        kwargs.push(['pelican_agent_name', pelicanAgent.name]);
      }

      // load panther agent if specified
      if (this.gameSettings.value.pantherAgent !== 'default') {
        let pantherAgent = this.pantherAgents.find(agent => agent.name === this.gameSettings.value.pantherAgent);
        kwargs.push(['panther_agent_filepath', pantherAgent.filepath]);
        kwargs.push(['panther_agent_name', pantherAgent.name]);
      }
    }

    // load game config if specified then emit to start the game
    if (this.gameSettings.value.config !== 'default') {
      this.activateGame.emit({
        "kwargs": kwargs,
        "config_file_path": this.gameSettings.value.config
      });
    } else {
      this.activateGame.emit({
        "kwargs": kwargs
      });
    }

  }

  pantherAgentchange() {
    this.pantherAgentJson = null;
    let agent = this.pantherAgents.filter(a => a.name === this.gameSettings.value.pantherAgent)[0];

    if (agent.filepath.includes('.py')) {
      this.pantherAgentJson = {
        "agentplayer": "panther",
        "algorithm": "Basic agent"
      }
    } else {
      this.gameServices.getAgentJson(agent.filepath).subscribe((data) => {
        this.pantherAgentJson = data;
      });
    }
  }

  pelicanAgentchange() {
    this.pelicanAgentJson = null;
    let agent = this.pelicanAgents.filter(a => a.name === this.gameSettings.value.pelicanAgent)[0];

    if (agent.filepath.includes('.py')) {
      this.pelicanAgentJson = {
        "agentplayer": "pelican",
        "algorithm": "Basic agent"
      }
    } else {
      this.gameServices.getAgentJson(agent.filepath).subscribe((data) => {
        this.pelicanAgentJson = data;
      });
    }
  }

  configChanged() {
    this.gameServices.getConfigJson(this.gameSettings.value.config).subscribe((data) => {
      this.configJson = data;
    });
  }
}


