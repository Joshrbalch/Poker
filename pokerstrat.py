##poker player strategy and i/o

import random, pokerhands

def evaluate(player):
	
	value=player.get_value()
	
def calc_bet(player):

                   
        max_bet=player.stack-player.to_play
        min_bet=player.to_play
        if max_bet<min_bet:
        	min_bet=max_bet
        print ('max bet '+str(max_bet))
        print ('min be  '+str(min_bet))
        
        

        if max_bet<0:
                max_bet=player.stack
				
        bet_amount=random.randrange(min_bet,max_bet+1,5)
        
        
        return bet_amount
	

class Strategy():
        
        def __init__(self, player):
                
                self.tight=0
                self.aggression=0
                self.cool=0
                self.player=player
                self.name=str(self.__class__.__name__)
                
        @property
        
        def play_style(self):
                
                pass

        def decide_play(self, player, pot):
                
                pass

class Sklansky1(Strategy):

        #sklansky all-in tournament strategy

        def decide_play(self, player, pot):

                total_blinds=(BLINDS[0]+BLINDS[1])
                score=(player.stack/total_blinds)
                score*=pot.yet_to_play
                score*=(pot.limpers+1)
                
                player.get_value()
                
                key=((range(0,19)), (range(20,39)), (range(40,59)), (range(60,79)), (range(80,99)), (range(100,149)), (range(150,199)), (range(200, 399)), (range(400, 1000)))
                
                threshold={0:0, 1:0}
                
                for k in key:
                	if score in k:
                		minval=(threshold[key.index(k)])

##Key Number = 400 or more: Move in with AA and fold everything else.
##Key Number = 200 to 400: Move in with AA and KK only.
##Key Number = 150 to 200: Move in with AA, KK, QQ and AK
##Key Number = 100 to 150: Move in with AA, KK, QQ, JJ, TT, AK, AQ and KQ
##Key Number = 80 to 100: Move in with any pair, AK, AQ, KQ, any suited Ace and
##any suited connector down to 5-4 suited.
##Key Number = 60 to 80: Move in with any pair, any ace, KQ, any suited king
##and all one-gap and no-gap suited connectors.
##Key Number = 40 to 60: Move in with everything above + any king.
##Key Number = 20 to 40: Move in with everything above + any 2 suited cards
##Key Number = <20: Move in with any 2-cards.


class Random(Strategy):

    
        def decide_play(self, player, pot):

                
             
                choice=random.randint(0,3)
               
                
                if choice==0:
                	player.fold(pot)
                
                elif choice==1:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, calc_bet(player))
                elif choice==2:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, player.stack)
                	
                
                
                
		
class Human(Strategy):
    
    options=[['x', 'f', 'b'], ['c', 'r', 'f'], ['c', 'f']]
    choices={0:'check, fold or bet', 1:'call, raise, fold', 2:'call all-in or fold'}
    
    def decide_play(self, player, pot):
        
        player.get_value()
        
        options=Human.options
        choices=Human.choices
        action=''
        op=0


        if player.to_play==0:
                op=0
        elif player.to_play<player.stack:
                op=1
        else: op=2

        if player.all_in or player.stack<=0:
                player.stake=0
                print ('all in test')
                

        else:

                while action not in options[op]:

                        try:
                                action=input(str(choices[op]))
                        except NameError:
                         print ('enter a valid choice')

    
        if action=='x':
                player.check_call(pot)
        elif action=='f':
                player.fold(pot)
        elif action=='c':
                player.check_call(pot)
        elif action=='b' or action=='r':
                stake=0
                max=player.stack-player.to_play
                print ('max '+str(max))
                while stake not in range (10,(max+1), 5):
                        try:
                                stake=int(input('stake..'))
                        except:
                                print ('input a stake')
                                
                player.bet(pot, stake)

        
                                
					
			
			
				
			
		
			
			
			
			
		
	
	
	

