#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, copy
from sys import exit

# ***************************
# *** Phase 0.0 Functions ***

# mshot.py
# getDeck(): generate a deck of 52 cards
# deck: a list of 52 items
# item format: [suit, rank]
# suit: (0, 1, 2, 3) = (Spade, Heart, Diamond, Club)
# rank: (2, ..., 10, 11, 12, 13, 14) = (2, ..., 10, Jack, Queen, King, Ace)
def getDeck():
    deck=[]
    for i in range(0, 4):
        for j in range (2, 15):
            deck = deck + [[i, j]]
    return deck


def split_string(str):
    currentstring = ''
    lst = []
    for i in str:
        if i == ' ':
            lst.append(currentstring)
            currentstring = ''
        else:
            currentstring += i
    lst.append(currentstring)
    return lst

# mshot.py
# deal(deck): deal a deck of 52 cards for a game of Honeymoon Draw Bridge
# player1: 13 cards
# player2: 13 cards
# stock: 26 cards
def deal(deck, n):
    if n == 1:
        p1 = []
        for i in deck[0:13]:
            p1.append(i)
        return p1
    elif n == 2:
        p2 = []
        for i in deck[13:26]:
            p2.append(i)
        return p2
    elif n == 3:
        stock = []
        for i in deck[26:53]:
            stock.append(i)
        return stock

# mshot.py
# symbol(num, s): determine which symbol will be displayed for each card
# num: determines which shape to use
# s=0 - use unicode black symbols for suits
# s=1 - use unicode white (outlined) symbols for suits
# s=2 - use unicode mixed black/while symbols for suits
def symbol(num, s):
    ref = [[0, 0, '♠'], [0, 1, '♤'], [0, 2, '♠'], [1, 0, '♥'], [1, 1, '♡'], [1, 2, '♡'], [2, 0, '♦'], [2, 1, '♢'], [2, 2, '♢'], [3, 0, '♣'], [3, 1, '♧'], [3, 2, '♣']]
    for i in ref:
        if i[0] == num and i[1] == s:
            return i[2]

# mshot.py
# showCards(cards, symbol): print a complete or partial deck of cards in its
#                original sequence in an easy to read format
# disp: what will end up being printed, with values appended to a list to show
#                             up on the same line
# conversions: contains lists that associate the numerical value with the true
# face card names 
# x: calls the function symbol in order to determine what character to use,
# with i[0] containing the suit number and carrying over the initial sym number
#          that corresponds to what color the characters will be
# a: the string value of the card's number
# card of 11 or higher is a face card (Jack, Queen, King, Ace)
# a: whitespace that will be inserted between the displays
# disp2: adds whitespace between each value of disp in order to make it easier
#                        to see the individual cards
def showCards(cards, sym, sort):
    if sort == True:
        cards.sort()
    disp = []
    for i in cards:
        conversions = {11:'J', 12:'Q', 13:'K', 14:'A'}
        x = symbol(i[0], sym)
        a = str(i[1])
        b = i[1]
        if b > 10:
            a = conversions[b]
        disp.append(a+str(x))
    a = '  '
    disp2 = a.join(disp)
    return disp2

# mshot.py
# encodeCards(cards)
# Encode a list of cards into a string to be sent through a message queue
# c: the string of the encoded cards
# the cards are encoded in a format snn.snn. ... with s being the suit number
#                      and n being the card number
def encodeCards(cards):
    c = ''
    for i in cards:
        c += str(i[0]) + '%02d' % i[1] + '.'
    return c

# mshot.py
# orderCards(cards, n): orders cards by suit or number
# secondElement(cards): returns the second element of the list
# n=0: have cards of the same suit together, ascending in numerical order
# n=1: have cards of the same number together, in suit order
def secondElement(cards):
    return cards[1]
def orderCards(cards, n):
    if n == 0:
        cards.sort()
        return cards
    if n == 1:
        cards.sort(key=secondElement)
        return cards
    else:
        pass

# mshot.py
# encodeCards(cards)
# Decode a message encoded by encodeCards(cards) and construct a list of cards
# counter: determines what function each character has
# deck: the final list with cards in [suit, num] form
# a: the stored suit number
# b: first digit of card number
# c: second digit of card number
# NOTE: the periods cause the entire card to be processed, so there MUST be a
#          period after the last card for that one to be included
def decodeCards(msg):
    counter = 0
    deck = []
    for i in msg:
        if counter == 0:
            a = i
            counter = 1
        elif counter == 1:
            b = i
            counter = 2
        elif counter == 2:
            c = i
            counter = 3
        elif counter == 3:
            deck.append([int(a), int(str(b)+str(c))])
            counter = 0
    return deck



# mshot.py
# enforceRules(move)
# enforces rules so nobody can play an illegal move
def enforceRules(move, precursor):
    if move == "n" or precursor == "n":
        return True
    move = [int(move[0]), int(move[1])]
    precursor = [int(precursor[0]), int(precursor[1])]
    if move[0] < precursor[0]:
        return False
    if move[0] == precursor[0]:
        if move[1] >= precursor[1] and move[1] != 4:
            return False
        if move[1] <= precursor[1] or move[1] == 4:
            if precursor[1] == 4:
                return False
            else:
                return True
    if move[0] > precursor[0]:
        return True


def Biddy(Extra):
    extra = Extra
    Bid = ''
    Bid = input('Do you want to bid [y/n]\n')
    
       
    
    if Bid == 'y':    
        print ('Please input the number of tricks you plan to win, minus six (for example, type 2 if you plan to win eight tricks)')
        Bid = input("Tricks:")
        if (Bid.isdigit()):
            Bid = int(Bid)
            if Bid <= 7 and Bid > 0:
                print ('Please select a trump or no trump')
                Bid = str(Bid)
                trump = input("Enter your desired trump. Type 'S' for spades, 'H' for hearts, 'D' for diamonds, 'C' for clubs, and 'N' for no trump.\n")
                trump = trump.lower()
                if trump == 's':
                    Bid = Bid[:1]
                    Bid = Bid + '0'
                elif trump == 'h':
                    Bid = Bid[:1]
                    Bid = Bid + '1'
                elif trump == 'd':
                    Bid = Bid[:1]
                    Bid = Bid + '2'
                elif trump == 'c':
                    Bid = Bid[:1]
                    Bid = Bid + '3'
                elif trump == 'n':
                    Bid = Bid[:1]
                    Bid = Bid + '4'
                else:
                    print ('Please write your selection exactly like the requirements.')
                    Bid = Biddy(extra)
            else:    
                print ('Please enter a valid input.')
                Bid = Biddy(extra)
        else:
            print ('Please enter a valid input.')
            Bid = Biddy(extra)
    elif Bid == 'n':
        Bid = 'n'
    else:
        print ('please input a valid input.')
        Bid = Biddy(extra)
    Rule = enforceRules(Bid, Extra)
    if Rule == False:
        print ('Invalid bid, please submit a new bid')
        Bid = Biddy(extra)
    return Bid

# Drawing Phase Codes ********************

# mshot.py
# xMsg(mqOut, mqIn, msgOut)
# Exchange a round of messages between two processes
# Input Parameters:
#  mqOut - output message queue name (routing key);
#          if unspecified (''), skip sending
#  mqIn - input message queue name (routing key)
#          if unspecified (''), skip receiving
#  msgOut - message as a list
# Return Values:
#  msgIn - message as a list
# Function Objectives:
#  - encodes msgOut and sends it to mqOut
#  - receives from mqIn and decodes it to msgIn
#  - return msgIn
def xMsg(mqOut, mqIn, msgOut):
    import pika, os, logging, time
    if mqOut != "":
        url = os.environ.get(
                    'CLOUDAMQP_URL',
                    'amqp://cjreuywj:G7MA6eSEAjr7jq6FHYb812EnZJDHo5o4@jaguar.rmq.cloudamqp.com/cjreuywj'
                    )
        params = pika.URLParameters(url)
        params.socket_timeout = 5
        
        connection = pika.BlockingConnection(params) # Connect to CloudAMQP
        channel = connection.channel() # start a channel
        channel.queue_declare(queue=mqOut) # Declare a queue
# send a message

    # print('Send: ' + outMsg)
    # Send message to the default exchange ''
        channel.basic_publish(exchange='',routing_key=mqOut,
                          # set per-message TTL in milliseconds 
                              properties=pika.BasicProperties(
                                          expiration='60000',
                                          ),
                              body=msgOut)
        print ('Message "' + msgOut + '" sent to "' + mqOut + '".')
        connection.close()
    if mqIn != "":
        inMsg = ""

# create a function to perform some work based on the message received
        def processFunction(msg):
            nonlocal inMsg
            print('Received "' + str(msg) + '" from "' + mqIn + '".')
            print(" Processing finished");
            #signal the start_consuming loop to exit
            inMsg = msg
            channel.stop_consuming()
            
# create a function which is called on incoming messages
        def callback(ch, method, properties, body):
        # convert message to UTF-8
            body=body.decode()
            processFunction(body)


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
        url = os.environ.get('CLOUDAMQP_URL',
                     'amqp://cjreuywj:G7MA6eSEAjr7jq6FHYb812EnZJDHo5o4@jaguar.rmq.cloudamqp.com/cjreuywj')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel() # start a channel
        # decalre an exchange here as needed; otherwise the default exchange is used
        # channel.exchange_declare(exchange='logs', exchange_type='fanout')
        channel.queue_declare(queue=mqIn) # Declare a queue


# set up subscription on the queue
        channel.basic_consume(mqIn, callback, auto_ack=True)

# start consuming (blocks)
        print(">> Start consuming")
        channel.start_consuming()
# delete the message queue upon exit
        channel.queue_delete(mqIn)
        connection.close()
        print(">> Connection closed")
        return inMsg

# if leadCard = (0,0) then the player has to lead
def cardDrawing(hand, faceCard, leadCard):
  faceCard=[1,2]
  leadCard=[3,4]
  hand=[[1,2],[2,3]]
  hand=hand.decode()
  print("Face up card:  " + str(faceCard))
  print("Your hand:  " + hand)
  faceCard=faceCard.decode()
  if leadCard != [0,0]:
      print("Opponent's move:  " + str(leadCard))
   # display the hand to the user
   # display the face card
   # if leadCard != (0,0) display the lead card
   # collect player's card
   # if follow-suit fails, collect player's card again (repeated as necessary)
  return hand

# Return status = FALSE when follow-suit fails
# return status = TRUE when follow-suit succeeds
def followSuit(hand, leadCard, followCard):
    i = 0
    while i < len(hand):
        if hand[i] == followCard:
            break
        i = i + 1
    if i == len(hand):
        return False
    if followCard[0]==leadCard[0]:
        return True
    else:
        return False
   #enforce follow-suit rule

#this is to compare cards
def compareCards(p1Card, p2Card, lead, trump):
    print("Compare:" + str(p1Card) + str(p2Card))
    p1Card = [p1Card[0], p1Card[1], 0]
    p2Card = [p2Card[0], p2Card[1], 1]
    playerCards = [p1Card, p2Card]
    leadCard = playerCards.pop(lead)
    followCard = playerCards[0]
    if trump == 4:
        if leadCard[0] != followCard[0]:
            return leadCard[2]
        if leadCard[0] == followCard[0]:
            if leadCard[1] > followCard[1]:
                return leadCard[2]
            if leadCard[1] < followCard[1]:
                return followCard[2]
            if leadCard[1] == followCard[1]:
                print("Sorry, something has gone wrong with the code. The game is aborting.")
                exit()
    if trump != 4:
        if leadCard[0] != followCard[0]:
            if followCard[0] == trump:
                return followCard[2]
            if followCard[0] != trump:
                return leadCard[2]
        if leadCard[0] == followCard[0]:
            if leadCard[0] == followCard[0]:
                if leadCard[1] > followCard[1]:
                    return leadCard[2]
                if leadCard[1] < followCard[1]:
                    return followCard[2]
                if leadCard[1] == followCard[1]:
                    print("Sorry, something has gone wrong with the code. The game is aborting.")
                    exit()





def availableChoices(hand, leadCard):
    import mshot
    originalHand = copy.deepcopy(hand)
    def checkCards():
        nonlocal hand
        c = 0
        for i in hand:
            if leadCard == [0, 0]:
                break
            if i[0] != leadCard[0]:
                del hand[c]
                c = 0
                checkCards()
            c = c + 1
        if len(hand) == 0:
            hand = copy.deepcopy(originalHand)
    checkCards()
    follow = ""
    def promptCard():
        nonlocal follow
        print("Your hand:  " + mshot.showCards(originalHand, 2, True)) 
        print("Your possible moves:  " + mshot.showCards(hand, 2, True))
        print('Enter your move here. Enter from 1 to '
              + str(len(hand)) + '. "1" corresponds to the first card in your possible moves, "2" corresponds to the second card in your possible moves, etc.')
        number = input()
        if (number.isdigit()):
            follow = int(number) - 1
        else:
            print("Sorry, that is not a valid choice.")
            promptCard()
        if follow < 0 or follow >= len(hand):
            print("Sorry, that is not a valid choice.")
            promptCard()
    promptCard()
    follow_card = hand[follow]
    originalHand.remove(hand[follow])
    hand = copy.deepcopy(originalHand)
    return [follow_card, hand]

# Drawing Phase Codes ********************
def decodeCard(card):
    Suit = card [0]
    Number = card [1:]
    Suit = int(Suit)
    Number = int(Number)
    card = [Suit,Number]
    return card


def showCard(cards, symbol):
    # To-Do: use Python print function for now
    a = cards[0]   
    if a == 0:
        a = '♠'
    elif a == 1:
        a = '♥'
    elif a == 2:
        a = '♦'
    elif a == 3:
        a = '♣'
   
    
    b = cards[1]   
    if b == 10:
        b = '10'
    elif b == 11:
        b = 'J'
    elif b == 12:
        b = 'Q'
    elif b == 13:
        b = 'K'
    elif b == 14:
        b = 'A'
    b = str(b)
    a = str(a)
    card = b+a

    print (card)
    
def encodeCard(card):    
    suit = str(card[0])    
    number = str(card[1])
    if len(card) == 3:
        number = str(card[1])+str(card[2])
    if len(number) == 1:
        number = '0' + number
    
    card = suit + number   
    print ('Encoded lead:'+ card)
    return card


def decodeBid(Code):
    if Code == "n":
        return "pass"
    Suit = Code [1]
    if Suit == '0':
        Suit = 'Spade'
    if Suit == '1':
        Suit = 'Heart'
    if Suit == '2':
        Suit = 'Diamond'
    if Suit == '3':
        Suit = 'Club'
    if Suit == '4':
        Suit = 'No Trump'
    extra = Code[0] + Suit
    return extra





#Need the amount of tricks that has been won before the trick that was won
def trickTracking(tricksbefore, trickcounter, hand, messagequeue, cards):
#Returns trick counter after a trick has been won
#Need to add 1 to trick counter
#Needs to get cards from both hands so dealer can delete them
#Needs the message queue so dealer knows who won
#Needs the hand of both players so the dealer knows that they each played a valid card
   return trickcounter


# ***************************
# *** Phase 0.1 Functions *** #
# mshot.py
# analyze(hand): analyze a hand of cards
def analyze(hand):
    pass

