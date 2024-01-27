import numpy as np
import pickle
from blackjack import BlackjackGame

class BlackjackQLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # Initialize Q-table
        self.Q = np.zeros((33, 12, 2, 2))  # Player sum, dealer card, action

    def choose_action(self, player_sum, dealer_card, usable_ace):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(["hit", "stay"])
        else:
            return "hit" if self.Q[player_sum, dealer_card, usable_ace, 0] > self.Q[player_sum, dealer_card, usable_ace, 1] else "stay"

    def update(self, player_sum, dealer_card, usable_ace, action, reward, new_player_sum, new_dealer_card, new_usable_ace):
        action_idx = 0 if action == "hit" else 1
        old_value = self.Q[player_sum, dealer_card, usable_ace, action_idx]
        future_max = np.max(self.Q[new_player_sum, new_dealer_card, new_usable_ace])
        self.Q[player_sum, dealer_card, usable_ace, action_idx] = old_value + self.alpha * (reward + self.gamma * future_max - old_value)

    @staticmethod
    def has_usable_ace(hand):
        """Check if the hand has a usable ace."""
        value, ace = 0, False
        for card in hand:
            card_number = card['number']
            value += min(10, int(card_number) if card_number not in ['J', 'Q', 'K', 'A'] else 11)
            ace |= (card_number == 'A')
        return int(ace and value + 10 <= 21)

    def train(self, episodes):
        one_percent = round(episodes / 100)

        for ep in range(episodes):
            game = BlackjackGame()
            game.start_game()

            if ep % one_percent == 0:
                progress = (ep/episodes) * 100
                print(f"Training progress: {progress:.2f}%")

            
            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0]['number'] != 'A' else 11)
            status = "continue"

            while status == "continue":
                player_sum = game.hand_value(game.player_hand)
                usable_ace = self.has_usable_ace(game.player_hand)
                action = self.choose_action(player_sum, dealer_card, usable_ace)
                status = game.player_action(action)
                new_player_sum = game.hand_value(game.player_hand)
                new_usable_ace = self.has_usable_ace(game.player_hand)

                reward = 0  # Intermediate reward, only final matters

                if status == "player_blackjack":
                    reward = 1
                elif status == "player_bust":
                    reward = -1

                if reward != 0:
                    self.update(player_sum, dealer_card, usable_ace, action, reward, new_player_sum, dealer_card, new_usable_ace)

                if action == "stay":
                    break

            final_result = game.game_result()
            final_reward = 1 if final_result == "win" else (-1 if final_result == "loss" else 0)
            self.update(player_sum, dealer_card, usable_ace, action, final_reward, new_player_sum, dealer_card, new_usable_ace)

    def play(self):
        game = BlackjackGame()
        game.start_game()

        print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

        status = "continue"
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        while status == "continue":
            player_sum = game.hand_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (10 if game.dealer_hand[0]['number'] != 'A' else 11)
            action = "hit" if self.Q[player_sum, dealer_card, usable_ace, 0] > self.Q[player_sum, dealer_card, usable_ace, 1] else "stay"
            status = game.player_action(action)
            
            if action == "stay":
                break
                
            print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        

        if status == "continue":
            print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
            game.dealer_action()

        final_result = game.game_result()
        return final_result
        
    def save_model(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.Q, file)

    def load_model(self, filename):
        with open(filename, 'rb') as file:
            self.Q = pickle.load(file)


# Train the agent
agent = BlackjackQLearning()
agent.train(5000000)

test_games = 1000000
wins = 0
losses = 0
draws = 0

for _ in range(test_games):
    print("-----")
    result = agent.play()
    print(result)
    if result == "win":
        wins += 1
    elif result == "loss":
        losses += 1
    else:
        draws += 1

print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
print(f"Win rate: {wins/(wins + losses)*100:.2f}%")
