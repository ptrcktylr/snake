import pygame
import random

# screen size, clock, & window
WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
clock = pygame.time.Clock()

# game
pygame.init()
pygame.display.set_caption('Snake by ptrcktylr')

# colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


# snake class
class Snake:
    def __init__(self, win):

        self.window = win
        self.update = pygame.display.update()

        self.width = 25
        self.velocity = 25

        # starts snake head at the middle of the game board
        start_position = (WIDTH // 2, WIDTH // 2)

        # stores snake body parts & starts with the start position
        self.body = [start_position] 

        # directions
        self.right = True
        self.left = False
        self.down = False
        self.up = False
    
    def move(self):
        self.keys = pygame.key.get_pressed()

        # if any((self.keys[pygame.K_UP], self.keys[pygame.K_DOWN], self.keys[pygame.K_RIGHT], self.keys[pygame.K_LEFT])):
        #     self.direction = self.keys[pygame.K_UP]*1 + self.keys[pygame.K_DOWN]*2 + self.keys[pygame.K_LEFT]*4 + self.keys[pygame.K_RIGHT]*8

        if self.keys[pygame.K_UP] and not self.down:
            self.up = True

            self.down = False
            self.left = False
            self.right = False
        
        elif self.keys[pygame.K_DOWN] and not self.up:
            self.down = True

            self.up = False
            self.left = False
            self.right = False

        elif self.keys[pygame.K_RIGHT] and not self.left:
            self.right = True

            self.down = False
            self.up = False
            self.left = False
        
        elif self.keys[pygame.K_LEFT] and not self.right:
            self.left = True

            self.right = False
            self.down = False
            self.up = False

        # make x and y the head of the snake
        x, y = self.body[0]
        # remove the last body part
        self.body.pop()

        if self.up == True:
            y = (y - self.velocity)
        elif self.down == True:
            y = (y + self.velocity)
        elif self.left == True:
            x = (x - self.velocity)
        elif self.right == True:
            x = (x + self.velocity)

        self.body.insert(0, (x, y))

    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(self.window, GREEN, (x, y, self.width, self.width)) # square body parts

    def eat(self, food):

        # set x and y to the head
        x, y = self.body[0]

        # if head collides with food
        if x == food.x and y == food.y:
            # add length
            self.body.append(self.body[-1])
            # eat
            return True

        return False


# food class
class Food:
    def __init__(self, win, x=None, y=None):
        self.window = win
        self.width = 25
        self.x, self.y = x, y
        if not x or not y: self.new_random_position(snake)

    def draw(self):
        pygame.draw.rect(self.window, RED, (self.x, self.y, 25, 25))

    def new_random_position(self, snake):
        self.x, self.y = random.choice(range(0, WIDTH, 25)), random.choice(range(0, WIDTH, 25))

        # while the food position is in the snakes body, get a new position
        while (self.x, self.y) in snake.body:
            print('food spawned in itself, spawning new food..')
            self.x, self.y = random.choice(range(0, WIDTH, 25)), random.choice(range(0, WIDTH, 25))


# game variables
snake = Snake(WIN)
food = Food(WIN)
food.new_random_position(snake)
score = 0

gameover = False

while not gameover:
    clock.tick(10)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            gameover = True

    # if we hit a wall, game is over
    if snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= WIDTH:
        gameover = True
    
    # if we hit our body, game is over
    for part in snake.body[1:-1]: # all parts except head
        if part == snake.body[0]: # if part pos equals head pos
            gameover = True

    # if we eat, increase length
    if snake.eat(food):
        score += 1
        food.new_random_position(snake)


    WIN.fill(BLACK)
    snake.move()

    food.draw()
    snake.draw()

    pygame.display.update()

pygame.quit()