from node import Node
import numpy as np
import random

class GridWorld:

  def __init__(self, dim, p = 0, gridworld_goal = None, real = False):
    # print ('GridWorld initialized')
    self.dim = dim # Dimension of the grid
    self.p = p # Probability of nodes being blocked

    # Denotes if this gridworld is the original one (True) 
    # Or the one to keep track of agent's knowledge base (False)
    self.real = real 
    # self.seed = seed
    
    self.grid = self.createGrid() # Grid to hold the Nodes
    # Original gridworld that the agent is trying to solve
    self.gridworld_goal = gridworld_goal 
    self.agent = None

  
  # Returns a terrain type based on i = 0, 1, 2
  @staticmethod
  def terrainType(i):
    terrains = ['Flat', 'Hill', 'Forest']
    return terrains[i]
  
  # Returns symbols for each terrain type
  # Useful for printing/visualizing the generated gridworld
  @staticmethod
  def terrainSym(i):
    syms = {'Flat':'-', 'Hill':'^', 'Forest':'#'}
    return syms[i]

  # Creates a grid that holds Nodes
  def createGrid(self):
    
    grid = np.ndarray((self.dim, self.dim), dtype=np.object) # Empty grid

    # Populating the gridworld with Nodes
    for i in range(self.dim):
      for j in range(self.dim):
        grid[i][j] = Node((i,j), self)

    if self.real: # If this gridworld was the original/real/main one
      
      # random.seed(self.seed)
      # np.random.seed(self.seed)
      
      # Randomly setting target position
      # self.target_position = (random.randint(0, self.dim-1), random.randint(0, self.dim-1))
      self.target_position = tuple(np.random.randint(0, self.dim, size=2))
      
      # print ('Target Position : {}'.format(self.target_position))

      # Boolean grid based on probability p so as to set each cell to be blocked / unblocked
      p_grid = np.random.choice([False, True], size=(self.dim, self.dim), p=[1-self.p, self.p])
      # Making sure target position and (0, 0) position are unblocked
      p_grid[self.target_position] = p_grid[0, 0] = False

      for i in range(self.dim):
        for j in range(self.dim):
          # Setting each cell to be blocked / unblocked based on p_grid
          grid[i][j].block = p_grid[i][j] 
          grid[i][j].target = False # Setting Node.target of each cell to be False
          if not p_grid[i][j]:
            # If a cell is unblocked, then we randomly assign it to a terrain type
            grid[i][j].terrain = self.terrainType(np.random.randint(0,3))      
      
      # Setting the Node.target of node in the target position to be True
      grid[self.target_position].target = True
    
    else: # If this gridworld is not the main one, but the one to track agent's knowledge base

      for i in range(self.dim):
        for j in range(self.dim):
          
          # Setting the initial p_target value to be 1/dim*dim
          grid[i][j].p_target = 1/(self.dim*self.dim)
          
          # Setting the p_find initially
          ## Update 0.35 with a variable value
          grid[i][j].p_find = 0.35*grid[i][j].p_target
   
    return grid

  # Prints the generated gridworld
  def printGrid(self): 
    
    print (np.array([[self.terrainSym(j.terrain)
                      if j.block == False 
                      else 'X' 
                      for j in i] 
                     for i in self.grid]))

  # Sets the node attribute to be Blocked
  # and updates the p_target and p_find of all cells
  def nodeBlocked(self, position): # Meant for the gridworld_explore

    self.grid[position].block = True # Setting the respective node to Blocked

    for i in range(self.dim):
      for j in range(self.dim):
        if (i, j) == position:
          continue
        else: 
          self.grid[i, j].p_target = self.grid[i, j].p_target / (1 - self.grid[position].p_target)
          self.grid[i, j].p_find = self.grid[i, j].p_target * (1 - self.grid[i, j].terrainFNR())

    self.grid[position].p_target = 0
    self.grid[position].p_find = 0

  # Sets the node attribute to be Blocked 
  # and stores the now-seen terrain type in the agent's knowledge gridworld
  def nodeOpen(self, position, terrain): # Meant for the gridworld_explore

    self.grid[position].block = False
    self.grid[position].terrain = terrain

  # Looks for target in a particular node considering the false negative rate
  def targetSearch(self, position, agent): # Meant for gridworld_real
    agent.action_count += 1
    if self.target_position == position:
      if random.random() >  self.grid[position].terrainFNR():
        return True
    return False

  # Updates the p_target and p_find of all cells
  # considering that we failed to find the target in a particular node
  def searchFailed(self, position): # Meant for the gridworld_explore
    # print ('Search failed in {}'.format(position))
    for i in range(self.dim):
      for j in range(self.dim):
        if (i, j) == position:
          continue
        else:
          self.grid[i, j].p_target = self.grid[i, j].p_target / (1 - self.grid[position].p_target * (1 - self.grid[position].terrainFNR()))
          self.grid[i, j].p_find = self.grid[i, j].p_target * (1 - self.grid[i, j].terrainFNR())

    self.grid[position].p_target = (self.grid[position].p_target * self.grid[position].terrainFNR()) / (1 - self.grid[position].p_target * (1 - self.grid[position].terrainFNR()))
    self.grid[position].p_find = self.grid[position].p_target *(1 - self.grid[position].terrainFNR())

  def tryPath(self, path, agent): # Meant for gridworld_real
    # print ('tryPath started')
    for index, position in enumerate(path):
      ## What happens if the node is already visited?
      agent.gridworld.grid[position].visited = True # Setting the node to Visited
      agent.action_count += 1

      if self.grid[position].block == True: # If a block is detected
        agent.gridworld.nodeBlocked(position) 
        return False
      else:
        agent.gridworld.nodeOpen(position, self.grid[position].terrain)
        agent.position = position # Agent is moved to the next node in the path
    
    return True
