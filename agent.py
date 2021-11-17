class Agent:

  def __init__(self, gridworld, typ):
    self.gridworld = gridworld # Gridworld knowledge base of the agent
    self.type = typ # Agent type
    self.path = []
    self.gridworld.agent = self
    self.action_count = 0
    # print ('Agent initiated')

  # Returns the nearest target with least p_target
  def getNextTarget(self):

    # print ('Agent - getNextTarget initiated')
    max_p = 0
    max_p_node_positions = [] # List to keep track of all positions with least p_target
    
    if self.type == 6:

      for i in range(self.gridworld.dim):
        for j in range(self.gridworld.dim):

          if self.gridworld.grid[i, j].p_target > max_p:
            max_p = self.gridworld.grid[i, j].p_target
            max_p_node_positions.clear()
            max_p_node_positions.append((i,j))
          elif self.gridworld.grid[i, j].p_target == max_p:
            max_p_node_positions.append((i,j))

    elif self.type == 7:

      for i in range(self.gridworld.dim):
        for j in range(self.gridworld.dim):

          if self.gridworld.grid[i, j].p_find > max_p:
            max_p = self.gridworld.grid[i, j].p_find
            max_p_node_positions.clear()
            max_p_node_positions.append((i,j))
          elif self.gridworld.grid[i, j].p_find == max_p:
            max_p_node_positions.append((i,j))
    
    elif self.type == 8:
      
      for i in range(self.gridworld.dim):
        for j in range(self.gridworld.dim):
          
          dist_norm = 1 - (abs(self.position[0] - i) + abs(self.position[1] - j)/(2*self.gridworld.dim))
          alpha = 0.0002

          mod_p = self.gridworld.grid[i, j].p_find + alpha*dist_norm
          
          if mod_p > max_p:
            max_p = mod_p
            max_p_node_positions.clear()
            max_p_node_positions.append((i,j))
          elif mod_p == max_p:
            max_p_node_positions.append((i,j))
          
    if len(max_p_node_positions) == 1:
#       print ('Target decided : {}'.format(max_p_node_positions[0]))
      return max_p_node_positions[0]

    else:
      distance_from_agent = [abs(self.position[0] - pos[0]) + abs(self.position[1] - pos[0]) for pos in max_p_node_positions]
      min_distance = min(distance_from_agent)
      min_idx = []
      for idx, val in enumerate(distance_from_agent):
        if val==min_distance:
          min_idx.append(idx)
      target_choice = max_p_node_positions[random.choice(min_idx)]
#       print ('Target decided : {}'.format(target_choice))
      return target_choice

      # return max_p_node_positions[distance_from_agent.index(min(distance_from_agent))]