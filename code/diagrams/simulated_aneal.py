import random as rand
import math

def small_change(best_guess, space=500, max_step=50):
    """
    Make small random changes to the points

    :best_guess: list of nodes and their point locations
    :space: Square size of canvas
    :max_step: how big of a jump do we allow
    """
    #take into account dict
    #print(best_guess['anam'])
    for node in best_guess:
        # only choose a couple to change
        if rand.randint(1,100) > 80:
            continue
        x = best_guess[node][0][0]
        y = best_guess[node][1][1]
        # Choose random number
        rand_num = rand.randint(1,20)
        # maybe negate random number
        if rand.randint(0,100) < 50:
            rand_num *= -1
            # add or subtract random number 
        x += rand_num
        # Steps repeat for y value
        rand_num = rand.randint(1,100)
        if rand.randint(0,100) < 50:
            rand_num *= -1
        y += rand_num
        # check if we go out of bands
        if x > space: x = space - 100 
        if x < 0: x = 0 
        if y > space: y = space - 100
        if y < 0: y = 0 
        # replace value
        best_guess[node][0] = (x, y)
    return best_guess

def simulated_annealing(best_guess, cost, space=500, initial_T=100.0, final_T=0.1, cooling_rate=0.99, max_step=50):
    """
    Takes a guess and will apply a simulated annealing algorithm to improve on the guess

    :best_guess: List of nodes and point locations
    :cost: function to calculate how good a solution is 
    :space: square size of canvas
    :inital_T: our initial starting temperature
    :final_T: temerature we should stop at
    :cooling_rate: how fast does the cooling happen every time
    :max_step: how much do we want to change the diagram each time
    """

    for step in range(max_step, 0, -1):
        T = initial_T

        while T > final_T:
            # Make a new solution
            new = small_change(best_guess, space, step)

            # Check if it is better
            score = cost(best_guess) - cost(new)
            if score >= 0:
                best_guess = new
            else:
                prob = math.e ** (-score / T) # Boltzmann Function
                if rand.random() < (prob):
                    best_guess = new # Even if it is worse might take it

            # Decrease Temp
            T = T * cooling_rate

    return best_guess
