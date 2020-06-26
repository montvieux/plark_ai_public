import { Component, OnInit, Input } from '@angular/core';
import { Services } from '../../services/services';
import { DomSanitizer } from '@angular/platform-browser';
import { NgbModalConfig, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { async } from '@angular/core/testing';

@Component({
  selector: 'app-game-view',
  templateUrl: './game-view.component.html',
  styleUrls: ['./game-view.component.scss']
})
export class GameViewComponent implements OnInit {

  image;
  video;
  videoResults;
  gameSettings;
  drivingAgent;
  gameEndState;
  agentVsAgent;

  gameResultMessage; // You lost / you won
  gameResultReasonMessage; //You were hit with a torpedo.

  gameResults = [
    ['BINGO', 'The aircraft must return to base through lack of fuel'],
    ['WINCHESTER', 'The aircraft has dropped all its torpedoes, and all torpedoes in the water have finished running'],
    ['ESCAPE', 'The submarine escaped over the top edge of the map'],
    ['PELICANWIN', 'The panther has been sunk']
  ];

  pelicanWin = [
    'PELICANWIN'
  ];

  pantherWin = [
    'BINGO',
    'WINCHESTER',
    'ESCAPE'
  ];

  constructor(private gameServices: Services, private sanitizer: DomSanitizer, config: NgbModalConfig, private modalService: NgbModal) {
  }
  @Input()
  set gameSettingsInput(gameSettingsInput) {
    this.gameSettings = gameSettingsInput;
    this.drivingAgent = this.gameSettings.kwargs.find(i => i[0] === 'driving_agent')[1];
    this.agentVsAgent = (this.gameSettings.kwargs.find(i => i[0] === 'panther_agent_name') && this.gameSettings.kwargs.find(i => i[0] === 'pelican_agent_name'))
  }

  ngOnInit() {
    this.newGame();
    console.log('game settings: ', this.gameSettings);
  }

  action(actionID) {
    this.gameServices.game_step(actionID).subscribe(async (imageData) => {
      let objectURL;
      if (imageData.type === "application/json") {
        let game_Json = await new Response(imageData).json();
        this.gameEndState = game_Json.gameState;
        this.gameEndMessage();
        objectURL = URL.createObjectURL(this.dataURItoBlob(game_Json.image));

      } else {
        objectURL = URL.createObjectURL(imageData);
      }
      this.image = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });
  }

  newGame() {

    this.gameEndState = null;
    this.image = null;
    this.video = null;
    this.videoResults = null;

    if (this.agentVsAgent) {
      this.gameServices.makeVideo(this.gameSettings).subscribe(data => {
        console.log('data: ', data);
        this.video = data.videoURL;
        this.videoResults = data.gameState;
      });
    } else {
      this.gameServices.newGame(this.gameSettings).subscribe((data) => {
        let objectURL = URL.createObjectURL(data);
        this.image = this.sanitizer.bypassSecurityTrustUrl(objectURL);
      });
    }
  }

  resetGame() {
    this.gameEndState = null;
    this.image = null;
    this.video = null;
    this.videoResults = null;


    if (this.agentVsAgent) {
      this.gameServices.makeVideo(this.gameSettings).subscribe(data => {
        console.log('data: ', data);
        this.video = data.videoURL;
        this.videoResults = data.gameState;
      });
    } else {
      let date = new Date();
      this.gameServices.resetGame(date).subscribe((data) => {
        let objectURL = URL.createObjectURL(data);
        this.image = this.sanitizer.bypassSecurityTrustUrl(objectURL);
      });
    }
  }

  showResults() {
    this.gameEndState = this.videoResults;
    this.gameEndMessage();
  }

  viewChange(event) {
    this.gameServices.updateView(event.target.value).subscribe((data) => {
      let objectURL = URL.createObjectURL(data);
      this.image = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });
  }

  open(content) {
    this.modalService.open(content);
  }

  dataURItoBlob(dataURI) {
    // take from https://medium.com/better-programming/convert-a-base64-url-to-image-file-in-angular-4-5796a19fdc21
    const byteString = window.atob(dataURI);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const int8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      int8Array[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([int8Array], { type: 'image/jpeg' });
    return blob;
  }

  gameEndMessage() {

    let result = this.gameResults.find(state => state[0] === this.gameEndState);

    if (this.agentVsAgent) {
      if (this.pelicanWin.includes(this.gameEndState)) {
        this.gameResultMessage = this.gameSettings.kwargs.find(i => i[0] === 'pelican_agent_name')[1] + ' wins!';
      } else if (this.pantherWin.includes(this.gameEndState)) {
        this.gameResultMessage = this.gameSettings.kwargs.find(i => i[0] === 'panther_agent_name')[1] + ' wins!';
      }
    } else {
      if (this.drivingAgent === 'pelican') {
        if (this.pelicanWin.includes(this.gameEndState)) {
          this.gameResultMessage = 'You win!';
        } else {
          this.gameResultMessage = 'You lost';
        }
      } else if (this.drivingAgent === 'panther') {
        if (this.pantherWin.includes(this.gameEndState)) {
          this.gameResultMessage = 'You win!';
        } else {
          this.gameResultMessage = 'You lost';
        }
      }
    }
    this.gameResultReasonMessage = result[1];
  }
}
