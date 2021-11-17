from heapq import *

from node import Node
from gridworld import GridWorld
from agent import Agent


def AstarSearch(start, end, gridworld):
  # print ('A* started')
  
  # Making sure the nodes doesn't values from the previous A* runs
  for i in range(gridworld.dim):
    for j in range(gridworld.dim):
      gridworld.grid[i,j].parent = None # Removing parents
      gridworld.grid[i,j].g = 0 # Setting g to 0
      gridworld.grid[i,j].hofn(end) # Setting h for the new end position
      gridworld.grid[i,j].fofn() # Updating f based on g and h

  # Start and end node initialization
  start_node = gridworld.grid[start]
  end_node = gridworld.grid[end]

  #Setting up fringe (Priority Queue) & a closed list
  fringe, closed = [], []
  heapify(fringe)
  # closed = []

  # Inserting the start node into the fringe
  heappush(fringe, start_node)

  while len(fringe) != 0:
      
      # Setting current node to the node with the lowest f value
      current_node = heappop(fringe)
      # Putting the current node into the closed list
      closed.append(current_node)

      # If the end node is reached
      if current_node == end_node:
        return [True, current_node.pathFinder()]

      # Generate children of the current node
      children = current_node.generateChildren()

      for i in children: # For each children on current node

          i_new_g = current_node.g + 1          

          if i in closed: # If the children is already in the closed list
              continue # we don't have to explore it again

          if i in fringe: # If the children is already in the fringe

              k = [j for j in fringe if j == i][0]

              # If the existing version of children in the fringe has smaller g
              if k.g < i_new_g: 
                continue # we do nothing
              
              else: # Else we modify the children's g value to the new value
                k.parent = current_node
                k.g = i_new_g
                k.fofn()
                heapify(fringe)

          else: # If the children is not in the fringe, we insert
            i.parent = current_node
            i.g = i_new_g
            i.fofn()
            heappush(fringe, i)

  return [False, None]

def startVoyage(gridworld_real, agent_type):
  # print ('startVoyage started')
  # Checking to see if the given gridworld is solvable

  [status, path] = AstarSearch((0,0), gridworld_real.target_position, gridworld_real)

  # If no parth is available from (0, 0) to the target, we exit the program
  if status == False:
    # print ('No actual path available for the target. Try a new gridworld.')
    return False, None
  else:
    pass
    # print ('Path available for the given gridworld')

  # Blank gridworld to keep track of the agent's knowledge base
  gridworld_explore = GridWorld(gridworld_real.dim, gridworld_goal=gridworld_real)
  
  # New agent
  agent = Agent(gridworld_explore, typ=agent_type)
  agent.position = (0, 0) 
  
  # gridworld_real.exploreNode((0, 0), agent)

  # This loop goes on till we find the target
  while True:    
    # print ('Main while loop started')
    # Identifying probable position of the target node
    agent.goal_position = agent.getNextTarget() 

    # Trying to the reach the believed target node position
    # We get out of the while loop only after reaching the intended possible target node
    while agent.position != agent.goal_position:
      # print ('Inner while loop started')
      # Use A* to generate a possible path to the identified target
      [status, path] = AstarSearch(agent.position, agent.goal_position, agent.gridworld)
      
      ## This if statement is probabaly redundant. Have to check and remove
      if status == False:
        # print ('A boxed node seem to have the highest probability. Marking it as blocked.')
        agent.gridworld.grid[agent.goal_position].visited = True
        agent.gridworld.nodeBlocked(agent.goal_position)
        agent.goal_position = agent.getNextTarget() 
        continue

      # Moving through the estimated path
      status = gridworld_real.tryPath(path, agent)
      
      # If a block was detected when trying out the estimated path
      # we check which node has the highest p_target and assign that as agent's next target
      if not status:
        # print ('A block detected during tryPath')
        agent.goal_position = agent.getNextTarget()

    # Searching for target in the arrived node
    if gridworld_real.targetSearch(agent.position, agent): # If found, we exit
      return True, agent.action_count
    else: # If the target is not there, we update the p values accordingly
      agent.gridworld.searchFailed(agent.position)


def main(dim=20, p=0.3, trials = 100):

  data_dict = {}
  result = {}

  for agent in [6,7,8]:

    out = {'Flat': [], 'Hill': [], 'Forest': []}

    for i in range(trials):
        
      # Creating a randomly generated gridworld with blocked cells and cells of different terrain
      # This is going to be the gridworld we are trying to solve
      gridworld_real = GridWorld(dim, p, real=True)      
      # gridworld_real.printGrid()

      terrain = gridworld_real.grid[gridworld_real.target_position].terrain

      # Start solving the gridworld
      status, action_count = startVoyage(gridworld_real, agent_type=agent)
      if status:
        out[terrain].append(action_count)

      print ('Agent {}, Trial {}/{}'.format(agent, i+1, trials))

    data_dict[agent] = out

  print (data_dict)

  for agent in data_dict:
    for terrain in data_dict[agent]:
      if len(data_dict[agent][terrain])== 0:
        data_dict[agent][terrain] = None     
      else:
        data_dict[agent][terrain] = sum(data_dict[agent][terrain])/len(data_dict[agent][terrain])
                                                                       
  return data_dict

res = main(dim=20, p=0.3, trials = 500)
print (res)