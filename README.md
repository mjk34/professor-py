# uwuBot

## Summary:
This is the coding behind Uwuversity's Professor bot for Discord.

Professor bot is a developing agent that is currently used to reward community members based on in game achievements and daily participation. Members are currently able to submit Valorant game scores to earn uwuCreds, a community resource that can be used for trade, expression as well as participate in the ongoing raffles.

Professor bot manages and evaluates resources through it's locally maintained centralized blockchain where each recorded action is a transaction block that can be used to result in something meaningful. Professor bot was first built with a MongoDB backend, but a personal interest in blockchain structure pushed me to rework it. 

After reworking the available services around the centralized blockchain structure, I can say that it actually simplified the complexity of some of the services, and if anything, it was exciting to see the features in a new light.

## Install

pip3 install -r requirements.txt

## Current Development Branches:
  - [ ] main

## Past Development Branches:
  - [x] blockChain     # Rework the backend MongoDB dependency to a blockchain structure
  - [x] refactor       # Simplify duplication code and add in documentation to improve clarity
  - [x] slashcmd       # Upgrade Professor's features to slashcommands
  - [x] uwufy          # Implement message filtering to make user messages more "kawaii" 
