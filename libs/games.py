import random
import pandas as pd
import numpy as np

class game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        # Reset scores
        player1.reset_score()
        player2.reset_score()

        # Decide who starts
        self.current_player = random.choice([player1, player2])
        self.defender = player1 if self.current_player is player2 else player2

    def simulate(self):
        # Play until one player wins
        while self.player1.score < 7 and self.player2.score < 7:
            # print(f"{self.current_player.name} in control")
            if self.current_player.take_shot(self.defender):
                self.current_player.goal()
                self.current_player, self.defender = self.defender, self.current_player
            elif self.defender.catch(self.current_player):
                self.current_player, self.defender = self.defender, self.current_player

        # Structure the result
        result = {
            'Player1'       : self.player1.name,
            'Player1_Score' : self.player1.score,
            'Player2'       : self.player2.name,
            'Player2_Score' : self.player2.score
        }
        return result

class league:
    def __init__(self, players, n_games):
        self.results = []
        self.players = players
        self.n_games = n_games

    def simulate(self):
        """ Simulate n games using a list of players, returning a DataFrame of results. """
        for _ in range(self.n_games):
            # Choose two random, distinct players
            player1, player2 = random.sample(self.players, 2) 
            # setup and run the siumulated game, storing the results
            sim_game = game(player1, player2)
            game_result = sim_game.simulate()
            self.results.append(game_result)
        
        # Convert results list to DataFrame
        results_df = pd.DataFrame(self.results)
        results_df.loc[:, 'winner'] = np.where(results_df['Player1_Score']==7, results_df['Player1'], results_df['Player2'])

        return results_df
