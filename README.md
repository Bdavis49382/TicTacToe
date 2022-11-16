# Overview

This game is a way to play tic tac toe with someone on a different computer.

In order to play the game, simply download the server.py file and run it. Then, whoever wants to play with you must download the client.py file and run it after changing the server ip address to your ip address, and the rest is history!


[Software Demo Video](https://youtu.be/PgjSsMKI4yk)

# Network Communication

I used a client/server type of connection rather than peer to peer

The program uses TCP and runs on port 5050

The messages sent between client and server are all preceded by a message describing the length of the following message. The server or client will print out the message, unless it is marked as a board message(which is what most of the messages in this game are) by having a b at the end, in which case it uses that new board to update the existing one in that program.
# Development Environment

This program was built on vscode, using python and it's socket and threading libraries.

# Useful Websites

* [Youtube tutorial](https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim)

# Future Work


* Add user interface instead of terminal
* Give the client a way to select a server, rather than hard coded