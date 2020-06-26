import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Hunting the plark';

  activeGame;
  gameSettings;
  constructor() { }

  ngOnInit() {
  }

  activateGame(event) {
    this.activeGame = true;
    this.gameSettings = event;
    console.log('gameSettings: ', this.gameSettings);
  }

}
