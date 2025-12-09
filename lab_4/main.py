import pygame, sys, random


# ============ КЛАСС КОНФИГУРАЦИИ ============
class Config:
    SCREEN_WIDTH = 288
    SCREEN_HEIGHT = 512
    FPS = 60
    GRAVITY = 0.25
    FLOOR_HEIGHT = 75
    PIPE_SPEED = 5
    FLOOR_SPEED = 1
    BIRD_JUMP = -5
    PIPE_GAP = 450
    PIPE_SPAWN_RATE = 1000  # ms
    BIRD_ANIMATION_RATE = 200  # ms
    SCORE_SOUND_INTERVAL = 100


# ============ КЛАСС ПТИЦЫ ============
class Bird:
    def __init__(self, config):
        self.config = config
        self.load_images()
        self.reset()

        # Анимация
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, config.BIRD_ANIMATION_RATE)

    def load_images(self):
        self.frames = [
            pygame.image.load("assets/bluebird.png").convert_alpha(),
            pygame.image.load("assets/bluebird-midflap.png").convert_alpha(),
            pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
        ]

    def reset(self):
        self.frame_index = 0
        self.surface = self.frames[self.frame_index]
        self.rect = self.surface.get_rect(center=(50, Config.SCREEN_HEIGHT / 2))
        self.movement = 0

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.surface = self.frames[self.frame_index]
        self.rect = self.surface.get_rect(center=(50, self.rect.centery))

    def jump(self):
        self.movement = 0
        self.movement += Config.BIRD_JUMP

    def update(self):
        self.movement += Config.GRAVITY
        self.rect.centery += self.movement

    def draw(self, screen):
        rotated_bird = pygame.transform.rotozoom(
            self.surface,
            -self.movement * 5,
            1
        )
        screen.blit(rotated_bird, self.rect)

    def get_rect(self):
        return self.rect


# ============ КЛАСС УПРАВЛЕНИЯ ТРУБАМИ ============
class PipeManager:
    def __init__(self, config):
        self.config = config
        self.pipe_list = []
        self.pipe_surface = pygame.image.load("assets/pipe-green.png")
        self.pipe_heights = [200, 250, 300, 350, 400]

        # Таймер спавна труб
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, config.PIPE_SPAWN_RATE)

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_heights)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos - Config.PIPE_GAP))
        return bottom_pipe, top_pipe

    def spawn_pipe(self):
        self.pipe_list.extend(self.create_pipe())

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= Config.PIPE_SPEED

    def draw_pipes(self, screen):
        for pipe in self.pipe_list:
            if pipe.bottom >= Config.SCREEN_HEIGHT:
                screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

    def get_pipes(self):
        return self.pipe_list

    def clear(self):
        self.pipe_list.clear()


# ============ КЛАСС ПОЛА ============
class Floor:
    def __init__(self, config):
        self.config = config
        self.surface = pygame.image.load("assets/base.png")
        self.x_pos = 0

    def update(self):
        self.x_pos -= Config.FLOOR_SPEED
        if self.x_pos <= -200:
            self.x_pos = 0

    def draw(self, screen):
        screen.blit(self.surface, (self.x_pos, Config.SCREEN_HEIGHT - Config.FLOOR_HEIGHT))
        screen.blit(self.surface, (self.x_pos + 200, Config.SCREEN_HEIGHT - Config.FLOOR_HEIGHT))


# ============ КЛАСС ОБНАРУЖЕНИЯ СТОЛКНОВЕНИЙ ============
class CollisionDetector:
    @staticmethod
    def check(bird_rect, pipes):
        # Проверка столкновений с трубами
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return False

        # Проверка границ экрана
        if bird_rect.top <= -100 or bird_rect.bottom >= Config.SCREEN_HEIGHT - Config.FLOOR_HEIGHT:
            return False

        return True


# ============ КЛАСС ПОЛЬЗОВАТЕЛЬСКОГО ИНТЕРФЕЙСА ============
class UI:
    def __init__(self, config):
        self.config = config
        self.game_font = pygame.font.Font("assets/FlappyBirdy.ttf", 40)
        self.background = pygame.image.load("assets/background-night.png")
        self.game_over_surface = pygame.image.load("assets/message.png")
        self.game_over_rect = self.game_over_surface.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))

    def draw_score(self, screen, score, high_score, game_state):
        if game_state == "main_game":
            score_surface = self.game_font.render(str(int(score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.config.SCREEN_WIDTH / 2, 50))
            screen.blit(score_surface, score_rect)

        elif game_state == "game_over":
            score_surface = self.game_font.render(f"Score:{int(score)}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.config.SCREEN_WIDTH / 2, 50))
            screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f"High Score:{int(high_score)}", True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(self.config.SCREEN_WIDTH / 2, 410))
            screen.blit(high_score_surface, high_score_rect)

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_game_over(self, screen):
        screen.blit(self.game_over_surface, self.game_over_rect)


# ============ КЛАСС ИГРОВОГО ДВИЖКА ============
class GameEngine:
    def __init__(self):
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Инициализация компонентов
        self.bird = Bird(self.config)
        self.pipe_manager = PipeManager(self.config)
        self.floor = Floor(self.config)
        self.collision_detector = CollisionDetector()
        self.ui = UI(self.config)

        # Игровое состояние
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.score_sound_countdown = self.config.SCORE_SOUND_INTERVAL

        # Звуки
        self.flap_sound = pygame.mixer.Sound("assets/wing.ogg")
        self.death_sound = pygame.mixer.Sound("assets/hit.ogg")
        self.score_sound = pygame.mixer.Sound("assets/point.ogg")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_active:
                        self.bird.jump()
                        self.flap_sound.play()
                    else:
                        self.reset_game()

            if event.type == self.pipe_manager.SPAWNPIPE and self.game_active:
                self.pipe_manager.spawn_pipe()

            if event.type == self.bird.BIRDFLAP:
                self.bird.animate()

    def update(self):
        if self.game_active:
            # Обновление птицы
            self.bird.update()

            # Обновление труб
            self.pipe_manager.move_pipes()

            # Обновление пола
            self.floor.update()

            # Проверка столкновений
            self.game_active = self.collision_detector.check(
                self.bird.get_rect(),
                self.pipe_manager.get_pipes()
            )

            # Обновление счета
            self.score += 0.01
            self.update_score_sound()

            # Проверка завершения игры
            if not self.game_active:
                self.game_over()

    def update_score_sound(self):
        self.score_sound_countdown -= 1
        if self.score_sound_countdown <= 0:
            self.score_sound.play()
            self.score_sound_countdown = self.config.SCORE_SOUND_INTERVAL

    def game_over(self):
        self.death_sound.play()
        self.high_score = max(self.score, self.high_score)

    def reset_game(self):
        self.game_active = True
        self.pipe_manager.clear()
        self.bird.reset()
        self.score = 0
        self.score_sound_countdown = self.config.SCORE_SOUND_INTERVAL

    def draw(self):
        # Отрисовка фона
        self.ui.draw_background(self.screen)

        if self.game_active:
            # Отрисовка игровых объектов
            self.pipe_manager.draw_pipes(self.screen)
            self.bird.draw(self.screen)
            self.ui.draw_score(self.screen, self.score, self.high_score, "main_game")
        else:
            # Отрисовка экрана завершения игры
            self.ui.draw_game_over(self.screen)
            self.ui.draw_score(self.screen, self.score, self.high_score, "game_over")

        # Отрисовка пола (всегда)
        self.floor.draw(self.screen)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.config.FPS)


# ============ ТОЧКА ВХОДА ============
if __name__ == "__main__":
    pygame.mixer.pre_init()
    pygame.init()

    game = GameEngine()
    game.run()