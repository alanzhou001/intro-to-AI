import pytest
import sys
import numpy as np

# Add current directory to sys.path to import shopping module
sys.path.insert(0, "")

import pricing as pricing


def test_available_prices1():
    """Test that available_prices returns the correct price lists"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    prices=ai.available_prices()
    expected = [1.42772123, 1.46646874, 1.50521625, 1.54396376, 1.58271127,
       1.62145877, 1.66020628, 1.69895379, 1.7377013 , 1.77644881,
       1.81519631, 1.85394382, 1.89269133, 1.93143884, 1.97018634]
    assert list(prices) == pytest.approx(expected,1e-3), "available_prices does not return the correct prices list"

def test_available_prices2():
    """Test that available_prices returns the correct price lists"""
    game = pricing.PricingGame(mu=2)
    ai=pricing.AI(game.a,game.c,game.mu)
    prices=ai.available_prices()
    expected = [3.55021869, 3.60705037, 3.66388204, 3.72071372, 3.77754539,
       3.83437706, 3.89120874, 3.94804041, 4.00487209, 4.06170376,
       4.11853543, 4.17536711, 4.23219878, 4.28903046, 4.34586213]
    assert list(prices) == pytest.approx(expected,1e-3), "available_prices does not return the correct prices list for alternative pricing game parameters"


def test_action_to_price():
    """Test that action_to_price returns the correct price"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    prices=ai.action_to_price(3)
    expected = 1.5439637578714591
    assert prices == pytest.approx(expected,1e-3), "action_to_price does not return the correct price"

def test_update1():
    """Test that update function updates Q value correctly"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.q[4][4][3]=0.5
    ai.q[3][4][2]=0.9
    ai.update((4,4),3,(3,4),0.7)
    expected = 0.65825
    assert ai.q[4][4][3] == expected, "update function does not updates Q value correctly"

def test_choose_action0():
    """Test that choose_action returns the correct action"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.q[5][6][3]=0.3
    ai.q[5][6][2]=0.2
    action=ai.choose_action((5,6), 1000000)
    expected = 3
    assert action == expected, "choose_action does not return the correct action"

def test_choose_action1():
    """Test that choose_action returns the correct action"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.q[7][8]=list(range(0,15))
    action=ai.choose_action((7,8), 400000) #epsilon = 0.20189
    expected = 14
    total = 1000
    count = 0
    for i in range(total):
        action = ai.choose_action((7,8), 400000)
        if action == expected:
            count += 1

    def assert_within(actual, expected, tolerance):
        lower = expected - tolerance
        upper = expected + tolerance
        if not lower <= actual <= upper:
            raise AssertionError("choose_action does not return the correct action when t is small")

    assert_within( count / total, (1-np.exp(- 400000 * ai.beta))+1/15, 0.2)

def test_choose_action3():
    """Test that choose_action returns the correct action"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.action=[5]
    ai.q[5][6][3]=0.3
    ai.q[5][6][2]=0.2
    ai.choose_action((5,6), 1000000)
    expected = [5,3]
    assert ai.action == expected, "choose_action does not append the newly selected action in self.action"


def test_check_convergence0():
    """Test that check_convergence correctly checks convergence"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.count=ai.ct+1
    ai.action=[6]*ai.count
    actual=ai.check_convergence()
    expected = True
    assert actual == expected, "check_convergence does not correctly identify whether the AI converges"

def test_check_convergence1():
    """Test that check_convergence correctly checks convergence"""
    game = pricing.PricingGame()
    ai=pricing.AI(game.a,game.c,game.mu)
    ai.count=ai.ct+1
    ai.action=[6]*ai.count+[5]
    actual=ai.check_convergence()
    expected = False
    assert actual == expected, "check_convergence does not correctly identify whether the AI converges"

def test_train0():
    """Test that train function correctly return the action"""
    pricing.game = pricing.PricingGame()
    pricing.ai1 = pricing.AI(pricing.game.a, pricing.game.c, pricing.game.mu)
    pricing.ai2 = pricing.AI(pricing.game.a, pricing.game.c, pricing.game.mu)
    pricing.ai1.q[7][8] = list(range(0, 15))
    pricing.ai2.q[7][8] = list(reversed(range(0, 15)))
    actual=pricing.train((7,8),1e10)
    expected = (14,0)
    assert actual == expected, "train function does not correctly return the actions choosen by the two AIs"

def test_train1():
    """Test that train function correctly return the action"""
    pricing.game = pricing.PricingGame()
    pricing.ai1 = pricing.AI(pricing.game.a, pricing.game.c, pricing.game.mu)
    pricing.ai2 = pricing.AI(pricing.game.a, pricing.game.c, pricing.game.mu)
    pricing.ai1.q[7][5] = list(range(0, 15))
    pricing.ai2.q[7][5] = list(reversed(range(0, 15)))
    a1,a2=pricing.train((7,5),1000000)
    actual=(pricing.ai1.q[7][5][a1],pricing.ai2.q[7][5][a2])
    expected = (11.913671472422326, 11.952781212317507)
    assert actual == pytest.approx(expected,1e-3), "train function does not correctly update the Q value"
