import pygame, sys, random
from enum import Enum


class GameState(Enum):
    MAIN = "main_game"
    OVER = "game_over"


class Config:
    SCREEN_W = 288
    SCREEN_H = 512
    FPS = 60
    GRAVITY = 0.25
    FLOOR_H = 75
    PIPE_SPEED = 5
    FLOOR_SPEED = 1
    JUMP = -5
    PIPE_GAP = 450
    PIPE_SPAWN = 1000
    BIRD_ANIM = 200
    SCORE_SOUND = 100
    PIPE_HEIGHTS = [200, 250, 300, 350, 400]


class Bird:
    def __init__(self, config):
        self.config = config
        self.frames = [
            pygame.image.load("assets/bluebird.png").convert_alpha(),
            pygame.image.load("assets/bluebird-midflap.png").convert_alpha(),
            pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
        ]
        self.reset()
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, config.BIRD_ANIM)

    def reset(self):
        self.frame = 0
        self.surface = self.frames[self.frame]
        self.rect = self.surface.get_rect(center=(50, Config.SCREEN_H / 2))
        self.movement = 0

    def update(self):
        self.movement += Config.GRAVITY
        self.rect.centery += self.movement

    def jump(self):
        self.movement = 0
        self.movement += Config.JUMP

    def draw(self, screen):
        rotated = pygame.transform.rotozoom(self.surface, -self.movement * 5, 1)
        screen.blit(rotated, self.rect)

    def animate(self):
        self.frame = (self.frame + 1) % len(self.frames)
        self.surface = self.frames[self.frame]


class PipeManager:
    def __init__(self, config):
        self.config = config
        self.pipes = []
        self.pipe_img = pygame.image.load("assets/pipe-green.png")
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, config.PIPE_SPAWN)

    def spawn(self):
        height = random.choice(Config.PIPE_HEIGHTS)
        bottom = self.pipe_img.get_rect(midtop=(500, height))
        top = self.pipe_img.get_rect(midtop=(500, height - Config.PIPE_GAP))
        self.pipes.extend([bottom, top])

    def update(self):
        for pipe in self.pipes:
            pipe.centerx -= Config.PIPE_SPEED

    def draw(self, screen):
        for pipe in self.pipes:
            if pipe.bottom >= Config.SCREEN_H:
                screen.blit(self.pipe_img, pipe)
            else:
                flip = pygame.transform.flip(self.pipe_img, False, True)
                screen.blit(flip, pipe)


class Floor:
    def __init__(self):
        self.img = pygame.image.load("assets/base.png")
        self.x = 0

    def update(self):
        self.x -= Config.FLOOR_SPEED
        if self.x <= -200:
            self.x = 0

    def draw(self, screen):
        y = Config.SCREEN_H - Config.FLOOR_H
        screen.blit(self.img, (self.x, y))
        screen.blit(self.img, (self.x + 200, y))


class GameEngine:
    def __init__(self):
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.SCREEN_W, self.config.SCREEN_H))
        self.clock = pygame.time.Clock()

        self.bird = Bird(self.config)
        self.pipes = PipeManager(self.config)
        self.floor = Floor()
        self.font = pygame.font.Font("assets/FlappyBirdy.ttf", 40)
        self.bg = pygame.image.load("assets/background-night.png")
        self.game_over_img = pygame.image.load("assets/message.png")
        self.game_over_rect = self.game_over_img.get_rect(center=(self.config.SCREEN_W / 2, self.config.SCREEN_H / 2))

        self.state = GameState.MAIN
        self.score = 0
        self.high_score = 0
        self.sound_timer = self.config.SCORE_SOUND

        self.flap_sound = pygame.mixer.Sound("assets/wing.ogg")
        self.death_sound = pygame.mixer.Sound("assets/hit.ogg")
        self.score_sound = pygame.mixer.Sound("assets/point.ogg")

    def check_collision(self):
        for pipe in self.pipes.pipes:
            if self.bird.rect.colliderect(pipe):
                return False
        if self.bird.rect.top <= -100 or self.bird.rect.bottom >= Config.SCREEN_H - Config.FLOOR_H:
            return False
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state == GameState.MAIN:
                    self.bird.jump()
                    self.flap_sound.play()
                else:
                    self.state = GameState.MAIN
                    self.pipes.pipes.clear()
                    self.bird.reset()
                    self.score = 0

            if event.type == self.pipes.SPAWNPIPE and self.state == GameState.MAIN:
                self.pipes.spawn()

            if event.type == self.bird.BIRDFLAP:
                self.bird.animate()

    def update(self):
        if self.state == GameState.MAIN:
            self.bird.update()
            self.pipes.update()
            self.floor.update()

            if not self.check_collision():
                self.death_sound.play()
                self.high_score = max(self.score, self.high_score)
                self.state = GameState.OVER

            self.score += 0.01
            self.sound_timer -= 1
            if self.sound_timer <= 0:
                self.score_sound.play()
                self.sound_timer = self.config.SCORE_SOUND

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.pipes.draw(self.screen)
        self.bird.draw(self.screen)
        self.floor.draw(self.screen)

        if self.state == GameState.MAIN:
            score_text = self.font.render(str(int(self.score)), True, (255, 255, 255))
            self.screen.blit(score_text, score_text.get_rect(center=(self.config.SCREEN_W / 2, 50)))
        else:
            self.screen.blit(self.game_over_img, self.game_over_rect)
            score_text = self.font.render(f"Score:{int(self.score)}", True, (255, 255, 255))
            high_text = self.font.render(f"High:{int(self.high_score)}", True, (255, 255, 255))
            self.screen.blit(score_text, score_text.get_rect(center=(self.config.SCREEN_W / 2, 50)))
            self.screen.blit(high_text, high_text.get_rect(center=(self.config.SCREEN_W / 2, 410)))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.config.FPS)


if __name__ == "__main__":
    pygame.mixer.pre_init()
    pygame.init()
    GameEngine().run()