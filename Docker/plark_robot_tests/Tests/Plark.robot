*** Settings ***
Documentation  This is some basic info about the whole suite
Resource  ../Resources/Common.robot  # necessary for Setup & Teardown
Resource  ../Resources/PlarkApp.robot  # necessary for lower level keywords in test cases
Test Setup  Begin Web Test
Test Teardown  End Web Test

# Copy/paste the below line to Terminal window to execute
# robot -d results Tests/Plark.robot

*** Test Cases ***
User can navigate to the Hunting the Plark webpage
    [Tags]  Smoke
    PlarkApp.Load Webpage
    Sleep  3s

User can navigate to config Page and select a config
    PlarkApp.Load Webpage
    PlarkApp.Choose a config
    Sleep  3s
    
User can select an agent to train with and start a game
    [Tags]  Smoke
    PlarkApp.Load Webpage
    PlarkApp.Select an agent and go to game screen
    Sleep  3s

User has control over the game 
    PlarkApp.Load Webpage
    PlarkApp.Select an agent and go to game screen
    Sleep  10s
    PlarkApp.Use direction buttons
    Sleep  3s
    PlarkApp.Use direction buttons
    Sleep  3s
    PlarkApp.Use direction buttons
    Sleep  3s
    PlarkApp.End a game  
    Sleep  3s
    PlarkApp.Reset the game
    Sleep  3s



