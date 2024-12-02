import numpy as np
from scipy.optimize import fsolve
import random
import matplotlib.pyplot as plt
import sys


class PricingGame(object):
    def __init__(self,a=[2,2,0],c=[1,1],mu=0.25):
        """
        Initialize pricing game.
        Each pricing game has：
            a: List of product quality indexes [a1,a2,a0], where a0 is for outside goods (to compute demand)
            c : List of marginal costs [c1,c2] for product 1 and product 2 (to compute profit)
            mu: consumer taste preference
        """
        self.a =  a
        self.c =  c
        self.mu =  mu


    @classmethod
    def demand(self,p,a,mu):
        """Computes demand (Equation (5) on Page 3237 of Calvano et al.(2020))"""
        p=np.array(p)
        a=np.array(a)
        exp_terms = np.exp((a[0:2] - p) / mu)
        total = exp_terms.sum() + np.exp(a[2] / mu)  # include the outside good (a_0)
        return exp_terms / total

    @classmethod
    def bertrand_nash_equilibrium(self,a,c,mu):
        """Compute Bertrand-Nash Equilibrium Price"""

        def equilibrium_conditions(p):
            q = self.demand(p,a,mu)
            eq1 = p[0] - c[0] - mu / (1 - q[0])
            eq2 = p[1] - c[1] - mu / (1 - q[1])
            return [eq1, eq2]

        # Initial guess for prices
        initial_guess = [c[0] + mu, c[1] + mu]

        # Solve the system of equations
        p_optimal = fsolve(equilibrium_conditions, initial_guess)
        return p_optimal

    @classmethod
    def monopoly_price(self,a,c,mu):
        """Compute Monopoly Price (maximizing joint profit)"""

        def monopoly_conditions(p):
            q = self.demand(p,a,mu)
            eq1 = - (p[0] - c[0]) * (1 - q[0]) + (p[1] - c[1]) * q[1] + mu
            eq2 = - (p[1] - c[1]) * (1 - q[1]) + (p[0] - c[0]) * q[0] + mu
            return [eq1, eq2]

        # Initial guess for prices
        initial_guess = [c[0] + mu, c[1] + mu]

        # Solve the system of equations
        p_monopoly = fsolve(monopoly_conditions, initial_guess)
        return p_monopoly

    def compute_profits(self, p):
        """Compute profit"""
        a = self.a
        c = self.c
        mu = self.mu
        p=np.array(p)

        d = self.demand(p, a,mu)
        profit = (p - c) * d
        return profit



class AI():

    def __init__(self,a,c,mu, alpha=0.15, gamma=0.95, ksi=0.1, m=15, beta=4e-6,ct=100000,tmax=10000000):
        """
        Parameters (Section Baseline Parametrization and InitializationPage, Page 3234 of Calvano et al.(2020)):

            a: List of product quality indexes [a1,a2,a0], where a0 is for outside goods (to compute demand)
            c : List of marginal costs [c1,c2] for product 1 and product 2 (to compute profit)
            mu: consumer taste preference

            alpha: learning parameter (Q-learning)
            gamma: discount factor (Q-learning)
            ksi: action space parameter
            m: number of actions in action space
            beta: exploration parameter for epison-greedy algorithm
            ct: convergence period
            count: number of periods where AI actions are stable
            tmax: maximum number of period

        Initialize AI with Q-learning list full of zero. The dimension is (15,15,15).
            self.q[previous state for ai1][previous state for ai2][current action]

        price contains all possible prices the AI can choose

        action contains all historical actions the AI have choosen

        """
        self.a = a
        self.c = c
        self.mu = mu

        self.alpha = alpha
        self.gamma = gamma
        self.ksi = ksi
        self.m = m
        self.beta = beta
        self.ct = ct
        self.count=0
        self.tmax = tmax

        self.q=np.zeros((self.m, self.m,self.m))
        self.prices=self.available_prices()
        self.action=[]

    def available_prices(self):
        """
        Return the possible prices to choose.
        """

        raise NotImplementedError

    def action_to_price(self,action):
        """
        return the price corresponding to an action.
        """
        raise NotImplementedError


    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.

        Use the formula:

        Q(s, a) <- (1- alpha) * old value estimate  + alpha * (reward + gamma * best_future_reward)

        """
        raise NotImplementedError


    def choose_action(self, state,t):
        """
        Given a state `state`, return an action `p` to take.

        With probability np.exp(- t * beta) choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        raise NotImplementedError

    def check_convergence(self):
        """
        Check whether the AI converge.

        Convergence is achieved if the optimal strategy for AI does not change for 100,000 consecutive periods.
        """
        raise NotImplementedError



def train(state,t):
    """
    Train an AI by playing `n` Pricing games.
    """
    raise NotImplementedError

def draw(bin_size=10000):
    t_array = np.array(range(0, t))
    bin_indices = t_array // bin_size

    for i in [0,1]:
        ai = [ai1,ai2][i]
        prices=[ai.action_to_price(x) for x in ai.action[-len(t_array):]]
        prices_array = np.array(prices)
        sum_prices = np.bincount(bin_indices, weights=prices_array)[bin_indices[0]:]
        count_prices = np.bincount(bin_indices)[bin_indices[0]:]
        mean_prices = sum_prices / count_prices
        bin_centers = np.arange(len(mean_prices))

        plt.plot(bin_centers, mean_prices, label=f"AI{i+1}")
        plt.ylim(ai.prices[0],ai.prices[-1])
        plt.legend()
        plt.xlabel(f'Number of Period ({bin_size})', fontsize=12)
        plt.ylabel('Prices', fontsize=12)
    plt.axhline(y=PricingGame.bertrand_nash_equilibrium(ai.a,ai.c,ai.mu)[0], linestyle='-', lw=2)
    plt.text(bin_centers[-1]/3, PricingGame.bertrand_nash_equilibrium(ai.a,ai.c,ai.mu)[0]-0.027, 'Bertrand Nash Equilibrium', size=14)
    plt.axhline(y=PricingGame.monopoly_price(ai.a,ai.c,ai.mu)[0], linestyle='--', lw=2)
    plt.text(bin_centers[-1]/3, PricingGame.monopoly_price(ai.a,ai.c,ai.mu)[0]+0.015, 'Monopoly Collusion Price', size=14)
    plt.savefig("AI collusion")
    plt.close()

def main():

    global game,ai1,ai2,t
    game = PricingGame()

    ai1 = AI(game.a,game.c,game.mu)
    ai2 = AI(game.a,game.c,game.mu)

    # initial state
    a1,a2=random.choice(list(range(0,ai1.m))),random.choice(list(range(0,ai2.m)))
    # a1,a2=0,0
    t=0
    while True:
        a1,a2=train((a1,a2),t)

        if (t % 10000 == 0) & (t > 0):
            sys.stdout.write("\rt=%i" % t)
            sys.stdout.flush()

        if ai1.check_convergence() and ai2.check_convergence():
            print('Converged!')
            break

        t = t+1

    print("Done training")

    # Draw the AI Price Graph
    draw()

    # Print the final AI prices
    print(f"AI1 chooses price {ai1.action_to_price(a1)}")
    print(f"AI2 chooses price {ai2.action_to_price(a2)}")


if __name__ == '__main__':
    main()