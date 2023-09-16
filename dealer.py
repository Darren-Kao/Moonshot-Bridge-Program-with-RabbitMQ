#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, signal, random, time
import mshot, mq

# URL for CloudAMQP
cloudAMQP = sys.argv[1] # Instance URL

def signalHandler(sig, frame):
    global dealerChl, dealerQ
    print('>>> control-c is received.')
    dealerChl.queue_delete(dealerQ)
    print(">>> Message Queue", dealerQ, "is removed.")
    connection.close()
    print(">>> Connection to CloudAMQP is closed.")
    sys.exit(0)



# Set up a handler for SIGINT, so dealQ is deleted upon control-c
signal.signal(signal.SIGINT, signalHandler)

print(sys.version)
print()


# Declarations
dealerQ='xdealer'
playerName=[0, 0]
playerQ=[0, 0]
playerChl=[0, 0]
playerHand=[0, 0]



# Phase 0: Message Queue Setup

print("-- Phase 0: Message Queue Setup ---")

# Overwrite the default dealer queue by command line argumemnt if presents
if (len(sys.argv)>1):
    dealerQ=sys.argv[1]

print("Dealer Queue: " + dealerQ)

connection=mq.connSetup(cloudAMQP)
dealerChl=mq.qSetup(connection, dealerQ)

for i in range (2):
    msg=mq.qReceive(dealerChl, dealerQ)
    playerName[i]=msg[0]
    playerQ[i]=msg[1]
    print("Player", i, playerName[i], playerQ[i])
    playerChl[i]=mq.qSetup(connection, playerQ[i])

print()



# Phase 1: Dealing

print("-- Phase 1: Dealing ---")

deck=mshot.getDeck()
random.shuffle(deck)
playerHand[0] = mshot.deal(deck, 1)
playerHand[1] = mshot.deal(deck, 2)
stock = mshot.deal(deck, 3)

for i in range(2):
    print("Player", i)
    print(mshot.showCards(playerHand[i], 2, True))
    msg=[playerName[1-i], playerHand[i]]
    mq.qSend(playerChl[i], playerQ[i], msg)
print("Stock")
print(mshot.showCards(stock, 2, False))

print()



# Phase 2: Bidding

print("-- Phase 2: Bidding ---")
time.sleep(3)

outMsg = playerQ[1]
# print ('player0'+outMsg)
mq.qSend(playerChl[0], playerQ[0], outMsg)   

outMsg = playerQ[0]
# print ('player1'+outMsg)
mq.qSend(playerChl[1], playerQ[1], outMsg)   

time.sleep(3)


outMsg = '00'
mq.qSend(playerChl[0], playerQ[0], outMsg) 
print ('prompted player 0 to start bidding...')
msg = mq.qReceive(dealerChl, dealerQ)

player = msg[0]
card = [msg[1],msg[2]]
# print (card) 

if player == '0':
    player = '1'
elif player == '1':
    player = '0'

contract=[int(player), int(card[0]), int(card[1])]
print ('Contract:', contract)
# At the end of bidding phase, the contract variable needs to be set.
# contract=[player, level, trump]
# The player getting the contract needs to win 6+level tricks to win.
# For ease of testing, it is hard coded for now:
# Player 1 gets the contract at 3-Diamond.
mq.qSend(playerChl[0], playerQ[0], contract) 
mq.qSend(playerChl[1], playerQ[1], contract) 

# Phase 3: Drawing

print("-- Phase 3: Drawing ---")

wildCard=[0, 0]
cards=[0, 0]
lead=contract[0]
trump=contract[2]

for i in range (1, 14):
    print("> Drawing: Trick", i)
    # Temporary fix: refresh the player channels
    for i in range(2):
        playerChl[i]=mq.qSetup(connection, playerQ[i])
    
    faceCard=stock.pop(0)
    drawCard=stock.pop(0)

    outMsg=[faceCard, wildCard]
    mq.qSend(playerChl[lead], playerQ[lead], outMsg)
    inMsg=mq.qReceive(dealerChl, dealerQ)
    cards[lead]=inMsg[0]

    outMsg=[faceCard, cards[lead]]
    mq.qSend(playerChl[1-lead], playerQ[1-lead], outMsg)
    inMsg=mq.qReceive(dealerChl, dealerQ)
    cards[1-lead]=inMsg[0]

    lead=mshot.compareCards(cards[0], cards[1], lead, trump)

    # outMsg=[win (0 or 1), opponent's card, card acquired]
    outMsg=[1, cards[1-lead], faceCard]
    mq.qSend(playerChl[lead], playerQ[lead], outMsg)
    outMsg=[0, cards[lead], drawCard]
    mq.qSend(playerChl[1-lead], playerQ[1-lead], outMsg)



    
# Phase 4: Playing

print("-- Phase 4: Playing ---")

wildCard=[0, 0]
cards=[0, 0]
lead = contract[0]
trump=contract[2]

for i in range (1, 14):
    print("> Playing: Trick", i)
    # Temporary fix: refresh the player channels
    for i in range(2):
        playerChl[i]=mq.qSetup(connection, playerQ[i])

    outMsg=[wildCard]
    mq.qSend(playerChl[lead], playerQ[lead], outMsg)
    inMsg=mq.qReceive(dealerChl, dealerQ)
    cards[lead]=inMsg[0]

    outMsg=[cards[lead]]
    mq.qSend(playerChl[1-lead], playerQ[1-lead], outMsg)
    inMsg=mq.qReceive(dealerChl, dealerQ)
    cards[1-lead]=inMsg[0]

    lead=mshot.compareCards(cards[0], cards[1], lead, trump)

    # outMsg=[win (0 or 1), opponent's card, card acquired]
    outMsg=[1, cards[1-lead]]
    mq.qSend(playerChl[lead], playerQ[lead], outMsg)
    outMsg=[0, cards[lead]]
    mq.qSend(playerChl[1-lead], playerQ[1-lead], outMsg)


# Phase 5: Ending

print("-- Phase 5: Ending ---")

dealerChl.queue_delete(dealerQ)
connection.close()
sys.exit()


    
    
