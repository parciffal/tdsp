import numpy as np
from .logging_tools import info_log

class MultiArmedBandit:
    
    def __init__(self, arm_names):
        self.arm_names = arm_names
        self.arm_counts = np.zeros(len(arm_names))
        self.arm_values = np.zeros(len(arm_names))

    def choose_arm(self):
        probabilities = self.arm_values / self.arm_counts
        probabilities[np.isnan(probabilities)] = 0
        return np.argmax(probabilities)

    def update(self, arm, reward):
        self.arm_counts[arm] += 1
        self.arm_values[arm] += (reward - self.arm_values[arm]) / self.arm_counts[arm]


def bidding_strategy(round_num, total_rounds, team_budget, impression_revenue, click_revenue, conversion_revenue, click_prob, conversion_prob, team_name):
    remaining_budget = team_budget
    max_bid = remaining_budget

    bandit = MultiArmedBandit([team_name])

    while round_num <= total_rounds and remaining_budget > 0:
        # Calculate the maximum bid per impression based on the remaining budget
        max_bid_per_impression = max_bid / remaining_budget if remaining_budget > 0 else 0

        # Generate a random bid for the team
        bid = np.random.uniform(0, max_bid_per_impression)

        # Calculate the revenue earned for this impression based on the click and conversion probabilities
        impression_revenue_earned = bid * impression_revenue
        click_revenue_earned = click_prob * click_revenue
        conversion_revenue_earned = click_revenue_earned * conversion_prob + (1 - click_prob) * impression_revenue_earned
        revenue_earned = conversion_revenue_earned * conversion_revenue

        # Update the remaining budget and the team's budget
        remaining_budget -= bid

        # Update the multi-armed bandit algorithm with the reward for the team's bidding strategy
        bandit.update(0, revenue_earned)

        # Print the results for this round
        info_log("Round: %d, Team: %s, Bid: %f, Revenue: %f, Remaining budget: %f" % (round_num, team_name, bid, revenue_earned, remaining_budget))

        round_num += 1

    return bid