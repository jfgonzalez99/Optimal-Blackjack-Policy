from random import seed, randint
import time

class Deck:
    def __init__(self, randomSeed=1):
        if randomSeed != 1:
            seed(randomSeed)
        self.drawnCards = set()
        self.numCards = 52

    def drawCard(self):
        if self.numCards == 0:
            return None

        card = randint(0,51)
        while card in self.drawnCards:
            card = randint(0,51)

        self.drawnCards.add(card)
        self.numCards -= 1
        return card

class Player:
    def __init__(self):
        # Hearts, Clubs, Diamonds, Spades
        self.suits = ["\u2665","\u2663","\u2666","\u2660"]
        self.values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        self.hand = []
        self.nonAceTotal = 0
        self.numAces = 0
    
    def addCard(self, card):
        # Return 4 if 10-A, return 3 if 8-9, return 2 if 6-7, return 1 if 4-5, return 0 if 2-3
        self.hand.append(card)
        if card % 13 == 0:
            self.numAces += 1
            return 1
        else:
            val = card % 13
            # Cards numbered 2 or 3
            if val == 1 or val == 2:
                self.nonAceTotal += val + 1
                return 0
            # Cards numbered 4 or 5
            if val == 3 or val == 4:
                self.nonAceTotal += val + 1
                return 1
            # Cards numbered 6 or 7
            if val == 5 or val == 6:
                self.nonAceTotal += val + 1
                return 2
            # Cards numbered 8 or 9
            if val == 7 or val == 8:
                self.nonAceTotal += val + 1
                return 3
            # Face cards and 10
            else:
                self.nonAceTotal += 10
                return 4
    
    def handValue(self):
        # Set one ace equal to 11
        if self.hasUsableAce():
            return self.nonAceTotal + self.numAces + 10
        # Set all aces equal to 1
        else:
            return self.nonAceTotal + self.numAces
    
    def hasUsableAce(self):
        return int(self.numAces > 0 and self.nonAceTotal <= 11 - self.numAces)

    def printHand(self):
        print(' '.join(self.intToCard(card) for card in self.hand))

    def intToCard(self, n):
        return self.values[n%13] + self.suits[n%4]

class BlackJack:
    def __init__(self, deckSeed=1):
        self.numAgentWins = 0
        self.numDealerWins = 0
        self.numDraws = 0
        self.action_space = [0,1]
        self.deckSeed = deckSeed

    def reset(self):
        # Reset count
        self.numHighCards = 0
        self.num8_9 = 0 
        self.num6_7 = 0
        self.num4_5 = 0
        self.num2_3 = 0

        # Shuffle deck
        if self.deckSeed == 1:
            self.deck = Deck()
        else:
            self.deck = Deck(self.deckSeed)

        # Create dealer
        self.dealer = Player()

        # Give dealer two cards
        dealerCard1 = self.deck.drawCard()
        dealerCard2 = self.deck.drawCard()
        self.countCard(self.dealer.addCard(dealerCard1))
        self.dealer.addCard(dealerCard2)

        # Create agent
        self.agent = Player()

        # Deal agent cards until sum is greater than 11
        while self.agent.handValue() <= 11:
            self.countCard(self.agent.addCard(self.deck.drawCard()))

        return self.updateState()
    
    def updateState(self):
        self.state = [self.agent.handValue(), 
                      self.agent.hasUsableAce(), 
                      self.numHighCards, 
                      self.num8_9, 
                      self.num6_7,
                      self.num4_5,
                      self.num2_3]
        return self.state
    
    def step(self, action):
        reward = 0
        done = False
        if action:
            self.countCard(self.agent.addCard(self.deck.drawCard()))
            next_state = self.updateState()
            # If agent exceeds 21 they lose
            if next_state[0] > 21:
                done = True
                reward = -2
                self.numDealerWins += 1
            return next_state, reward, done
        # If agent stands, dealer plays
        else:
            done = True
            # Dealer must draw while hand is less than 17
            while self.dealer.handValue() < 17:
                self.dealer.addCard(self.deck.drawCard())
            dealerHandValue = self.dealer.handValue()
            agentHandValue = self.agent.handValue()
            if dealerHandValue > 21 or dealerHandValue < agentHandValue:
                reward = 3
                self.numAgentWins += 1
            elif dealerHandValue > agentHandValue:
                reward = -2
                self.numDealerWins += 1
            else:
                reward = 0
                self.numDraws += 1
            return self.state, reward, done

    def countCard(self, cardVal):
        if cardVal == 0:
            self.num2_3 += 1
        elif cardVal == 1:
            self.num4_5 += 1
        elif cardVal == 2:
            self.num6_7 += 1
        elif cardVal == 3:
            self.num8_9 += 1
        else:
            self.numHighCards += 1  
    
    def random_action(self):
        return randint(0,1)

    def printGame(self):
        print("Dealer:")
        self.dealer.printHand()
        print("Agent:")
        self.agent.printHand()
    
    def percentWin(self):
        totalGames = self.numAgentWins + self.numDealerWins + self.numDraws
        return self.numAgentWins / totalGames

    def percentLose(self):
        totalGames = self.numAgentWins + self.numDealerWins + self.numDraws
        return self.numDealerWins / totalGames

    def percentDraw(self):
        totalGames = self.numAgentWins + self.numDealerWins + self.numDraws
        return self.numDraws / totalGames

    def printWinPercentage(self):
        print(f"Win Rate:\t {self.percentWin()}")
        print(f"Draw Rate:\t {self.percentDraw()}")
        print(f"Loss Rate:\t {self.percentLose()}")
