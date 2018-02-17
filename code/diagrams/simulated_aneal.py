import random as rand
import math

def small_change(best_guess, space=500, max_step=50):
    #take into account dict
    #print(best_guess['anam'])
    for node in best_guess:
        if rand.randint(1,100) < 60:
            continue
        x = best_guess[node][0][0]
        y = best_guess[node][1][1]
        rand_num = rand.randint(1,150)
        if rand.randint(1,50) < 25: rand_num = -rand_num
        if rand.randint(1,50) < 25: x += rand_num
        rand_num = rand.randint(1,150)
        if rand.randint(1,50) < 25: rand_num = -rand_num
        if rand.randint(1,50) < 25: y += rand_num
        if x > space: x = space - 100 
        if x < 0: x = 0 
        if y > space: y = space - 100
        if y < 0: y = 0 
        best_guess[node][0] = (x, y)
    #print(best_guess)
    return best_guess

def simulated_annealing(best_guess, cost, space=500, initial_T=100.0, final_T=0.1, cooling_rate=0.9999, max_step=1):

    for step in range(max_step, 0, -1):
        T = initial_T

        while T > final_T:
            # Choose a node
            new = small_change(best_guess, space, step)

            # Check if it is better
            score = cost(new) - cost(best_guess)
            #print(new_cost)
            if score < 0:
                best_guess = new
            else:
                prob = math.e ** (-score / T) # Boltzmann Function
                if rand.random() < prob:
                    best_guess = new # Even if it is worse might take it

            # Decrease Temp
            T = T * cooling_rate

    return best_guess
