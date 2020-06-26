import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class Services {

    // TODO: this needs to be changed to 5000 when included in the docker container
    private gamehost = 'http://0.0.0.0:5000/';

    constructor(private httpClient: HttpClient) {
    }

    newGame(settings) {
        console.log('kwargs: ', settings);
        return this.httpClient.post('/new_game', {settings}, { responseType: 'blob' });
    }

    makeVideo(settings) {
        return this.httpClient.post<any>('/make_video', {settings}, {responseType: 'json'});
    }

    resetGame(date) {
        return this.httpClient.post('/reset_game', { date }, { responseType: 'blob' });
    }

    game_step(actionID) {
        return this.httpClient.post('/game_step', { action: actionID }, { responseType: 'blob' });
    }

    updateView(view) {
        return this.httpClient.post('/output_view', { view }, { responseType: 'blob' } );
    }

    getAgents() {
        return this.httpClient.get('/get_agents');
    }

    getAgentJson(filepath) {
        return this.httpClient.post('/get_agent_json', { filepath });
    }

    getGameConfigs() {
        return this.httpClient.get('/get_game_configs');
    }

    getConfigJson(configPath) {
        return this.httpClient.post('/get_config_json', {configPath});
    }
}
