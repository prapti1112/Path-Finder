import numpy as np
import node

class Q_Learning:
    
    def __init__(self, goal, start, map, noOfActions, noOfCells=20) -> None:
        self.start = start
        self.goal = goal
        self.map = map
        print(f"Map info: Length-({len(self.map)}, {len(self.map[0])}), 1st element: {self.map[0][0]}")
        
        self.cellCount = noOfCells
        self.actions = ['up', 'right', 'down', 'left']
        self.q_values = np.zeros((noOfCells, noOfCells, noOfActions))

        self.initialiseRewards()

        self.epsilon = 0.9 # the percentage of time when we should take the best action (instead of a random action)
        self.discount_factor = 0.9 # discount factor for future rewards
        self.learning_rate = 0.9 

        self.train()
    

    def initialiseRewards(self):
        self.rewards = np.full((self.cellCount, self.cellCount), -1.)
        
        for nodeRow in self.map:
            for node in nodeRow:
                print(node)
                if node.status == "obstacle":
                    self.rewards[node.x][node.y] = -100.
        
        self.rewards[self.goal[1]][self.goal[0]] = 100.
    

    def is_terminal_state(self, current_row_index, current_column_index):
        #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
        if self.rewards[current_row_index, current_column_index] == -1.:
            return False
        else:
            return True
    
    def get_random_location(self):
        #get a random row and column index
        current_row_index = np.random.randint(self.cellCount)
        current_column_index = np.random.randint(self.cellCount)
        #continue choosing random row and column indexes until a non-terminal state is identified
        #(i.e., until the chosen state is a 'white square').
        while self.is_terminal_state(current_row_index, current_column_index):
            current_row_index = np.random.randint(self.cellCount)
            current_column_index = np.random.randint(self.cellCount)
        return current_row_index, current_column_index
    
    
    def get_next_action(self, current_row_index, current_column_index, epsilon):
        #if a randomly chosen value between 0 and 1 is less than epsilon, then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else: # Choose a random action
            return np.random.randint(4)
    

    def get_next_location(self, current_row_index, current_column_index, action_index):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'right' and current_column_index < self.cellCount - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'down' and current_row_index < self.cellCount - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            new_column_index -= 1
        
        return new_row_index, new_column_index
    

    # def get_shortest_path(self, start_row_index, start_column_index):
    #     #return immediately if this is an invalid starting location
    #     if self.is_terminal_state(start_row_index, start_column_index):
    #         return []
    #      #if this is a 'legal' starting location
    #     current_row_index, current_column_index = start_row_index, start_column_index
    #     shortest_path = []
    #     shortest_path.append([current_row_index, current_column_index])
    #     #continue moving along the path until we reach the goal (i.e., the item packaging location)
    #     while not self.is_terminal_state(current_row_index, current_column_index):
    #     #get the best action to take
    #         action_index = self.get_next_action(current_row_index, current_column_index, 1.)
    #         #move to the next location on the path, and add the new location to the list
    #         current_row_index, current_column_index = self.get_next_location(current_row_index, current_column_index, action_index)
    #         shortest_path.append([current_row_index, current_column_index])
    #     return shortest_path
        

    def train(self):
        for episode in range(1000):
        #get the starting location for this episode
            row_index, column_index = self.get_random_location()

            #continue taking actions (i.e., moving) until we reach a terminal state
            #(i.e., until we reach the item packaging area or crash into an item storage location)
            while not self.is_terminal_state(row_index, column_index):
                #choose which action to take (i.e., where to move next)
                action_index = self.get_next_action(row_index, column_index, self.epsilon)

                #perform the chosen action, and transition to the next state (i.e., move to the next location)
                old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
                row_index, column_index = self.get_next_location(row_index, column_index, action_index)
                
                #receive the reward for moving to the new state, and calculate the temporal difference
                reward = self.rewards[row_index, column_index]
                old_q_value = self.q_values[old_row_index, old_column_index, action_index]
                temporal_difference = reward + (self.discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value

                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (self.learning_rate * temporal_difference)
                self.q_values[old_row_index, old_column_index, action_index] = new_q_value

            print(f"Episode {episode} completed !!!!!")

        print('Training complete!')
    

    def getPath(self, m=None, s=None, g= None):
        
        self.path = []
        
        if self.is_terminal_state(self.start[0], self.start[1]):
            return []
         #if this is a 'legal' starting location
        current_row_index, current_column_index = self.start[0], self.start[1]
        
        self.path.append(self.map[current_row_index][current_column_index])
        
        #continue moving along the path until we reach the goal (i.e., the item packaging location)
        while not self.is_terminal_state(current_row_index, current_column_index):
        #get the best action to take
            action_index = self.get_next_action(current_row_index, current_column_index, 1.)
            #move to the next location on the path, and add the new location to the list
            current_row_index, current_column_index = self.get_next_location(current_row_index, current_column_index, action_index)
            self.path.append(self.map[current_row_index][current_column_index])

        return self.path, self.map

        
        
        
