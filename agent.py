#-------------------------------------------------------------------------------
#TEAM NAME : SEEKERS

#MEMBERS:
    #ANKITA RATHOD(VY49170)
    #NITU CHOUDHARY (KJ96491)

#-------------------------------------------------------------------------------

import numpy as np
from utils import Directions
import util_functions as uf
from utils import MapTiles


class BaseAgent(object):
    def __init__(self, height, width, initial_strength, name='base_agent'):
        """
        Base class for a game agent

        Parameters
        ----------
        height: int
            Height of the game map
        width: int
            Width of the game map
        initial_strength: int
            Initial strength of the agent
        name: str
            Name of the agent
        """
        self.height = height
        self.width = width
        self.initial_strength = initial_strength
        self.name = name

    def step(self, location, strength, game_map, map_objects):
        """

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far


        Returns
        -------
        direction: Directions
            Which direction to move
        """
        pass


class RandomAgent(BaseAgent):
    """
    A random agent that moves in each direction randomly

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='random_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        return np.random.choice(list(Directions))


class HumanAgent(BaseAgent):
    """
    A human agent that that can be controlled by the user. At each time step
    the agent will prompt for an input from the user.

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='human_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of an agent that at each step asks the user
        what to do

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}

        dirchar = ''
        while not dirchar in ['N', 'S', 'W', 'E']:
            dirchar = input("Please enter a direction (N/S/E/W): ").upper()

        return dir_dict[dirchar]

class Node():
    """
        Node class for bookkeeping of children nodes for SeekerAgent
    """
    def __init__(self, position=None):
        self.position = position  #The x,y co-ordinates of the cell
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position

class SeekerAgent(BaseAgent):
    def __init__(self, height, width, initial_strength, name='seeker_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)
    visited_list=[]     #To store already visited locations 
    def step(self, location, strength, game_map, map_objects):
        
        SeekerAgent.visited_list.append(location)
        
        direction = {(-1, 0): "N", (1, 0): "S", (0, -1): "W", (0, 1): "E"}
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}
        children = []
        children_same_h =[]
        child_max_index= -1
        p = []
        direc = ''
        max1 = 0
        (x, y) = location
        d = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #Function to calculate heuristic
        def cal_h(position, game_map):
            s1=0    #To store the delta value for the map_objects
            s2=0    #To store the delta value for the map_objects
            s=0     #To store the maximum delta

            #To calculate path cost
            if (game_map[position[0]][position[1]] == MapTiles.PATH):
                h = 1 
            elif (game_map[position[0]][position[1]] == MapTiles.SAND):
                h = 3
            elif (game_map[position[0]][position[1]] == MapTiles.MOUNTAIN):
                h = 10
            elif (game_map[position[0]][position[1]] == MapTiles.WALL):
                return -1

            #Nearby Map_objects are checked for the child node(i.e given position)
            #And the delta values are calculated
            if(direction[tuple(np.subtract( position, location))] == "N"):
                position1 = tuple(np.subtract(position,(0,-1)))
                position2 = tuple(np.subtract(position,(0, 1)))
                for k in map_objects:
                    if k == position1:
                        if(map_objects[k].label == 'medkit'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s1 = map_objects[k].delta
                            
                    if k == position2:
                        if(map_objects[k].label == 'medkit'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s2 = map_objects[k].delta

                s = max(s1,s2)
                            
                if(position[0]>=self.height/2):
                    h =h+1
                else:
                    h =h+5
            
            elif(direction[tuple(np.subtract( position, location))] == "S"):
                position1 = tuple(np.subtract(position,(0, -1)))
                position2 = tuple(np.subtract(position,(0, 1)))
                for k in map_objects:
                    if k == position1:
                        if(map_objects[k].label == 'medkit'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s1 = map_objects[k].delta
                            
                    if k == position2:
                        if(map_objects[k].label == 'medkit'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s2 = map_objects[k].delta

                    s = max(s1,s2)
                if(position[0]<=self.height/2):
                    h =h+1
                else:
                    h =h+5
                    
            elif(direction[tuple(np.subtract( position, location))] == "E"):
                position1 = tuple(np.subtract(position,(-1,0)))
                position2 = tuple(np.subtract(position,(1,0)))
                
                for k in map_objects:
                    if k == position1:
                        if(map_objects[k].label == 'medkit'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s1 = map_objects[k].delta
                            
                    elif k == position2:
                        if(map_objects[k].label == 'medkit'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s2 = map_objects[k].delta

                s = max(s1,s2)
                if(position[1]<=self.width/2):
                        h =h+1
                else:
                        h =h+5
                        
            elif(direction[tuple(np.subtract( position, location))] == "W"):
                position1 = tuple(np.subtract(position,(-1,0)))
                position2 = tuple(np.subtract(position,(1,0)))
                
                for k in map_objects:
                    if k == position1:
                        if(map_objects[k].label == 'medkit'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s1 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s1 = map_objects[k].delta
                            
                    elif k == position2:
                        if(map_objects[k].label == 'medkit'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'skeleton'):
                            s2 = map_objects[k].delta
                        elif(map_objects[k].label== 'boss'):
                            s2 = map_objects[k].delta

                s = max(s1,s2)

                #penalty points 1  is added when the action when chosen goes towards the unexplored region of the map.
                #penalty points 5 is added when the action when chosen goes more towards the boundary and towards the area which has less cells to explore.
                if(position[1]>=self.width/2):
                    h =h+1
                else:
                    h =h+5
                    
            return strength-h+s     #Returns heuristic value considering the delta for the map_objects,cell cost, penalties and the strength of the agent

        #Generating Children 
        for new_pos in d:
            node_position = tuple(np.add(location, new_pos))
            # To validate if position is within range
            if (node_position[0] > (self.height - 1) or node_position[0] < 0 or node_position[1] < 0 or node_position[
                1] > (self.width - 1)):
                continue
            
            new_node = Node(node_position)
            new_node.h = cal_h(node_position, game_map)
            
            if new_node.h != -1:
                children.append(new_node)

        p.clear()      
        #To remove the already visited node from children list
        
        for k,c in enumerate(children):
            for v in SeekerAgent.visited_list:
                if(c.position==v):
                    #store the indices of the already visited nodes
                    p.append(k)
                    break
                    

        if len(p)!= 0 and len(children)!=0:
            for j in range(0, len(p)):
                # Loop to remove the nodes from the children list which is already present in the visited_list.
                children.pop(p[j] - j)
              
        #To find maximum heuristic value
        #Higher the heuristic after considering the delta values of map_objects, cell cost, penalties and the strength of the agent, higher is the chance of taking that action(i.e choosing the node)
        #Node with highest heuristic value is chosen
        for i,c in enumerate(children):
            if c.h >= max1 and c.h!=-1:
                max1 = c.h
                child_max_index = i
        if(len(children)==0):
            return np.random.choice(list(Directions))
        else:
            child = children.pop(child_max_index)
        for c in children:
            if not c==child:
                if c.h == child.h:
                    children_same_h.append(c)
                    
        #If there are more possibilities with same heuristic value choose one node randomly.
        if(len(children_same_h)!=0):
            child = np.random.choice(children_same_h)

        #To find the direction
        direc = direction[tuple(np.subtract( child.position, location))]
        
        #Return the direction for one step
        return dir_dict[direc]
