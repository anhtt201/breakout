import random

import pygame

pygame.init()

# Define screen size
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# Define background color
background_color = (234, 218, 184)
background_sky_image = pygame.image.load('img/sky.png')
background_sky_rect = background_sky_image.get_rect()
x = 0
background_sun_image = pygame.image.load('img/sun.png')

# Define block color
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

# Define paddle color
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

# Define text color
text_color = (78, 81, 139)
# Define game variables
# cols = random.randint(1, 10)
# rows = random.randint(1, 10)
cols = 14
rows = 4
clock = pygame.time.Clock()
FPS = 60
live_ball = False
game_over = 0
MENU = True
random_numbers = []

# Define button image
restart_img = pygame.image.load('img/restart_btn.png')
restart_img = pygame.transform.scale(restart_img, (restart_img.get_width() * 2, restart_img.get_height() * 2))
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# brick wall class
class Wall():
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols

    def create_wall(self):
        self.block = []
        # define an empty list for an individual block
        block_individual = []
        for row in range(self.rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(self.cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = random.randint(row, self.rows) * self.height
                rect = pygame.Rect(block_x, block_y + 50, self.width, self.height)
                # assign block strength based on row
                # if row < 2:
                #     strength = 3
                # elif row < 4:
                #     strength = 2
                # elif row < 6:
                #     strength = 1
                # create a list at this point to store the rect and colour data
                strength = random.randint(1, 3)
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.block.append(block_row)

    def draw_wall(self):
        for row in self.block:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, background_color, (block[0]), 2)


class Paddle():
    def __init__(self, width, height, speed, score, level, life):
        self.width = width
        self.height = height
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2)
        self.y = SCREEN_HEIGHT - (self.height * 2)
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        self.score = score
        self.level = level
        self.life = life

    def move(self):
        # Reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.direction = 1

    def draw_paddle(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self, width, height, speed, score, level, life):
        self.__init__(width, height, speed, score, level, life)


class Ball():
    def __init__(self, x, y, radius, speed_x, speed_y, speed_max, game_over):
        self.x = x - radius
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.speed_max = speed_max
        self.game_over = game_over
        self.score = 0

    def move(self):
        # collision threshold
        collision_thresh = 5

        # start off with the assumption that the wall has been destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall.block:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    ball_sound.play()
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        paddle.score += 10
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                        paddle.score += 10
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        paddle.score += 10
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                        paddle.score += 10
                    # reduce the block's strength by doing damage to it
                    if wall.block[row_count][item_count][1] > 1:
                        wall.block[row_count][item_count][1] -= 1
                    else:
                        wall.block[row_count][item_count][0] = (0, 0, 0, 0)

                # check if block still exists, in which case the wall is not destroyed
                if wall.block[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
            paddle.level += 1
            paddle.life += 1
            wall.rows += 1
            wall.cols += 1
            wall.width = SCREEN_WIDTH // wall.cols

        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.game_over = -1
            paddle.life -= 1

        # look for collission with paddle
        if self.rect.colliderect(paddle):
            ball_sound.play()
            # check if colliding from the top
            if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius, 3)

    def reset(self, x, y, radius, speed_x, speed_y, speed_max, game_over):
        self.__init__(x, y, radius, speed_x, speed_y, speed_max, game_over)


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action


# Create a wall
wall = Wall(50, 30, 1, SCREEN_WIDTH // random.randint(10, 30))
wall.create_wall()

# Create a paddle
paddle = Paddle(100, 20, 8, 0, 1, 1)

# Create a ball
ball = Ball(paddle.x + (paddle.width // 2), paddle.y - paddle.height, 10, 4, -4, 5, 0)

# Create a button
restart_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2, restart_img)
start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 180, start_img)
exit_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 80, exit_img)

# Create ball bounce sound
ball_sound = pygame.mixer.Sound('audio/bounce.wav')
winning_sound = pygame.mixer.Sound('audio/win.wav')
losing_sound = pygame.mixer.Sound('audio/lose.wav')
win_play_sound = 0
lose_play_sound = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BREAKOUT")
logo_icon = pygame.image.load('img/Breakout/Icons/logo.jpg').convert_alpha()
pygame.display.set_icon(logo_icon)

# Define font
font = pygame.font.SysFont('Constantia', 30)
run = True


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


max_level = 5

while run:

    clock.tick(FPS)
    screen.fill(background_color)

    if MENU:
        rel_x = x % background_sky_image.get_rect().width
        screen.blit(background_sky_image, (rel_x - background_sky_image.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            screen.blit(background_sky_image, (rel_x, 0))
        x -= 5
        # screen.blit(background_sky_image, background_sky_rect.move(-background_sky_rect.width, 0))
        # background_sky_rect.move_ip(5, 0)
        # if background_sky_rect.left == SCREEN_WIDTH:
        #     background_sky_rect.x = 0
        screen.blit(background_sun_image, (SCREEN_WIDTH - 100, 50))
        if exit_button.draw():
            run = False
        if start_button.draw():
            MENU = False
    else:
        # Draw objects
        wall.draw_wall()
        paddle.draw_paddle()
        ball.draw()
        score = font.render(f"Score: {paddle.score}", True, (0, 0, 0))
        screen.blit(score, (0, 0))
        life = font.render(f"Lives: {paddle.life}", True, (0, 0, 0))
        screen.blit(life, (SCREEN_WIDTH // 2 - 50, 0))
        if paddle.level <= max_level:
            level = font.render(f"Level: {paddle.level}", True, (0, 0, 0))
            screen.blit(level, (SCREEN_WIDTH - 100, 0))
        if live_ball:
            paddle.move()
            game_over = ball.move()
            if game_over != 0:
                live_ball = False
        if not live_ball:
            if game_over == 0:
                draw_text("Press enter or space to play", font, text_color, 230, SCREEN_HEIGHT // 2)
            elif game_over == 1:
                if paddle.level <= max_level:
                    draw_text(f"Next level: {paddle.level}", font, text_color, 300, SCREEN_HEIGHT // 2 - 50)
                    draw_text("Press enter or space to continue", font, text_color, 170,
                              SCREEN_HEIGHT // 2)
                else:
                    draw_text("You won", font, text_color, 350, SCREEN_HEIGHT // 2 - 50)
                    draw_text("Press enter or space to play again", font, text_color, 200,
                              SCREEN_HEIGHT // 2)
                if not win_play_sound:
                    winning_sound.play()
                    win_play_sound = 1
            elif game_over == -1:
                if not lose_play_sound:
                    losing_sound.play()
                    lose_play_sound = 1
                if restart_button.draw():
                    if paddle.life > 0:
                        ball.reset(paddle.x + (paddle.width // 2), paddle.y - paddle.height, 10, 4, -4, 5, 0)
                        paddle = Paddle(100, 20, 8, paddle.score, paddle.level, paddle.life)
                        wall.create_wall()
                        losing_sound.stop()
                        game_over = 0
                    if paddle.life == 0:
                        ball.reset(paddle.x + (paddle.width // 2), paddle.y - paddle.height, 10, 4, -4, 5, 0)
                        paddle = Paddle(100, 20, 8, 0, 1, 1)
                        wall.rows = 1
                        wall.cols = random.randint(3, 6)
                        wall.width = SCREEN_WIDTH // wall.cols
                        wall.create_wall()
                        game_over = 0
                        losing_sound.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if (event.type == pygame.KEYDOWN and (
                event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER)) \
                and not live_ball and game_over != -1:
            live_ball = True
            ball.reset(paddle.x + (paddle.width // 2), paddle.y - paddle.height, 10, 4, -4, 5, 0)
            if game_over == 1 and paddle.level <= max_level:
                wall.create_wall()
                paddle = Paddle(100, 20, 8, paddle.score, paddle.level, paddle.life)
            if paddle.level > max_level:
                MENU = True
                wall.rows = 1
                wall.cols = random.randint(3, 6)
                wall.width = SCREEN_WIDTH // wall.cols
                wall.create_wall()
                paddle = Paddle(100, 20, 8, 0, 1, 1)
            winning_sound.stop()
            win_play_sound = 0
            lose_play_sound = 0
    pygame.display.update()
pygame.quit()
