import random

class BlackjackGame:
    
    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    suits = {
        "diamonds": diamond,
        "hearts": heart,
        "spades": spade,
        "clubs": club
    }

    def __init__(self):
        self.deck = self.generate_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []

    @staticmethod
    def generate_deck():
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        deck = [{'number': number, 'suit': suit} for number in numbers for suit in suits]
        return deck

    def deal_card(self):
        return self.deck.pop()

    def start_game(self):
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    @staticmethod
    def hand_value(hand):
        value = 0
        aces = 0
        for card in hand:
            if card['number'] in ['J', 'Q', 'K']:
                value += 10
            elif card['number'] == 'A':
                value += 11
                aces += 1
            else:
                value += int(card['number'])

        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def player_action(self, action):
        if action == "hit":
            self.player_hand.append(self.deal_card())
        return self.game_status()

    def dealer_action(self, output=False):
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
            if output:
                print("Dealer hits and has:", self.format_cards(self.dealer_hand), self.hand_value(self.dealer_hand))

    def game_status(self):
        player_value = self.hand_value(self.player_hand)
        if player_value > 21:
            return "player_bust"
        elif player_value == 21:
            return "player_blackjack"
        else:
            return "continue"

    def game_result(self):
        self.dealer_action()
        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)

        if player_value > 21:
            return "loss"
        elif dealer_value > 21 or player_value > dealer_value:
            return "win"
        elif player_value == dealer_value:
            return "draw"
        else:
            return "loss"
    
    @staticmethod
    def format_cards(cards):
        result = ""
        for card in cards:
            suit = BlackjackGame.suits[card["suit"]]
            result += f"{card['number']}{suit} "
        
        return result.strip()

game = BlackjackGame()
game.start_game()

def main():
    print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

    status = "continue"
    while status == "continue":
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        action = input("Enter an action (hit/stay): ")
        status = game.player_action(action)
        
        if action == "stay":
            break

    if status == "continue":
        print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
        game.dealer_action()

    print(game.game_result())

if __name__ == "__main__":
    main()

    



