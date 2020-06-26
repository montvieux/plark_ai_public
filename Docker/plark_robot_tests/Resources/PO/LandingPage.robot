*** Settings ***
Library  SeleniumLibrary

*** Variables ***


*** Keywords ***
Load
    Go To  http://172.20.128.2:5000/

Verify Page Loaded
    Wait Until Page Contains  Hunting the Plark

Click Config Page Tab
    Click Element  id=ngb-nav-1

Click Pelican Controller Drop Down
    Click Element  id=pelicanController

Select Human Pelican 
    Click Element  id=human_pelican

Select Agent Pelican    
    Click Element  id=agent_pelican
    
Click Pelican Pretrained Agent Drop down
    Click Element  id=pelicanAgent

Select Pelican with 5 Bouys 
    Click Element  css=#pelicanAgent > option:nth-child(1)

Select Pelican with 3 Bouys 
    Click Element  css=#pelicanAgent > option:nth-child(2)

Click Panther Controller Drop Down 
    Click Element  id=pantherController

Select Human Panther
    Click Element  id=human_panther

Select Agent Panther
    Click Element  id=agent_panther

Click Start Game
    Click Button  id=start_game
