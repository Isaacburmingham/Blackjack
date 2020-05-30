# Isaac Burmingham


import random
import sys
import csv
from collections import namedtuple

class Hand:
    """ Class that encapsulates blackjack hand """

    def __init__(self, cards=None):
        self.cards = []
        if cards == None:
            self.cards = []
        else:
            self.cards = cards
            total,soft_ace_count = self.score()


    def __str__(self):
        return f"My hand contains: {self.cards}, therefore my score is: {self.score()}"

    def add_card(self):
        if self.score()[0] < 21:
            self.cards.append(random.randint(1,13))
            total,soft_ace_count = self.score()

    def is_blackjack(self):
        if self.score()[0] == 21:
            if self.cards[0] >= 10 or self.cards[0] == 1: # can just use 0 and 1 indices since will only apply to hand of two
                if self.cards[1] >= 10 or self.cards[1] == 1:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_bust(self):
        if self.score()[0] > 21:
            return True
        else:
            return False

    def score(self):
        Score = namedtuple('Score','total soft_ace_count')
        count = 0
        soft_count = 0
        ace = False

        for card in self.cards:
            if card >= 10:
                count += 10
            else:
                count += card

            if card == 1:
                ace = True

        if count < 12 and ace == True:
            count += 10
            soft_count += 1

        return Score(count, soft_count)

class Strategy:

    def __init__(self, stand_on_value, stand_on_soft):
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    def __repr__(self):
        return "Strategy(%d,%d)" % (self.stand_on_value,self.stand_on_soft)

    def __str__(self):
        if self.stand_on_soft == True:
            return f"S{self.stand_on_value}"
        else:
            return f"H{self.stand_on_value}"

    def stand(self,hand):
        Stand = namedtuple('Stand','stand total')
        total, soft_ace_count = Hand.score(hand)
        if self.stand_on_soft == True:
            if total >= self.stand_on_value:
                return Stand(True,total) #stand
            else:
                return Stand(False,total) # take hit
        else:
            if total < self.stand_on_value:
                return Stand(False,total) # take hit
            elif total == self.stand_on_value and soft_ace_count == 1:
                return Stand(False,total) # take hit
            else:
                return Stand(True,total) # stand if over stand value

    def play(self):

        bust_count = 0
        self.hand = Hand() #initalize an empty hand
        getscore = self.hand.score()

        while getscore[0] < 21:

            if self.stand_on_soft == True or self.stand_on_soft == False:
                if self.stand(self.hand)[0] == True:
                    #print(hand,score(hand)[0],"STAND")
                    return self.hand

                else:
                    Hand.add_card(self.hand) # add a card


                    if Hand.score(self.hand)[0] > 21:
                        #print(hand,score(hand)[0],"BUST")
                        bust_count += 1
                        return self.hand


                    elif Hand.score(self.hand)[0] == 21:
                        #print(hand,score(hand)[0],"WIN")
                        return self.hand


                    else:
                        #print(hand,score(hand)[0],"Back to the top")
                        continue
        else:
            # You win
            return self.hand

def main():
    if len(sys.argv) > 2:
        raise ValueError
    else:
        num_sim = int(sys.argv[1])

        toggle = 1 # creating two toggles to alternate between different strategies
        toggle2 = 1
        win_list = []

        # it takes a bit to go through the sims if num_sims is large. ~1 min for 100 sims
        for k in range(num_sim):
            count_row = -1
            for i in range(13,21):
                for y in range(2):
                    count_row += 1
                    count_col = -1
                    toggle2 = (toggle2 + 1) % 2
                    for j in range(13,21):
                        for x in range(2):
                            count_col += 1
                            win_count = 0
                            toggle = (toggle + 1) % 2
                            player_strategy = Strategy(i,toggle2)
                            dealer_strategy = Strategy(j,toggle)
                            #print(player_strategy,toggle)
                            #print(dealer_strategy,toggle2)

                            player_hand = player_strategy.play()
                            dealer_hand = dealer_strategy.play()

                            if player_hand.is_bust():
                                win_list.append(0)
                                #print("Dealer wins")

                            else:
                                if dealer_hand.is_bust():
                                    win_count += 1
                                    win_list.append(win_count)
                                    #print("player wins")


                                else:
                                    if player_hand.is_blackjack():
                                        win_count += 1
                                        win_list.append(win_count)
                                        #print("player wins")

                                    elif dealer_hand.is_blackjack():
                                        win_list.append(0)
                                        #print("dealer wins")

                                    elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                                        win_list.append(0)
                                        #print("tie")


                                    elif dealer_hand.score()[0] == player_hand.score()[0]:
                                        win_list.append(0)
                                        #print("tie")

                                    elif player_hand.score()[0] > dealer_hand.score()[0]:
                                        win_count += 1
                                        win_list.append(win_count)
                                        #print("player wins")

                                    elif dealer_hand.score()[0] > player_hand.score()[0]:
                                        win_list.append(0)
                                        #print("Dealer wins")

        chunk = [win_list[x:x+256] for x in range(0,len(win_list), 256)] #break list into chunks of tables
        chunksum = [sum(x) for x in zip(*chunk)] # add the elements of each table
        final = [chunksum[x:x+16] for x in range(0,len(chunksum), 16)] # break up the rows
        grid = [[round(100*(item / num_sim),2) for item in final] for final in final]

        for row in grid:
            print(row) # terminal print


        with open('strategy.csv','w',newline='') as file:
            dealer_list = ["STRATEGY","D-H13","D-S13","D-H14","D-S14","D-H15","D-S15","D-H16","D-S16","D-H17","D-S17","D-H18","D-S18","D-H19","D-S19","D-H20","D-S20"]
            player_list = ["P-H13","P-S13","P-H14","P-S14","P-H15","P-S15","P-H16","P-S16","P-H17","P-S17","P-H18","P-S18","P-H19","P-S19","P-H20","P-S20"]

            writer = csv.writer(file,delimiter=" ")
            writer.writerow(dealer_list)
            for i in range(len(grid)):
                writer.writerow([player_list[i]] + grid[i])


if __name__=="__main__":
    main()
