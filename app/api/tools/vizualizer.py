import matplotlib.pyplot as plt

class BidVisualizer:
    def __init__(self, budget, rounds):
        self.budget = budget
        self.rounds = rounds
        self.bids = []
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor('xkcd:cyan')
        self.ax.set_xlim(0, self.rounds+1)
        self.ax.set_ylim(0, self.budget)
        self.ax.set_xlabel('Rounds')
        self.ax.set_ylabel('Bid')
        self.ax.set_title('Bidding Table')
        self.ax.set_facecolor('xkcd:mint green')
        self.line, = self.ax.plot([], [], color='black', linestyle='dashed', linewidth=1,\
                                  marker='o', markerfacecolor='black', markersize=2)
        

    def add_bid(self, bid_value, win_bool):
        if win_bool:
            self.ax.scatter(len(self.bids) + 1, bid_value, color='red', marker='o', s=40)
        
        self.bids.append(bid_value)
        self.line.set_data(range(1, len(self.bids)+1), self.bids)
        self.fig.canvas.draw()
        plt.pause(0.1)
            
