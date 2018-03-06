import math
import time
import requests
from PIL import Image,ImageDraw
from random import randint
from random import seed
from simulated_aneal import simulated_annealing

#import config at later date
height = 500
width = 500
seed(randint(1,1000))


#
# Start cost functions
#

def point_distance(point, other):
    #print(point, other)
    return math.sqrt((point[0] - other[0])**2 + (point[1] - other[1])**2)

#def dist_centre(point, centre=(250,250)):
#    return point_distance(point, centre)

#def dist_order(node_loc):
#    dists = [(point_distance(node_loc[node][0]), node) for node in node_loc:]
#    dists.sort()


def nice_angle(point, other, centre=(250,250)):
    a = point_distance(point, centre)
    b = point_distance(other, centre)
    c = point_distance(point, other)
    A = a**2
    B = b**2 
    AB = 2 * a * b
    C = c**2
    return math.cos(A + B - (AB - C))

def get_angles(node_loc):
    cost = 0
    RADIANS = 6.28319
    ideal_angle = RADIANS / len(node_loc)
    for node in node_loc:
        for other in node_loc:
            if node == other:
                continue
            angle = nice_angle(node_loc[node][0], node_loc[other][0])
            #cost += abs(abs(ideal_angle) - abs(angle))
            if abs(abs(angle) - ideal_angle) < .2:
                cost += 600
    return cost * 2

def same_line(node_loc):
    cost = 0
    for node in node_loc:
        for other in node_loc:
            if node != other:
                if abs(node_loc[node][0][0] - node_loc[other][0][0]) < 10:
                    cost += 1000
                if abs(node_loc[node][0][1] - node_loc[other][0][1]) < 10:
                    cost += 9000
    return cost * 2
                

def too_close(node_loc, server_loc=(250,250)):
    cost = 0
    # Distance that will be too close
    min_dist = 100
    for node in node_loc:
        for other in node_loc:
            if node == other:
                continue
            # Too close to another
            dist = point_distance(node_loc[node][0], node_loc[other][0])
            if dist < min_dist:
                cost += 100 * (100-dist)
            # too close to edge
            if (node_loc[node][0][0] - 500) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][0] - 500)))
            if (node_loc[node][0][1] - 500) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][1] - 500)))
            if (node_loc[node][0][0]) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][0])))
            if (node_loc[node][0][1]) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][1])))
    # too close to server
    if point_distance(server_loc, node_loc[node][0]) < 100:
        cost += 100

    return int(cost / 2)

def off_map(node_lst, h=500, w=500):
    cost = 0
    for node in node_lst:
        point = node_lst[node][0]
        if point[0] > w or point[0] < 0:
            cost += 500
        if point[1] > h or point[1] < 0:
            cost += 500
    return int(cost /2) 

def same_slope(node_lst, centre_x=250, centre_y=250):
    cost = 0
    for node in node_lst:
        for other in node_lst:
            if other != node:
                x = node_lst[node][0][0]
                y = node_lst[node][0][1]
                x1 = node_lst[other][0][0]
                y1 = node_lst[other][0][1]
                # Ensure no div 0
                if (centre_x - x): slope1 = (centre_y - y) / (centre_x - x)
                else: cost += 2000; continue
                # Ensure no div 0
                if (centre_x - x1): slope2 = (centre_y - y1) / (centre_x - x1)
                else: cost += 2000; continue
                # Check same slope
                if slope1 == slope2: cost += 3000
                elif abs(slope1 - slope2) < .5: cost += 2000
    return cost

def cost(node_lst):
    cost = 0
    cost += too_close(node_lst)
    cost += off_map(node_lst)
    cost += get_angles(node_lst)
    #cost += same_line(node_lst)
    cost += same_slope(node_lst)
    return cost

#
# End cost functions
#


def get_data():
    r = requests.get('http://panoptes.xyz:8080/render?target=*.ping.avg&format=json&from=-1min')
    data = r.json()
    return data

def get_nodes(data):
#    node_lst = []
#    for node in data:
#        distance = node["datapoints"][-1][0]
#        name = node["target"].split('.')[0]
#        node_lst.append((name, distance))
    node_lst = [('anam', 28.127), ('saturn', 30), ('pluto', 5), ('gary', 7), ('dave', 40)]
    return node_lst

def give_points(node_lst):
    points = {}
    for node in node_lst:
        directions = [(1,1),(-1,1),(1,-1),(-1,-1)]
        # Choose a direction
        direction = directions[randint(0,3)]
        # Random X coordinate
        step_x = (direction[0] * node[1]) 
        if step_x > 0: step_x +=  (randint(0,150))
        else: step_x -= (randint(0,150))
        # Random Y coordinate
        step_y = (direction[1] * node[1])
        if step_y > 0: step_y += (randint(0,150))
        else: step_y -= (randint(0,150))
        points[node[0]] = [(250 + step_x,\
                            250 + step_y), (250, 250)]
    return points

def draw_map(point, cost, width=500, height=500):
    img=Image.new('RGB',(width, height),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    for node in point:
        draw.line((point[node][0],point[node][1]),fill=(0,255,0),width=3)

    for node in point:
        msg = node #+ str(point[node][0])
        draw.text(point[node][0],msg,(0,0,0))
   
    # Draw server last to be on top
    server_pos = ((height/2)+3, (width/2)+3)
    draw.text(server_pos,'Server',(0,0,0))

    # Draw stats
    draw.text((5,490),f'Cost {cost}',(0,0,0))

    #img.show() 
    img.save('/home/greenday/www/diagrams/network.png')

def create_page():
    f = open('/home/greenday/www/diagrams/index.html', 'w+')
    f.write('<!doctype html>\n')
    f.write('<head>\n \t<title>Network Diagram</title>\n </head>')
    f.write('<body>\n \t <p> \t <img src="network.png" alt="Network Diagram"></p>\n')
    f.write(f'Last updated: {time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())}\n</body>')
    f.close()

def main():
    #data = get_data()
    population = []
    data = ''
    best_score = 1000000000000
    node_lst = get_nodes(data)
    # make first random guess
    best_guess = give_points(node_lst)
    # get the cost of that guess
    score = cost(best_guess)
    #draw_map(best_guess, score)
    # Run simulated_annealing on it to get it better
    ans = simulated_annealing(best_guess, cost)
    # get score of new diagram
    sim_score = cost(ans)
    drawn = False
    for _ in range(1):
        if sim_score < 160000:
            draw_map(ans, sim_score)
            drawn = True
            break
        else:
            if sim_score < best_score:
                best_score = sim_score
                best_guess = ans
                print(f'using graph with score {best_score}')
                simulated_annealing(ans, cost)
            else:
                print(f'Reusing graph score {best_score}')
                simulated_annealing(best_guess, cost)
    if not drawn:
        draw_map(ans, best_score)
    create_page()
    

if __name__ == '__main__':
    main()
