*** Settings ***
Resource  PO/ConfigPage.robot
Resource  PO/GamePage.robot
Resource  PO/LandingPage.robot


*** Keywords ***
Load Webpage
    LandingPage.Load
    LandingPage.Verify Page Loaded

Choose a config
    LandingPage.Click Config Page Tab
    ConfigPage.Click config dropdown 
    ConfigPage.Select a config 

Select an agent and go to game screen
    LandingPage.Click Pelican Pretrained Agent Drop down
    LandingPage.Select Pelican with 5 Bouys  
    LandingPage.Click Start Game

Use direction buttons
    GamePage.Up Arrow
    GamePage.Up Left Arrow
    GamePage.Up Right Arrow 
    GamePage.Down Right Arrow 
    GamePage.Down Left Arrow
    GamePage.Down Arrow

End a game 
    GamePage.Click End Turn

Reset the game 
    GamePage.Click Reset Game



    

    




