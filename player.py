#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, signal, copy
import mshot, mq
import time

# URL for CloudAMQP
cloudAMQP = sys.argv[1] # instance URL

def signalHandler(sig, frame):
    global playerChl, playerQ
    print('>>> control-c is received.')
    playerChl.queue_delete(playerQ)
    print(">>> Message Queue", playerQ, "is removed.")
    connection.close()
    print(">>> Connection to CloudAMQP is closed.")
    sys.exit(0)


# Set up a handler for SIGINT, so playerQ is deleted upon control-c
signal.signal(signal.SIGINT, signalHandler)


# Phase 0: Message Queue Setup

dealerQ='xdealer'
# Overwrite the default dealer queue by command line argumemnt if presents
if (len(sys.argv)>1):
    dealerQ=sys.argv[1]

playerQ='lunar' + mq.randomDigits(8)
print("Dealer Queue: " + dealerQ)
print("Player Queue: " + playerQ)

connection=mq.connSetup(cloudAMQP)
dealerChl=mq.qSetup(connection, dealerQ)
playerChl=mq.qSetup(connection, playerQ)

# Regsiter the player with the dealer.
playerName=input("Your name? ")
print()
outMsg=[playerName, playerQ]
mq.qSend(dealerChl, dealerQ, outMsg)



# Phase 1: Dealing

msg=mq.qReceive(playerChl, playerQ)
opponentName=msg[0]
hand=msg[1]
print("Opponent: ", opponentName)
print()
print("Your cards:")
print(mshot.showCards(hand, 2, True))



# Phase 2: Bidding
print ('bidding phase:')


msg=mq.qReceive(playerChl, playerQ)
opponentQ = msg
print ('opponents message queue:' + opponentQ)

player = '1'
currentBid = 'n'

while True:
    print()
    print ('Please wait for bidding prompt...')
    msg=mq.qReceive(playerChl, playerQ)
    op = msg[0]
    extra = msg[1:]
    if op == '0':
        extra = mshot.split_string(extra)
        cards = mshot.decodeCards(extra[0])
        mshot.showCards(cards, 2, True)
        player = '0'
        if extra[0] == '0':
            Bid = mshot.Biddy('00')
            currentBid = copy.deepcopy(mshot.decodeBid(Bid))
            mq.qSend(playerChl, opponentQ, '1'+Bid)
    if op == '1':
        if extra == "n" and currentBid != "n":
            print()
            print("You won the bidding phase with a bid of " + str(currentBid) + ".")
            contractPlayer = True
            break
            
        else:
            extra1 = mshot.decodeBid(extra)
            print ("Opponent's bid:  " + extra1)
            currentBid = copy.deepcopy(extra1)
            Bid = mshot.Biddy(extra)
            mq.qSend(playerChl, opponentQ, '1'+Bid)
        if Bid != "n":
            currentBid = copy.deepcopy(mshot.decodeBid(Bid))
        if Bid == "n" and currentBid != "n":
            print()
            print("Your opponent won the bidding phase with a bid of " + str(currentBid) + ".")
            mq.qSend(dealerChl, dealerQ, player + extra)
            print ('sent:')
            print (player + extra)
            contractPlayer = False
            break
            
        if Bid == "n" and currentBid == "n":
            print()
            print("Ah, well, I guess we'll have to restart the dealing now. What an inconvenience.")
contract = mq.qReceive(playerChl, playerQ)



# Phase 3: Drawing

wildCard=[0, 0]




for i in range (1, 14):
    print()
    print("> Drawing:  Trick", i)
    # Temporary fix: refresh the player channel
    # playerChl=mq.qSetup(connection, playerQ)

    inMsg=mq.qReceive(playerChl, playerQ)
    print("The reward card:  " + mshot.showCards([inMsg[0]], 2, True))
    if inMsg[1]==wildCard:
        print("You are leading.")
    else:
        print("Opponent's card:  " + mshot.showCards([inMsg[1]], 2, True))

    output = mshot.availableChoices(hand, inMsg[1])
    outMsg = [output[0]]
    hand = output[1]
    print("Card sent:  " + mshot.showCards(outMsg, 2, True))
    mq.qSend(dealerChl, dealerQ, outMsg)

    # inMsg=[win (0 or 1), opponent's card, card acquired]
    inMsg=mq.qReceive(playerChl, playerQ)
    print("Opponent's move:  " + mshot.showCards([inMsg[1]], 2, True))
    print()
    print("Card received:  " + mshot.showCards([inMsg[2]], 2, True))
    hand = hand + [inMsg[2]]
    
# Phase 4: Playing
wildCard = [0, 0]
tricksWon = 0
tricksLost = 0
win = 0

for i in range (1, 14):
    print()
    print("> Playing:  Trick", i)
    # Temporary fix: refresh the player channel
    # playerChl=mq.qSetup(connection, playerQ)

    inMsg=mq.qReceive(playerChl, playerQ)
    if inMsg[0]== [0, 0]:
        print("You are leading.")
    else:
        print("Opponent's card:  " + mshot.showCards([inMsg[0]], 2, True))

    output = mshot.availableChoices(hand, inMsg[0])
    outMsg = [output[0]]
    hand = output[1]
    print("Card sent:  " + mshot.showCards(outMsg, 2, True))
    mq.qSend(dealerChl, dealerQ, outMsg)

    # inMsg=[win (0 or 1), opponent's card, card acquired]
    inMsg=mq.qReceive(playerChl, playerQ)
    print("Opponent's move:  " + mshot.showCards([inMsg[1]], 2, True))
    if inMsg[0] == 1:
        tricksWon = tricksWon + 1
        if contractPlayer == True:
            tricksLeft = contract[1] + 6 - tricksWon
        if contractPlayer == False:
            tricksLeft = 7 - contract[1] - tricksWon
        if win == 0:
            if tricksLeft > 1:
                print()
                print("You won this trick. You only need to win " + str(tricksLeft) + 
              " more tricks in order to win the game!")
            if tricksLeft == 1:
                print()
                print("You won this trick. You only need to win " + str(tricksLeft) + 
              " more trick in order to win the game!")
            if tricksLeft <= 0:
                win = 1
                print()
                print("You won this trick, as well as the game! Don't just stop trying, though. See how many tricks you can get!")
        if win == 1:
            print()
            print("You won this trick. It's good that you're still trying!")
        if win == -1:
            print()
            print("You won this trick. It's good that you didn't give up!")
    if inMsg[0] == 0:
        tricksLost = tricksLost + 1
        if contractPlayer == True:
            tricksLeft = 7 - contract[1] - tricksLost
        if contractPlayer == False:
            tricksLeft = 6 + contract[1] - tricksLost
        if win == 0:
            if tricksLeft > 1:
                print()
                print("You lost this trick. You can only afford to lose " + str(tricksLeft) +
              " more tricks.")
            if tricksLeft == 1:
                print()
                print("You lost this trick. You can only afford to lose " + str(tricksLeft) +
              " more trick.")
            if tricksLeft == 0:
                print()
                print("You lost this trick. You cannot afford to lose any more tricks.")
            if tricksLeft < 0:
                win = -1
                print()
                print("You lost this trick, as well as the game. Better luck next time! Don't just stop trying, though. See how many tricks you can still steal from your opponent!")
        if win == 1:
            print()
            print("You lost this trick. I hope you're still trying...")
        if win == -1:
            print()
            print("You lost this trick. I hope you didn't give up...")

# Phase 5: Ending
if contractPlayer == True:
    if tricksWon >= 6 + contract[1]:
        print()
        print("You won the game! Congratulations!")
    if tricksWon < 6 + contract[1]:
        print()
        print("You lost the game. Better luck next time!")
if contractPlayer == False:
    if tricksWon > 7 - contract[1]:
        print()
        print("You won the game! Congratulations!")
    if tricksWon <= 7 - contract[1]:
        print()
        print("You lost the game. Better luck next time!")      
playerChl.queue_delete(playerQ)
connection.close()
sys.exit()
