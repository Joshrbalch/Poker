import random, pokerhands

class jrbalch(Strategy):
    def determine_mode(self, player):
                # Mode 0 is default, 1 is cautious, and 2 is aggressive
                if player.stack > 800:
                        return 2
                elif player.stack > 400:
                        return 1
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
                        player.check_call(pot)
            else:
                player.fold(pot)
        else:
                player.bet(pot, self.determine_bet(player))