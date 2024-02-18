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

class SklanskySys2(Strategy):

        #sklansky all-in tournament strategy

        def decide_play(self, player, pot):

                total_blinds=(pot.blinds[0]+pot.blinds[1])
                score=(player.stack/total_blinds)
                score*=pot.yet_to_play
                score*=(pot.limpers+1)
                score=int(score)
                
                hand_value, rep, tie_break, raw_data=player.get_value()
                raw_values, flush_score, straight, gappers=raw_data
                raw_values.sort()
                
                key=((range(0,19)), (range(20,39)), (range(40,59)), (range(60,79)), (range(80,99)), (range(100,149)), (range(150,199)), (range(200, 399)), (range(400, 1000)))

                for k in key:
                	if score in k:
                		pointer=key.index(k)

                GAI=False

                print ('score='+str(score))
                print ('pot raised='+str(pot.raised))
                
                if pot.raised:

                        if raw_values in ((13,13), (12,12)):
                                GAI=True

                        elif raw_values in (13,12) and flush_value==2:
                                GAI=True

                        else:
                                GAI=False
                
                elif score>400 and raw_values in (13,13):
                        GAI=True
                elif score in range (200,399) and raw_values in ((13,13),(12,12)):
                        GAI=True
                elif score in range (150,199) and raw_values in ((13,13),(12,12), (11,11), (13,12)):
                        GAI=True
                elif score in range (100,149) and raw_values in ((13,13),(12,12),(11,11),(10,10),(9,9),(13,12),(13,11),(12,11)):
                        GAI=True
                elif score in range (80,99):
                        if 'pair' in rep:
                                GAI=True
                        elif raw_values in ((13,12),(13,11),(12,11)):
                                GAI=True
                        elif flush_score==2 and 13 in raw_values:
                                GAI=True
                        elif flush_score==2 and straight>=5:
                                GAI=True
                elif score in range (60,79):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 in raw_values:
                                GAI=True
                        elif flush_score==2 and 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and gappers<=1:
                                GAI=True
                elif score in range (40,59):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 or 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and gappers<=1:
                                GAI=True
                elif score in range (20,39):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 or 12 in raw_values:
                                GAI=True
                        elif flush_score==2:
                                GAI=True
                elif score in range(0,19):
                        GAI=True

                else:
                        GAI=False


                if GAI:
                        if player.stack<=player.to_play:
                                player.check_call(pot)
                        else:
                                player.bet(pot, player.stack)
                else:
                        player.fold(pot)
                        
                        
                

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
                	
class jrbalch(Strategy):
    def determine_mode(self, player):
                # Mode 0 is default, 1 is cautious, and 2 is aggressive
                if player.stack > 800:
                        return 2
                elif player.stack > 400:
                        return 1
                else:
                        if player.get_value()[0] > 200:
                                return 2
                        else:
                                return 0

    def determine_bet(self, player):
                max_bet = player.stack - player.to_play
                
                min_bet = max(0, player.to_play)  # Ensure min_bet doesn't exceed max_bet

                if max_bet < min_bet:
                        min_bet = max_bet

                bet_amount = random.randint(min_bet, max_bet)

                if(bet_amount < 0):
                        bet_amount = -bet_amount 

                bet_amount = bet_amount - (bet_amount % 5)

                return bet_amount

    def set_thresholds(self, mode):
                # Define thresholds for each mode
                if mode == 1:
                        return [10, 15, 50, 50, 0, 0, 0]
                elif mode == 0:
                        return [1, 10, 10, 10, 0, 0, 0]
                elif mode == 2:
                        return None  # No thresholds needed for aggressive mode
                else:
                        raise ValueError("Invalid mode")
                # Determine the mode of play based on player's stack size

    def decide_play(self, player, pot):
        mode = self.determine_mode(player)
        print (pot.stage)

        # for card in player.cards:
        #     print(card)

        # Get the player's hand value and cards
        value = player.get_value()[0]

        # Set thresholds based on the selected mode
        thresholds = self.set_thresholds(mode)

        if pot.total > player.stack:
                player.fold(pot)

        # Decide the action based on mode and hand value
        elif mode != 2:
            if value > thresholds[pot.stage]:
                if mode == 0:
                        player.check_call(pot)
                elif mode == 1:
                        # Hail Mary clause
                        if(value > 100):
                                player.bet(pot, player.stack)
                        else:
                                player.check_call(pot)
                else:
                        player.fold(pot)
            else:
                player.fold(pot)

        if value > 100:
                player.bet(pot, self.determine_bet(player))
        else:
                player.check_call(pot)

class Human(Strategy):
    
    options=[['x', 'f', 'b'], ['c', 'r', 'f'], ['c', 'f']]
    choices={0:'check, fold or bet', 1:'call, raise, fold', 2:'call all-in or fold'}
    
    def decide_play(self, player, pot):
        
        player.get_value()
        value = player.get_value()[0]
        print ('Hand Value: '+ (str)(value))
        
        options=Human.options
        choices=Human.choices
        action=''
        op=0

        if player.to_play==0:
                op=0
        elif player.to_play<player.stack:
                op=1
        else: op=2

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
                max_bet=player.stack
                print ('max '+str(max_bet))
                while stake not in range (10,(max_bet+1), 5):
                        try:
                                stake=int(input('stake..'))
                        except:
                                print ('input a stake')
                print ('stake '+str(stake))                                
                player.bet(pot, stake)

        
                                
					
			
			
				
			
		
			
			
			
			
		
	
	
	


