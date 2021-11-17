class Node:
     
    def __init__(self, position, gridworld):

        self.position = position # Node position
        self.gridworld = gridworld # Gridworld the node belongs to
        self.parent = None # Parent of the node. Would be useful during A*
        self.block = None # If a node is blocked or not
        self.visited = False # If a node is visited / explored
        self.terrain = None # Terrain type of a node

        self.g = self.h = self.f = 0 # Initial f, g, h values of the node

    # Magic methods to compare two nodes
    def __lt__(self, other): # Check if one node is less than other
      return self.f < other.f
    def __eq__(self, other): # Check if two nodes are equal
      return self.position == other.position
    
    def hofn(self, goal): # Updates h(n) using Manhattan distance
        self.h = abs(goal[0] - self.position[0]) + abs(goal[1] - self.position[1])
    
    def fofn(self): # Updates f(n) as the sum of h(n) and g(n)
        self.f = self.g + self.h
    
    # Returns False Negative Rate (FNR) of respective nodes based on the terrain type
    def terrainFNR(self): 
      terrain_dict = {'Flat':0.2, 'Hill':0.5, 'Forest':0.8, None: 0.65}
      return terrain_dict[self.terrain]
      
    # Generates path from a given node using its parents
    def pathFinder(self): 
      path = [self.position]
      parent = self.parent
      while parent is not None:
        path.append(parent.position)
        parent = parent.parent
      return path[::-1]

    # Generates children of a node
    def generateChildren(self):
      self.children = []
      for i in [(self.position[0]-1, self.position[1]),
                (self.position[0]+1, self.position[1]),
                (self.position[0], self.position[1]-1),
                (self.position[0], self.position[1]+1)]:
          if i[0] >= 0 and i[1] >= 0 and i[0] < self.gridworld.dim and i[1] < self.gridworld.dim:
              if self.gridworld.grid[i].block != True:
                  self.children.append(self.gridworld.grid[i])
      return self.children
