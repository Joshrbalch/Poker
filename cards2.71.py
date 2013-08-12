import random
import pokerhands
from operator import attrgetter
import time
import pokerstrat



#card class

class Card:

    RANKS=['2','3','4','5','6','7','8','9','10','J', 'Q', 'K', 'A']

    SUITS=['h', 'c', 's', 'd']

    def __init__(self,rank, suit, faceup=True):

        self.rank=rank
        self.suit=suit
        self.values=[]
        self.__value=(Card.RANKS.index(self.rank)+1)
        
        self.faceup=faceup

    def __str__(self):

        if self.faceup:
            
            return str(self.rank)+str(self.suit)
        else:
            return 'XX'

    @property

    def value(self):

        v=self.__value

        return v

#hand class (also used for Player)

class Hand:

    

    def __init__(self, name, table, strategy='Random'):

        
        self.strategy=[]
        
        strategy_class=getattr(pokerstrat, strategy)
        strat=strategy_class(self)
        
       
       
        self.strategy.append(strat)
               
        
        self.cards=[]
        self.total_cards=(self.cards+table.cards)
        table.players.append(self)
        self.name=name
        self.small_blind=False
        self.big_blind=False
        self.dealer=False
        self.hand_value=0
        self.rep=''
        self.tie_break=0
        self.is_folded=False
        self.stack=1000
        
        self.stake=0
        self.in_pot=0
        self.to_play=0
        self.all_in=False
        self.first_all_in=False
        self.raised=0
        self.carry_over=0

        #data points for play analysis:

        self.history=[]

        self.pots_played=0
        self.win=0
        self.raises=0
        self.calls=0
        self.checks=0

    @property

    def play_analysis(self):

        pass
        

    def __str__(self):


        rep='\n'+str(self.name)+'\t    stack='+str(self.stack)+'\n'
        
        if self.small_blind:
            rep+=' small blind'
        elif self.big_blind:
            rep+=' big blind'
        elif self.dealer:
            rep+=' dealer'
        

        return rep
   
        
    
    def get_value(self):
        
        self.total_cards=(self.cards+table.cards)
        
        rep, hand_value, tie_break=pokerhands.evaluate_hand(self.total_cards)
        
        self.rep=str(rep)
        self.hand_value=hand_value
        self.tie_break=tie_break
    
        return hand_value, rep, tie_break

    def print_cards(self):

        rep=''

        if self.is_folded:
            rep='FF'

        else:

            for card in self.cards:

                rep+=str(card)+'  '
        

        print (rep)
        
        
    def flip(self):
            
        for card in self.cards: card.faceup=not card.faceup

    def fold(self, pot):

        self.is_folded=True
        self.in_pot=0
        self.stake=0
        self.raised=0
        
     
        print (str(self.name)+' folds')

        pot.folded_players.append(self)
        pot.active_players.remove(self)
        
                
        if len(pot.folded_players)>(len(table.players)-1):
        	
        	pot.stage=5
        	for pot in pots:
        		for player in pot.players:
        				if player.is_folded==False:
        					print (str(player.name)+' wins '+(str(pot.total)))
        					player.stack+=pot.total
        		
        
          
            
        
    def ante(self, pot):
        
        if self.small_blind:
            self.stack-=BLINDS[0]
            pot.total+=BLINDS[0]
            self.in_pot+=BLINDS[0]
            
        if self.big_blind:
            self.stack-=BLINDS[1]
            pot.total+=BLINDS[1]
            pot.to_play=BLINDS[1]
            self.in_pot+=BLINDS[1]
        

    
    
                    
    def bust(self):

        print (str(self.name)+' is bust')
        table.players.remove(self)
        
        
    def clear(self):

      self.cards=[]
      self.is_folded=False
      self.all_in=False
      self.raised=0
      

    def add(self, cards):

      self.cards.append(cards)

#__________represents the card deck - shuffled each round            
        
class Deck(Hand):

    def __init__(self):

        self.cards=[]

    def populate(self):

        for rank in Card.RANKS:

            for suit in Card.SUITS:

                card=Card(rank, suit)
                self.cards.append(card)

    def shuffle(self):

        random.shuffle(self.cards)

    def print_cards(self):

        rep=''

        for card in self.cards:

            rep+=str(card)+' '

        print (rep)

    def deal_to(self, hand, cards=1, faceup=True):

        if len(self.cards)<cards:
                print ('not enough cards to deal')
                
        elif len(self.cards)==0:
                print ('deck empty')
                
        else:
                dealt=[]
                if not faceup:
                    for card in self.cards:
                         card.faceup=False
                
                for i in range (0,cards):
                        dealt.append(self.cards.pop())
                
                        
                for card in dealt:
                    
                    hand.add(card)

#__________________represents the overall game    

class Table(Hand):

    def __init__(self):

                
        self.cards=[]
        self.players=[]
        self.is_folded=False
        self.button=0
        
    def print_cards(self):

        rep='Community cards_______________\n'

        if self.is_folded:
            rep='FF'

        else:

            for card in self.cards:

                rep+=str(card)+' '

        print (rep)

    
    def clear(self):

      self.cards=[]
      
      

#_______________POT represents the pot for each individual round of play

class Pot(object):
    
    stage_dict={0:'pre-flop bet', 1:'dealing the flop', 2:'dealing the turn', 3:'dealing the river'}
    deal_sequence=[0,3,1,1]
    pot_number=0
    
    def __init__(self, table, name):
        
   
        self.players=[]
        self.folded_players=[]
        self.active_players=[]
        self.name=name
        
            
        self.total=0
        
        self.button=table.button
        #the amount each player has to call
        self.to_play=0
        #0=antes+ pre-flop, 1=post-flop, 2=turn, 3=river
        self.stage=0
        #defines turn within each betting stage
        self.turn=0
        #self.no_raise
        self.no_raise=0
        #already bet - works out if the round starts with 0 bet 
        self.already_bet=False
        
    @property
    
    def table_size(self):
        
        
        return len(self.players)
        
    def __str__(self):

            rep='Pot= '+str(self.total)+'.  to play:'+str(self.to_play)
            return rep
            
    def set_blinds(self):
        
        dealer=(self.button)%self.table_size
        
        small_blind=(self.button+1)%self.table_size

        big_blind=(self.button+2)%self.table_size

        self.players[dealer].dealer=True

        self.players[small_blind].small_blind=True

        self.players[big_blind].big_blind=True

        return
    	

    @property

    def who_plays(self):

        next_up=0

        if self.stage==0:

            next_up=(self.button+3)%self.table_size

            return next_up

        else:

            next_up=(self.button+1)%self.table_size
            return next_up


class Side_pot(Pot):
    
    serial=0
    
    def __init__(self, parent):
        
        Pot.__init__(self, parent, Pot)
        
        self.button=parent.button
        Side_pot.serial+=1
        self.name='side pot '+str(Side_pot.serial)
        
        self.players=[]
           



#________________FUNCTIONS____________________________________________________

#clears the players hands, comm cards, deck and moves the button on

def debug(pot):

    print('debug______________________')
    for player in pot.players:
        
        print (str(player.name)+' Stack='+str(player.stack)+' Stake='+str(player.stake)+' Player in pot='+str(player.in_pot)+'  Pot total='+str(pot.total)+'  all_in='+str(player.all_in)+'first all in'+str(player.first_all_in))
    
    
    for pot in pots:
            print (str(pot.name)+' total '+ str(pot.total))
            for player in pot.active_players:
            	print (str(player.name))
            print ('Pot to play:  '+str(pot.to_play))
    print ('turn'+str(pot.turn)+'  no_raise'+str(pot.no_raise))
    print ('______________________________')


def next_hand(table, deck):

    table.clear()
    
    deck.clear()
    
    Side_pot.serial=0

    for hand in table.players:
        hand.clear()
        hand.small_blind=False
        hand.big_blind=False
        hand.dealer=False
        hand.first_all_in=False

    table.button+=1
    

#calculates the values and payouts

def ante_up(pot):

    for player in pot.players:
                
        player.ante(pot)
        print (player)
        deck.deal_to(player, 2)
        player.print_cards()
        pot.already_bet=True

    print (pot)
    print ('\n\n\n')


def betting_round(pot, table):

    global pots
    
    is_side_pot=False
    create_side_pot=False
    side_potters=[]
    

    

    while pot.no_raise<(pot.table_size):
        
                
        next_up=(int(pot.who_plays)+(pot.turn))%pot.table_size
        player=pot.players[next_up]
        player.to_play=(pots[-1].to_play-player.in_pot)
        if player.to_play<0:
        	player.to_play=0
        
        

        #is the player folded? decide action

        if player not in pots[-1].folded_players:

            print (str(player.name)+' to play'+ str(player.to_play)+'\n')

            for strategy in player.strategy:
                    player.stake=strategy.decide_play(player, pots)

        else:
            print (str(player.name)+ ' is folded')
            player.stake=0

        #read the stake and play
        
        if player.stake==-1:
        	  player.stake=0
        	  player.fold(pot)
        	  pot.turn+=1
        	  pot.no_raise+=1

        elif player.is_folded:

            pot.turn+=1
            pot.no_raise+=1
        	  
        
        elif player.stake==-2:
        		player.stake=0
        		pot.turn+=1
        		pot.no_raise+=1
        		print (str(player.name)+' is all in - no more play')

        elif player.stake==-3:
            player.stake=0
            pot.turn+=1
            pot.no_raise+=1
            print (str(player.name)+' pass - no action')
            
            
        
        #chck or call
        elif player.stake==player.to_play:
            
            if player.to_play==0:
                
                print (str(player.name)+' checks')
        
            else:
                
                print (str(player.name)+' calls '+str(player.stake))

            pot.turn+=1
            pot.no_raise+=1

        elif player.stake<player.to_play and player.stake==player.stack:

            print (str(player.name)+' calls all in'+str(player.stake))

            pot.turn+=1
            pot.no_raise+=1
        
        #raise   
        elif player.stake>player.to_play:
                
            rep=''
            if player.stack-player.stake==0:
                rep=' all in'
            pot.turn+=1
            pot.no_raise=1
            if pots[-1].already_bet:
                print (str(player.name)+' raises '+str(player.stake-player.to_play)+str(rep))
                
                
            else:
                print (str(player.name)+' bets '+str(player.stake)+str(rep))
                
                pots[-1].already_bet=True

            pots[-1].to_play+=(player.stake-player.to_play)

            
            
        
        pots[-1].total+=player.stake
        player.in_pot+=player.stake
        player.stack-=player.stake
         
        if player.stack==0 and player.first_all_in==False:
            
            print (str(player.name)+' is all in ')
            
            is_side_pot=True
            player.all_in=True
            player.first_all_in=True
            pots[-1].active_players.remove(player)
            

        
        
        debug(pot)
        
        
        
            
    #deal with side pots        
                
    if is_side_pot:
        
        for player in pots[-1].players:
        	if player.is_folded==False:
        		
        		side_potters.append(player)
            
        side_potters.sort(key=attrgetter('in_pot'), reverse=True)
        big_bet=side_potters[0].in_pot
        

        next_pot_players=[]
    
        
        
        #main pot
        print ('side pot')
        print ('high bet'+str(big_bet))
        low_bet=side_potters[-1].in_pot
        print ('low bet'+str(low_bet))
        
        for player in side_potters:
            
               
            refund=(player.in_pot-low_bet)
            if len(next_pot_players)>1:
                create_side_pot=True

            player.in_pot-=refund
            pot.total-=refund
            player.stack+=refund
            player.carry_over=refund
            
            if player.carry_over>0:
            	next_pot_players.append(player)
            	
            
            
            
            
            print (str(player.name))
            print ('refund...'+str(refund))

        if create_side_pot:

            sidepot=Side_pot(pot)
            
            for player in next_pot_players:
                
                sidepot.players.append(player)
                
                sidepot.total+=player.carry_over
                player.in_pot+=player.carry_over
                player.stack-=player.carry_over
                
                
                
            pots.append(sidepot)
            
            if player.stack>0:

                player.first_all_in=False
                player.all_in=False
                pots[-1].active_players.append(player)       
            
       
    for pot in pots:
        print (str(pot.name))
        pot.to_play=0
        
        print ('pot size= '+str(pot.total))

        for player in pot.players:
            player.in_pot=0
            player.stake=0
            player.raised=0
        
  

    pots[0].no_raise=0
    pots[0].to_play=0
    pots[0].turn=0
    pots[0].stage+=1
    pots[0].already_bet=False
    
        
        


def showdown(pot):
        
    scoring=[]

    for player in pot.players:
        if player.is_folded:
            pot.players.remove(player)
    
    if pot.table_size==1:
        for player in pot.players:
            print (str(player.name)+' wins'+str(pot.total))
            player.stack+=pot.total
            break

    for player in pot.players:
             player.get_value()
             scoring.append(player)
             
             
             
    #rank hands in value+tie break order
             
    scoring.sort(key=attrgetter('hand_value', 'tie_break'), reverse=True)
    split_pot=[]
    print ('\n\n\n')
    for player in scoring:
     
            print (player.name+' has '+str(player.rep))
            
            
    #check for split pot

    split_stake=0
    split=False
    
    for player in scoring[1:]:
        
        if player.hand_value==scoring[0].hand_value and player.tie_break==scoring[0].tie_break:

            split=True
            split_pot.append(scoring[0])
            split_pot.append(player)


    if split:

        print ('split pot')
        
        
        split_stake=int((pot.total/(len(split_pot))))
        for player in split_pot:
                 print (str(player.name)+' wins '+str(split_stake))
                 player.stack+=split_stake
                 
    else:
            
            scoring[0].stack+=pot.total
            print (str(scoring[0].name)+' wins '+str(pot.total))

#_______________________________________________________________________gameplay
        ######################

#set up the game and players
   
BLINDS=(10,20)                  

table=Table()

player1=Hand('Philip', table, 'Human')
player2=Hand('Igor', table)
player3=Hand('Carol', table)
player4=Hand('Johnboy', table)

deck=Deck()

status='play'

#for i in range (0,4):

while status=='play':

    #shuffle the deck
    
    deck.populate()
    deck.shuffle()

    #create pot for this hand
    pots=[]
    pot=Pot(table, 'main')
    for player in table.players:
            pot.players.append(player)
            pot.active_players.append(player)
            
    pots.append(pot)
    
    #allocate blinds and ante up

    pot.set_blinds()
    
    ante_up(pot)

    debug(pot)

    while pot.stage<4:
            
        deck.deal_to(table, Pot.deal_sequence[pot.stage])

        print (str(Pot.stage_dict[pot.stage]))
          
        table.print_cards()        	
 
        
        betting_round(pots[-1], table)
        

    
    if len(table.players)>1:

        for pot in pots:
        
            showdown(pot)

    for player in table.players:

        if player.stack<=BLINDS[1]:
            
            player.bust()
		
    if len(table.players)==1:
    	status='winner'
          
    print ('\n\n\n')
    
    next_hand(table, deck)
    
for player in table.players:
	
	print (str(player.name)+' wins the game')




    



    






   