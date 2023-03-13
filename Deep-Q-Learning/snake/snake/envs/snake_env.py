import pygame, sys, time, random
from pygame.surfarray import array3d
from pygame import display
import numpy as np
import gym
from gym import error,spaces,utils
from gym.utils import seeding

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)

class SnakeEnv(gym.Env):
    metadata = {'render.modes':['human']}
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.frame_size_x = 200
        self.frame_size_y = 200
        self.game_window = pygame.display.set_mode((self.frame_size_x,self.frame_size_y))
        # Reset the game
        self.reset()
        self.STEP_LIMIT = 5000
        self.sleep = 0
        
    def reset(self):
        '''
        .reset() NEEDS to return ONLY observation
        '''
        self.game_window.fill(BLACK)
        self.snake_pos = [100,50]
        self.snake_body = [[100,50],[90,50],[80,50]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        self.direction = "RIGHT"
        self.action = self.direction
        
        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface())
        img = np.swapaxes(img,0,1)
        return img
    
    @staticmethod
    def change_direction(action,direction):
        '''
        0 --> UP
        1 --> DOWN
        2 --> LEFT
        3 --> RIGHT
        '''
        if action == 0 and direction != 1:
            direction = 'UP'
        if action == 1 and direction != 0:
            direction = 'DOWN'
        if action == 2 and direction != 3:
            direction = 'LEFT'
        if action == 3 and direction != 2:
            direction = 'RIGHT'
        return direction
    
    @staticmethod
    def move(direction,snake_pos):
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10
        return snake_pos
        
    def spawn_food(self):
        '''
        Spawn food in a random location on window size
        '''
        return [random.randrange(1,(self.frame_size_x//10))*10,
                random.randrange(1,(self.frame_size_y//10))*10]    
    
    def eat(self):
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]
    
    def step(self,action):
        '''
        What happens when your agent performs the action on the enviroment
        '''
        scoreholder = self.score
        reward = 0
        self.direction = SnakeEnv.change_direction(action, self.direction)
        self.snake_pos = SnakeEnv.move(self.direction,self.snake_pos)
        self.snake_body.insert(0, list(self.snake_pos))
        # reward handler to report back reward
        reward = self.food_handler()
        # update env after action
        self.update_game_state()
        reward,done = self.game_over(reward)
        # Get observation
        img = self.get_image_array_from_game()
        info = {'score':self.score}
        self.steps += 1
        time.sleep(self.sleep)
        return img,reward,done,info
    
    def food_handler(self):
        if self.eat():
            self.score += 1
            reward = 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward = 0
        
        if not self.food_spawn:
            self.food_pos = self.spawn_food()
        self.food_spawn = True
        return reward


    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img,0,1)
        return img

    def update_game_state(self):
        # Draw the snake
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window,GREEN,pygame.Rect(pos[0],pos[1],10,10))
        # Draw Food
        pygame.draw.rect(self.game_window,WHITE,pygame.Rect(self.food_pos[0],self.food_pos[1],10,10))
   
        
    def game_over(self,reward):
        # TOUCH BOUNDING BOX
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return -1,True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return -1,True
        # TOUCH BODY
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return -1,True
        if self.steps >= self.STEP_LIMIT:
            return 0,True
        return reward,False


    def render(self,mode='human'):
        if mode == 'human':
            display.update()

    def close(self):
        pass