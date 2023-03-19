# Moonshot-Bridge-Program-with-RabbitMQ
A program to play Honeymoon bridge using messaging queues.

Project Moonshot: A Honeymoon Bridge program for two players

This code is a virtual version of Honeymoon Bridge, a two-player variant of the card game bridge. Instructions on how to play can be found at this link: 

https://ourpastimes.com/play-honeymoon-bridge-4709443.html

My version of the game has a couple of variations, namely that a) bidding is conducted before phase 1, and b) the top card of the deck is revealed each trick in phase 1, so the players know what they will get if they win the trick.

This code also serves as a demonstration of CloudAMQP's RabbitMQ messaging. It is through RabbitMQ that two players can use separate devices and still communicate with each other in the game. All the RabbitMQ-related functions are in the mshot.py file.

In order to use the program, first go to https://www.cloudamqp.com/, create an account, and create a RabbitMQ instance. Then, go to the instance overview by clicking on it, the copy the URL given on the website into the cloudAMPQ variable in the xplayer.py and xdealer.py files. Run xdealer.py first, then run xplayer.py twice to play!
