import pygame
import os

# Khởi tạo các module của pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set caption cho cửa sổ
pygame.display.set_caption('Shooter')
pygame_icon = pygame.image.load('img/icons/health_box.png')
pygame.display.set_icon(pygame_icon)
# Set framerate
clock = pygame.time.Clock()
FPS = 60

gravity = 0.75
# Define player action variables
moving_left = False
moving_right = False
shoot = False
# Load images
# Bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

BACKGROUND = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


# Simple base class for visible game objects.
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.direction = 1
        self.val_y = 0
        self.jump = False
        self.in_air = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Load all images for players
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            temp_list = []
            # Count number of files in folder
            number_of_frames = os.listdir(f'img/{self.char_type}/{animation}')
            for i in range(len(number_of_frames)):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            # temp_list = []
            # for i in range(5):
            #     img = pygame.image.load(f'img/{self.char_type}/Run/{i}.png')
            #     img = pygame.transform.scale(
            #         img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            #     temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        animation_countdown = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_countdown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out the reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if new action is different the previous
        if new_action != self.action:
            self.action = new_action
            # Update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.update_animation()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and self.in_air < 2:
            self.val_y = -11
            dy += self.val_y
            self.jump = False
            self.in_air += 1

        # apply gravity
        self.val_y += gravity
        if self.val_y >= 10:
            self.val_y
        dy += self.val_y

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = 0
        # update rec position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction, 10)
            bullet_group.add(bullet)
            # reduce ammo after shoot
            self.ammo -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += self.direction * self.speed
        # Check if bullet has gone off screen
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - 100:
            self.kill()


# Create sprite groups
bullet_group = pygame.sprite.Group()

player = Soldier('player', 200, 200, 3, 5, 5)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)
# player2 = Soldier(400, 200, 3, 5)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw()
    enemy.draw()

    # Update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    # Update player action
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            # Jump
            player.update_action(2)
        elif moving_left or moving_right:
            # Run
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)
    for event in pygame.event.get():
        # Thoát game(Ấn dấu x)
        if event.type == pygame.QUIT:
            run = False
        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shoot = True
        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shoot = False
        # Keyboard pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w or event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()
pygame.quit()
