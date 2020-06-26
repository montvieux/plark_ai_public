*** Settings ***
Library  SeleniumLibrary

*** Keywords ***

Click config dropdown 
    Click Element  id=config_Selector

Select a config 
    Click Element  css=#config_Selector
    