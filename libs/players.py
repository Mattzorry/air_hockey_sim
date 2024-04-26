import pandas as pd
import numpy as np
import random

from libs.utils import *

class Player:
    def __init__(self, name, power, puck_control, accuracy, deceptions, reflexes, blocking):
        self.name           = name
        self.power          = power
        self.puck_control   = puck_control
        self.accuracy       = accuracy
        self.deceptions     = deceptions
        self.reflexes       = reflexes
        self.blocking       = blocking
        self.total_skill    = self.calculate_total_skill()
        self.score = 0
        self.skill_history = pd.DataFrame({'Iteration': [], 'Total Skill': []})
        self.stats = {
            'shots':0,
            'on_targets':0,
            'deceptions':0,
            'read_blocks':0,
            'speedy':0,
            'catches':0,
            'goals':0
        }

    def calculate_total_skill(self):
        """ Calculate the total skill based on all attributes. """
        return (self.power + self.puck_control + self.accuracy + self.deceptions +
                self.reflexes + self.blocking)

    def scaled_random_walk(self, attribute):
        """ Apply a scaled random walk based on the current attribute level. """
        max_skill = 100
        scaling_factor = 1 / (1 + np.exp(0.1*(attribute-50)))  # Decreases as the attribute approaches 100
        change = random.gauss(0.2, 1 * scaling_factor)  # Smaller SD as skill is higher
        new_value = attribute + change
        return max(0, min(max_skill, new_value))  # Ensure attribute stays within 0 and 100

    def update_skills(self, game_number):
        """ Update player skills by a random walk scaled by the current skill level and update total skill. """
        self.power          = self.scaled_random_walk(self.power)
        self.puck_control   = self.scaled_random_walk(self.puck_control)
        self.accuracy       = self.scaled_random_walk(self.accuracy)
        self.deceptions     = self.scaled_random_walk(self.deceptions)
        self.reflexes       = self.scaled_random_walk(self.reflexes)
        self.blocking       = self.scaled_random_walk(self.blocking)
        self.total_skill    = self.calculate_total_skill()

        # Update the skill history DataFrame
        new_data = pd.DataFrame({'Iteration': [game_number], 'Total Skill': [self.total_skill]})
        self.skill_history = pd.concat([self.skill_history, new_data], ignore_index=True)

    def show_skills(self):
        print(f"{'Name':<15}: {self.name}")
        print(f"{'Shot Speed':<15}: {self.power:.2f}")
        print(f"{'Puck Control':<15}: {self.puck_control:.2f}")
        print(f"{'Attacks':<15}: {self.accuracy:.2f}")
        print(f"{'Deceptions':<15}: {self.deceptions:.2f}")
        print(f"{'Reflexes':<15}: {self.reflexes:.2f}")
        print(f"{'Blocking':<15}: {self.blocking:.2f}")
        print(f"{'Total Skill':<15}: {self.total_skill:.2f}")

    def take_shot(self, defender):
        """
        Simulate the shot process with sequential checks:
        1. Accuracy to determine if the shot is on target.
        2. Deception affecting the effectiveness of the defender's blocking.
        3. Power vs. Reflexes to see if the shot is too fast to be blocked.
        """

        self.stats['shots'] += 1

        # Step 1: Check if the shot is on target based on accuracy
        # Assuming 50 as a base difficulty to hit the target
        if not self.on_target():
            # print('\tmiss')
            return False  # Shot misses

        # Step 2: Use deception to potentially reduce the effectiveness of blocking
        # Determine if the shot gets past the blocking
        if not self.deceptive():
            # print('\tdeception!')

            # allow possiblity of read-blocking
            if self.read_blocked(defender): 
                # print('\tread blocked')
                return False  # Shot is blocked

        # Step 3: Power vs. Reflexes
        # Check if the shot is too fast for the goalie's reflexes
        if self.speedy(defender):
            # print('\tGoal!')
            return True
        else:
            # print('\tblocked - reflexes too fast')
            return False

    def goal(self):
        self.score += 1
        self.stats['goals'] += 1

    def on_target(self):
        prob = random.random() < norm_sigmoid(self.accuracy)
        if prob:
            self.stats['on_targets'] += 1
        return prob

    def deceptive(self):
        prob = random.random() < norm_sigmoid(self.deceptions)
        if prob:
            self.stats['deceptions'] += 1
        return prob

    def read_blocked(self, defender):
        prob = random.random() < norm_sigmoid(defender.blocking)
        if prob:
            defender.stats['read_blocks'] += 1
        return prob

    def speedy(self, defender):
        prob = random.random() < flatter_sigmoid_comp(self.power, defender.reflexes)
        if prob:
            self.stats['speedy'] += 1
        return prob

    def catch(self, opp):
        prob = random.random() < flatter_sigmoid_comp(self.puck_control, opp.puck_control)
        if prob:
            self.stats['catches'] += 1
        return prob

    def reset_score(self):
        self.score = 0

def generate_random_player(name):
    """Generate a player with skills centered around 50 with random biases."""
    central_value = 50
    bias = np.random.normal(0, 10)  # Gaussian bias with mean 0 and standard deviation 10
    
    # Generate each skill with a bias added to the central value and ensure they are within 0-100
    power           = max(0, min(100, np.random.normal(central_value + bias, 5)))
    puck_control    = max(0, min(100, np.random.normal(central_value + bias, 5)))
    attacks         = max(0, min(100, np.random.normal(central_value + bias, 5)))
    deceptions      = max(0, min(100, np.random.normal(central_value + bias, 5)))
    reflexes        = max(0, min(100, np.random.normal(central_value + bias, 5)))
    blocking        = max(0, min(100, np.random.normal(central_value + bias, 5)))
    
    # Create a new player with these skills
    return Player(name, power, puck_control, attacks, deceptions, reflexes, blocking)

def create_random_players(num_players):
    players = []
    for i in range(num_players):
        player_name = f"Player_{i+1}"
        players.append(generate_random_player(player_name))
    return players

def create_static_player(skill_value, player_name):
    import uuid
    if player_name is None:
        player_name = uuid.uuid4()
    return Player(player_name, skill_value, skill_value, skill_value, skill_value, skill_value, skill_value)


def create_even_players(num_players, skill_value):
    players = []
    for i in range(num_players):
        player_name = f"Player_{i+1}"
        players.append(create_static_player(player_name, skill_value))
        return players