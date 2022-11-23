from random import randint
from time import sleep
import os
import platform

class player:
    def __init__(self, type):
        self.P_type = type
        self.cards = []

    def getType(self):
        return self.P_type

    #Add a new card to the players list of cards
    def addCard(self,card):
        self.cards.append(card)
    
    #Return the total ammount of cards in the player's hand
    def ammountCards (self):
        return len(self.cards)

    #Take out a spacific card from the player's hand
    def removeCard(self,objCard):
        #look for the card you want to delete
        result = self.findCard(objCard.getColor(),objCard.getNumber(),True)
        
        if result:
            n = result[0]
            self.cards.remove(n)
            print("Card removed from hand...")
        else:
            print("Card not found")
    
    def showCards(self):
        for c in self.cards:
            print(f"{c.getColor()},{c.getNumber()}")
    #-----------------------------------------------------

    #look for a specific card in the player's hand. used for BOTS to grab the first one it finds
    def findFirstCard(self,objColor, objNum):

        for card in self.cards:
            if card.getColor() == objColor or card.getNumber() == objNum:
                return card
        
        return False
    
    #retrun list of locations with available cards
    def findCard(self,objColor,objNum,specific = False):

        results = []

        for i in range(len(self.cards)):
            iCard = self.cards[i]
            if specific:#search for a specific card with the same color and number
                if iCard.getColor() == objColor and iCard.getNumber() == objNum:
                    results.append(iCard)
                    return results
            else:#look for a card wich is compatible to center card by color or number
                if iCard.getColor() == objColor or iCard.getNumber() == objNum:
                    results.append(i)
        
        return results
    
    #Look for compatible cards and select one
    def selectPosibleCards(self,objColor, objNum):
        if self.P_type == "player":
            
            availableCards = self.findCard(objColor,objNum)#list of indexes of compatible cards
            if availableCards:

                counter =0
                for option in availableCards:
                    print(f"""\n|--------\n|CARD#{option}\n|Color: {self.cards[option].getColor()}\n|Number: {self.cards[option].getNumber()}\n|--------""")
                    counter +=1
                
                while(True):
                    try:
                        op=int(input("Which card do you choose?:"))
                        if op in availableCards:
                            break
                    
                    except Exception as e:
                        print("Choose again...")
                
                return self.cards[op]
            else:
                print("No cards available...")
                return False
        
        else:#what to do with a bot
            return self.findFirstCard(objColor,objNum)

class card:
    def __init__(self,Ncolor,Nnumber):
        self.color = Ncolor
        self.number = Nnumber
    
    def getColor(self):
        return self.color
    def getNumber(self):
        return self.number

def fillPile():
    cardPile = []
    numbers = [1,2,3,4,5,6,7,8,9]
    colors = ["red","green","blue","yellow"]

    for color in colors:
        for number in numbers:
            cardPile.append(card(color,number))
            cardPile.append(card(color,number))
    
    cardPile=mixCards(cardPile)
    return cardPile

def mixCards(cardPile):
    for i in range(len(cardPile)-1):
        loc = randint(0,len(cardPile)-1)
        temp= cardPile[loc]
        cardPile[loc]= cardPile[i]
        cardPile[i] = temp
    return cardPile

def startDeck(player, cardPile):
    
    for i in range(5):
        card = cardPile.pop(randint(0,len(cardPile)-1))
        player.addCard(card)

    return [player,cardPile]

def orderOfPlayers(players):
    orderList = []

    #Choose random player from list as first to play
    pivot = randint(0,len(players)-1)
    #keep count of the ammount of players already listed
    counter = 1
    #make a new list (who starts playing) and continue in order
    #e.g: start = 5, next 6...7...8...1...2(since it reached the limit of the player list it goes back to the start)
    while counter <= (len(players)):
        #if the pivot reaches the limit go back to the start
        if pivot == len(players):
            pivot = 0
        #add the player info to the order list
        orderList.append(players[pivot])
        pivot += 1
        counter += 1
    
    return orderList

def gameLoop(centerCard, playerList, deck, speed):
    counter = 0

    print("\n\nCurrent order of players:\n")
    
    for p in playerList:
        print(f"{p.getType()}->",end="")
    
    print("...")
    sleep(speed)
    clearScreen()

    state = True
    while state:
        for current in playerList:
            clearScreen()
            #Center card DATA
            number = centerCard.getNumber()
            color = centerCard.getColor()

            print(f"\n---------\nThe center card is:\n{color}\n{number}\n---------")
            sleep(speed)
            #---------------------------------

            

            if current.getType()=="player":
                print("\nIts your turn to play...\n--------\n")
                
                print("\nThese are your cards:")
                current.showCards()
                sleep(speed)
            
            else:
                print(f"Its {current.getType()}'s turn to play...\nhe has #{current.ammountCards()} cards")
                sleep(speed)

            res = current.selectPosibleCards(color,number)#if it is the player it will select a compatible card or draw a new one

            if res:
                current.removeCard(res)
                deck.reverse()
                deck.append(res)
                deck.reverse()
                centerCard = res
                number = centerCard.getNumber()
                color = centerCard.getColor()
                print(f"\n{current.getType()}, has placed a {color}, {number}!\n")
                sleep(speed)
            else:
                current.addCard(deck.pop())
                print(f"\n{current.getType()} has taken a new card")
                sleep(speed)


            if current.ammountCards() == 1:
                print(f"!!{current.getType()} says he has only one card left!!")
                sleep(speed)

            elif current.ammountCards()==0:
                print(f"!!!CONGRATS {current.getType()} you have won!!!")
                sleep(speed)
                state = False
                break
        deck = mixCards(deck)
        
    
    print("GAME OVER")

def clearScreen():
    if "Windows" in platform.system():
        os.system("cls")
    else:
        os.system("clear")


def textSpeed():
    speed = input("Select text speed:\ns-slow (3 seconds per text)\nn-normal (2 seconds per test)\nf-fast (one second per text)\n->").lower()
    if speed == "s":
        return 3 
    if speed == "n":
        return 2
    if speed == "f":
        return 1
    else:
        print("Using default - normal...")    
        return 2

if __name__ == "__main__":
    cardPile=fillPile()
    amount = int(input("How many bots ? (1-3):"))
    
    speed = textSpeed()
        
    players = []
    players.append(player("player"))
    players.append(player("bot_1"))
    if amount > 1:
        players.append(player("bot_2"))
        print("bot 2 added")

        if amount > 2:
            players.append(player("bot_3"))
            print("bot 3 added")

    orderList = orderOfPlayers(players)
    #spread cards to players initial hands
    for i in range(len(orderList)):

        results = startDeck(orderList[i],cardPile)
        orderList[i] = results[0]
        cardPile = results[1]

    #get the top card in the deck to the center
    centerCard = cardPile.pop()

    gameLoop(centerCard,orderList,cardPile,speed)