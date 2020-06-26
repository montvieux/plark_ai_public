*** Settings ***
Library  SeleniumLibrary

*** Keywords ***
Up Arrow
    Click Button  id=up

Down Arrow
    Click Button  id=down

Up Left Arrow
    Click Button  id=up_left

Up Right Arrow 
    Click Button  id=up_right
    
Down Right Arrow 
    Click Button  id=down_right

Down Left Arrow
    Click Button  id=down_left

Click End Turn
    Click Button  id=end_turn

Click Reset Game 
    Click Button  id=reset_game