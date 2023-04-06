import pygame
import sys
import random
import pygame.mixer


# Initialize Pygame
pygame.init()
pygame.mixer.init()


# Game constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
GRAVITY = 0.25
FLAP_POWER = 6.5
PIPE_GAP = 200
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Neil')
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load('images/background4.png').convert()
bird_image = pygame.image.load('images/NeilFace2.png').convert_alpha()
title_background_image = pygame.image.load('images/greatwall2.png').convert()
dead_bird_image = pygame.image.load('images/deadNeil.png').convert_alpha()
button_image = pygame.image.load('images/audio.png').convert_alpha()
click_sound = pygame.mixer.Sound('music/helloNeil.mp3')

def draw_button(screen, button_image, x, y):
    button_rect = button_image.get_rect(topleft=(x, y))
    screen.blit(button_image, button_rect)
    return button_rect


def show_title_screen():
    screen.fill(WHITE)
    screen.blit(title_background_image, (0, 0))

    # Draw title text
    font = pygame.font.Font(None, 72)
    title_text = font.render("Flappy Neil", True, (0, 0, 0))
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_text_rect)

    # Draw start button
    start_button = pygame.Surface((200, 100))
    start_button.fill((0, 0, 255))
    start_button_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 4))
    screen.blit(start_button, start_button_rect)

    # Draw start button text
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Start", True, WHITE)
    button_text_rect = button_text.get_rect(center=start_button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Draw audio button
    audio_button_rect = draw_button(screen, button_image, 10, 10)  # 10px from the top and left of the screen

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return
                if audio_button_rect.collidepoint(mouse_pos):
                    click_sound.play()
        clock.tick(FPS)



def draw_moving_background(x):
    background_width = background_image.get_width()
    background_repeat = (SCREEN_WIDTH // background_width) + 10  

    for i in range(background_repeat):
        screen.blit(background_image, (x + (i * background_width), 0))

def draw_score(score):
    font = pygame.font.Font(None, 56)
    text = font.render(str(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, 50)
    screen.blit(text, text_rect)

def show_game_over_screen():
    # Draw "Play Again" button
    play_again_button = pygame.Surface((200, 100))
    play_again_button.fill((0, 0, 255))
    play_again_button_rect = play_again_button.get_rect(center=(SCREEN_WIDTH // 2, 3 * SCREEN_HEIGHT // 4))
    screen.blit(play_again_button, play_again_button_rect)

    # Draw "Play Again" button text
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, WHITE)
    button_text_rect = button_text.get_rect(center=play_again_button_rect.center)
    screen.blit(button_text, button_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button_rect.collidepoint(mouse_pos):
                    return

        clock.tick(FPS)


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dy = 0
        self.dead = False
    
    def die(self):
        self.dead = True
        self.image = dead_bird_image

    def update(self):
        if not self.dead:
            self.dy += GRAVITY
            self.rect.y += self.dy

            if self.rect.top <= 0:
                self.rect.top = 0
                self.dy = 0
        else:
            self.rect.y += GRAVITY

    def flap(self):
        self.dy = -FLAP_POWER

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_upper):
        super().__init__()
        self.width = 80
        self.height = 640
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.is_upper = is_upper
        self.scored = False

        if is_upper:
            self.rect.bottom = y
        else:
            self.rect.top = y

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

def spawn_pipes():
    pipe_x = SCREEN_WIDTH
    pipe_y = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
    upper_pipe = Pipe(pipe_x, pipe_y - PIPE_GAP // 2, True)
    lower_pipe = Pipe(pipe_x, pipe_y + PIPE_GAP // 2, False)
    return (upper_pipe, lower_pipe)

def game_loop():
    show_title_screen()
    background_x = 0
    score = 0
    frame_count = 0

    pygame.mixer.music.load('music/music.ogg')
    pygame.mixer.music.play(-1)  # -1 means looping indefinitely

    bird = Bird()
    bird_group = pygame.sprite.Group(bird)
    pipe_group = pygame.sprite.Group()

    while True:
        screen.fill(WHITE)
        background_x -= PIPE_SPEED
        draw_moving_background(background_x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird_group.update()
        bird_group.draw(screen)

        # Spawn pipes
        if frame_count % (FPS * 2) == 0:
            pipe_pair = spawn_pipes()
            pipe_group.add(pipe_pair)

        # Update pipes
        pipe_group.update()
        pipe_group.draw(screen)

        # Scoring
        for pipe in pipe_group:
            if not pipe.scored and not pipe.is_upper and pipe.rect.right < bird.rect.left:
                score += 1
                pipe.scored = True

        # Draw score on screen
        draw_score(score)

        # Collision detection
        if pygame.sprite.spritecollideany(bird, pipe_group) or bird.rect.bottom >= SCREEN_HEIGHT:
            bird.die()
            pygame.mixer.music.stop()
            break

        # Update display and clock
        pygame.display.update()
        clock.tick(FPS)
        frame_count += 1
        
def main():
    show_title_screen()

    while True:
        game_loop()
        show_game_over_screen()


if __name__ == '__main__':
    main()
