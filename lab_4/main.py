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


class SoundManager:
    def __init__(self):
        self.flap = pygame.mixer.Sound("assets/wing.ogg")
        self.death = pygame.mixer.Sound("assets/hit.ogg")
        self.score = pygame.mixer.Sound("assets/point.ogg")
        self.timer = 0
        self.cooldown = Config.SCORE_SOUND

    def play_flap(self):
        self.flap.play()

    def play_death(self):
        self.death.play()

    def update_score_sound(self):
        self.timer -= 1
        if self.timer <= 0:
            self.score.play()
            self.timer = self.cooldown

    def reset_timer(self):
        self.timer = self.cooldown


class ResourceManager:
    @staticmethod
    def load_image(path, alpha=False):
        if alpha:
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()

    @staticmethod
    def load_font(path, size):
        return pygame.font.Font(path, size)


class ScoreManager:
    def __init__(self):
        self.current = 0
        self.high = 0
        self.pipes_passed = 0
        self.achievements = {
            'first_pipe': False,
            '10_points': False,
            '20_points': False,
            '50_points': False
        }

    def add_survival_score(self):
        self.current += 0.01

    def add_pipe_score(self):
        self.current += 1
        self.pipes_passed += 1
        self.check_achievements()

    def check_achievements(self):
        if not self.achievements['first_pipe'] and self.pipes_passed >= 1:
            self.achievements['first_pipe'] = True
            print("Achievement: First Pipe!")

        if not self.achievements['10_points'] and self.current >= 10:
            self.achievements['10_points'] = True
            print("Achievement: 10 Points!")

        if not self.achievements['20_points'] and self.current >= 20:
            self.achievements['20_points'] = True
            print("Achievement: 20 Points!")

        if not self.achievements['50_points'] and self.current >= 50:
            self.achievements['50_points'] = True
            print("Achievement: 50 Points!")

    def game_over(self):
        if self.current > self.high:
            self.high = self.current

    def reset(self):
        self.current = 0
        self.pipes_passed = 0
        for key in self.achievements:
            self.achievements[key] = False

    def get_display_score(self):
        return int(self.current)

    def get_display_high(self):
        return int(self.high)


class Bird:
    def __init__(self, screen_height):
        self.frames = [
            ResourceManager.load_image("assets/bluebird.png", alpha=True),
            ResourceManager.load_image("assets/bluebird-midflap.png", alpha=True),
            ResourceManager.load_image("assets/bluebird-upflap.png", alpha=True)
        ]
        self.screen_height = screen_height
        self.reset()
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, Config.BIRD_ANIM)

    def reset(self):
        self.frame = 0
        self.surface = self.frames[self.frame]
        self.rect = self.surface.get_rect(center=(50, self.screen_height / 2))
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
    def __init__(self):
        self.pipes = []
        self.passed_pipes = set()
        self.pipe_img = ResourceManager.load_image("assets/pipe-green.png", alpha=True)
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, Config.PIPE_SPAWN)

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

    def check_pipe_passed(self, bird_x):
        score = 0
        for i in range(0, len(self.pipes), 2):
            if i not in self.passed_pipes and self.pipes[i].centerx < bird_x:
                self.passed_pipes.add(i)
                score += 1
        return score

    def clear(self):
        self.pipes.clear()
        self.passed_pipes.clear()


class Floor:
    def __init__(self, screen_height):
        self.img = ResourceManager.load_image("assets/base.png", alpha=True)
        self.x = 0
        self.screen_height = screen_height

    def update(self):
        self.x -= Config.FLOOR_SPEED
        if self.x <= -200:
            self.x = 0

    def draw(self, screen):
        y = self.screen_height - Config.FLOOR_H
        screen.blit(self.img, (self.x, y))
        screen.blit(self.img, (self.x + 200, y))


class GameFactory:
    @staticmethod
    def create_bird():
        return Bird(Config.SCREEN_H)

    @staticmethod
    def create_pipe_manager():
        return PipeManager()

    @staticmethod
    def create_floor():
        return Floor(Config.SCREEN_H)

    @staticmethod
    def create_sound_manager():
        return SoundManager()

    @staticmethod
    def create_score_manager():
        return ScoreManager()


class GameEngine:
    def __init__(self, factory=GameFactory()):
        self.screen = pygame.display.set_mode((Config.SCREEN_W, Config.SCREEN_H))
        self.clock = pygame.time.Clock()

        # Dependency Injection через фабрику
        self.bird = factory.create_bird()
        self.pipes = factory.create_pipe_manager()
        self.floor = factory.create_floor()
        self.sound = factory.create_sound_manager()
        self.score = factory.create_score_manager()

        self.font = ResourceManager.load_font("assets/FlappyBirdy.ttf", 40)
        self.bg = ResourceManager.load_image("assets/background-night.png")
        self.game_over_img = ResourceManager.load_image("assets/message.png", alpha=True)
        self.game_over_rect = self.game_over_img.get_rect(center=(Config.SCREEN_W / 2, Config.SCREEN_H / 2))

        self.state = GameState.MAIN

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
                    self.sound.play_flap()
                else:
                    self.state = GameState.MAIN
                    self.pipes.clear()
                    self.bird.reset()
                    self.score.reset()
                    self.sound.reset_timer()

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
                self.sound.play_death()
                self.score.game_over()
                self.state = GameState.OVER

            self.score.add_survival_score()
            pipe_score = self.pipes.check_pipe_passed(self.bird.rect.centerx)
            if pipe_score > 0:
                self.score.add_pipe_score()

            self.sound.update_score_sound()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.pipes.draw(self.screen)
        self.bird.draw(self.screen)
        self.floor.draw(self.screen)

        if self.state == GameState.MAIN:
            score_text = self.font.render(str(self.score.get_display_score()), True, (255, 255, 255))
            self.screen.blit(score_text, score_text.get_rect(center=(Config.SCREEN_W / 2, 50)))
        else:
            self.screen.blit(self.game_over_img, self.game_over_rect)
            score_text = self.font.render(f"Score:{self.score.get_display_score()}", True, (255, 255, 255))
            high_text = self.font.render(f"High:{self.score.get_display_high()}", True, (255, 255, 255))
            self.screen.blit(score_text, score_text.get_rect(center=(Config.SCREEN_W / 2, 50)))
            self.screen.blit(high_text, high_text.get_rect(center=(Config.SCREEN_W / 2, 410)))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(Config.FPS)


if __name__ == "__main__":
    pygame.mixer.pre_init()
    pygame.init()
    GameEngine().run()