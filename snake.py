import pygame
import sys
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class APPLE:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, apple_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        
class BAD_APPLE:
    def __init__(self):
        self.randomize()

    def draw_bad_apple(self):
        bad_apple_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(bad_apple, bad_apple_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)



class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = APPLE()
        self.bad_apple = BAD_APPLE()  # Add this line


    def update(self):
        if not paused:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.draw_ground()
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.bad_apple.draw_bad_apple()  # Add this line
        self.draw_score()

        if paused:
            self.draw_paused_screen()

    def check_collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

            # Update the position of the bad_apple when the snake eats a regular apple
            self.bad_apple.randomize()

        if self.bad_apple.pos == self.snake.body[0]:  # Check for bad apple collision
            self.bad_apple.randomize()
            self.snake.body = self.snake.body[:-1]

        for block in self.snake.body[1:]:
            if block == self.apple.pos or block == self.bad_apple.pos:  # Check for both apples
                self.apple.randomize()
                self.bad_apple.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.snake.body[0].x = (self.snake.body[0].x + cell_number) % cell_number
        elif not 0 <= self.snake.body[0].y < cell_number:
            self.snake.body[0].y = (self.snake.body[0].y + cell_number) % cell_number

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_ground(self):
        ground_color = (120, 120, 120)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        ground_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, ground_color, ground_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        ground_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, ground_color, ground_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_paused_screen(self):
        paused_text = game_font.render("Paused", True, (255, 255, 255))
        screen.blit(paused_text, (screen.get_width() // 2 - paused_text.get_width() // 2, screen.get_height() // 2 - paused_text.get_height() // 2))




class MENU:
    def __init__(self):
        self.large_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
        self.normal_font = pygame.font.Font(None, 36)

        welcome_text = "Welcome to the Snake Game"
        goal_text1 = "Your goal is to get as many apples as you can."
        goal_text2 = "You can use the arrow keys to move the snake."
        goal_text3 = "Pause the game by pressing P."

        start_text = "Press Enter to Start"

        self.welcome_surface = self.large_font.render(welcome_text, True, (255, 255, 255))
        self.goal_surface1 = self.normal_font.render(goal_text1, True, (255, 255, 255))
        self.goal_surface2 = self.normal_font.render(goal_text2, True, (255, 255, 255))
        self.goal_surface3 = self.normal_font.render(goal_text3, True, (255, 255, 255))
        self.plus_one_surface = self.normal_font.render("+1", True, (255, 255, 255))
        self.minus_one_surface = self.normal_font.render("-1", True, (255, 255, 255))

        # Load the apple image
        self.apple_surface = pygame.image.load('Graphics/apple.png').convert_alpha()
        self.bad_apple_surface = pygame.image.load('Graphics/bad_apple.png').convert_alpha()


        self.start_surface = self.normal_font.render(start_text, True, (255, 255, 255))

        self.welcome_rect = self.welcome_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        self.goal_rect1 = self.goal_surface1.get_rect(center=(screen.get_width() // 2, self.welcome_rect.bottom + 40))
        self.goal_rect2 = self.goal_surface2.get_rect(center=(screen.get_width() // 2, self.goal_rect1.bottom + 10))
        self.goal_rect3 = self.goal_surface3.get_rect(center=(screen.get_width() // 2, self.goal_rect2.bottom + 10))

        # Create a box for the first apple.png image and the "+1" text
        self.box_width = max(self.apple_surface.get_width(), self.plus_one_surface.get_width()) + 20
        self.box_height = max(self.apple_surface.get_height() + self.plus_one_surface.get_height() + 20,
                              self.apple_surface.get_height() + self.minus_one_surface.get_height() + 20)

        # Adjust the X-coordinate to position the boxes next to each other
        self.box_rect1 = pygame.Rect((screen.get_width() - 2 * self.box_width - 20) // 2, self.goal_rect3.bottom + 20, self.box_width, self.box_height)

        self.apple_rect1 = self.apple_surface.get_rect(center=(self.box_rect1.centerx, self.box_rect1.centery - 10))
        self.plus_one_rect = self.plus_one_surface.get_rect(center=(self.box_rect1.centerx, self.box_rect1.centery + 10))

        # Create a box for the second apple.png image and the "-1" text with light green background
        self.box_rect2 = pygame.Rect(self.box_rect1.right + 20, self.box_rect1.top, self.box_width, self.box_height)

        self.apple_rect2 = self.bad_apple_surface.get_rect(center=(self.box_rect2.centerx, self.box_rect2.centery - 10))
        self.minus_one_rect = self.minus_one_surface.get_rect(center=(self.box_rect2.centerx, self.box_rect2.centery + 10))

        self.start_rect = self.start_surface.get_rect(center=(screen.get_width() // 2, 3 * screen.get_height() // 4))

    def draw_menu(self):
        screen.blit(self.welcome_surface, self.welcome_rect)
        screen.blit(self.goal_surface1, self.goal_rect1)
        screen.blit(self.goal_surface2, self.goal_rect2)
        screen.blit(self.goal_surface3, self.goal_rect3)

        # Draw the first box for the first apple.png image and the "+1" text
        pygame.draw.rect(screen, (130, 130, 130), self.box_rect1)
        screen.blit(self.apple_surface, self.apple_rect1)
        screen.blit(self.plus_one_surface, self.plus_one_rect)

        # Draw the second box for the second apple.png image and the "-1" text with light green background
        pygame.draw.rect(screen, (130, 130, 130), self.box_rect2)  # Light green color
        screen.blit(self.bad_apple_surface, self.apple_rect2)  # Same apple.png
        screen.blit(self.minus_one_surface, self.minus_one_rect)

        # Use a bold font for the "Press Enter to Start" text
        pygame.font.Font.set_bold(self.normal_font, True)
        screen.blit(self.start_surface, self.start_rect)
        pygame.font.Font.set_bold(self.normal_font, False)



pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
bad_apple = pygame.image.load('Graphics/bad_apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
menu = MENU()
game_active = False
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
        else:
            if event.type == SCREEN_UPDATE:
                if not paused:
                    main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_RETURN and paused:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    screen.fill((130, 130, 130))

    if not game_active:
        menu.draw_menu()
    else:
        main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)