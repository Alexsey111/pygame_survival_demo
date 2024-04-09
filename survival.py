import pygame
import random

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для музыки

# Загрузка музыки
pygame.mixer.music.load('b.mp3')
pygame.mixer.music.play(-1)  # -1 для зацикливания музыки
music_on = True  # Состояние музыки (включена или выключена)

# Настройки окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Выживание')

# Загрузка изображений
player_img = pygame.image.load('bear.png')
enemy_img = pygame.image.load('bee.png')
background_img = pygame.image.load('meadow.jpeg')

# Параметры главного персонажа
player_size = 50
player_pos = [window_size[0] // 2, window_size[1] - 2 * player_size]

# Параметры врагов
enemy_size = 50
enemy_pos = [random.randint(0, window_size[0] - enemy_size), 0]
enemy_speed = 17

# Счетчики
deaths = 0
best_time = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

collision_occurred = False
game_over = False


def create_enemy():
    return [random.randint(0, window_size[0] - enemy_size), 0]


def detect_collision(player_pos, enemy_pos, size):
    px, py = player_pos
    ex, ey = enemy_pos

    if (ex >= px and ex < (px + size)) or (px >= ex and px < (ex + size)):
        if (ey >= py and ey < (py + size)) or (py >= ey and py < (ey + size)):
            return True
    return False


def display_info():
    screen.blit(background_img, (0, 0))

    info_text = font.render("Управление: Стрелки влево/вправо - движение", True, (0, 0, 0))
    music_text = font.render("M - вкл./выкл. музыку", True, (0, 0, 0))

    screen.blit(info_text, (window_size[0] // 2 - info_text.get_width() // 2, window_size[1] // 2 - 30))
    screen.blit(music_text, (window_size[0] // 2 - music_text.get_width() // 2, window_size[1] // 2 + 30))

    pygame.display.flip()
    pygame.time.delay(7000)  # Отображение информации на 7 секунд


def display_game_over():
    screen.blit(background_img, (0, 0))

    game_over_text = font.render(f"Игра окончена! Смерти: {deaths}, Лучшее время: {best_time // 1000} сек", True,
                                 (0, 0, 0))
    text_rect = game_over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(game_over_text, text_rect)

    pygame.display.flip()
    pygame.time.delay(5000)  # Отображение информации на 5 секунд


display_info()

run = True
session_start_time = pygame.time.get_ticks()

while run:
    current_time = pygame.time.get_ticks() - session_start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Включение/выключение музыки при нажатии клавиши "M"
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player_pos[0] < window_size[0] - player_size:
        player_pos[0] += 5

    enemy_pos[1] += enemy_speed
    if enemy_pos[1] > window_size[1]:
        enemy_pos = create_enemy()

    if detect_collision(player_pos, enemy_pos, player_size):
        if not collision_occurred:
            deaths += 1
            collision_occurred = True

            if current_time > best_time:
                best_time = current_time

            session_start_time = pygame.time.get_ticks()
    else:
        collision_occurred = False

    screen.blit(background_img, (0, 0))
    screen.blit(enemy_img, (enemy_pos[0], enemy_pos[1]))
    screen.blit(player_img, (player_pos[0], player_pos[1]))

    elapsed_time = current_time // 1000
    text = font.render(f"Смерти: {deaths}  Текущее время: {elapsed_time} сек  Лучшее время: {best_time // 1000} сек",
                       True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()  # Остановка музыки при выходе из игры

display_game_over()

pygame.quit()

