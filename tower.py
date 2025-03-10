import pygame
from bullet import Bullet
import math
import time


class Tower(pygame.sprite.Sprite):
    '''
        Базовый класс для всех башен в игре.
    Атрибуты:
        position (Vector2): Позиция башни.
        game (Game): Ссылка на объект игры.
        image (Surface): Изображение башни.
        rect (Rect): Прямоугольник, ограничивающий область башни.
        tower_range (float): Радиус действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Время между выстрелами в миллисекундах.
        last_shot_time (int): Время последнего выстрела.
        level (int): Уровень башни.
        original_image (Surface): Исходное изображение башни.
    '''
    def __init__(self, position, game):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image

    def upgrade_cost(self):
        '''Возвращает стоимость апгрейда башни.'''
        return 100 * self.level

    def draw(self, screen):
        '''Отрисовывает информацию о башне на экране.'''
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        '''Обновляет состояние башни, проверяет цели и производит выстрелы.'''
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        '''Проверяет, наведена ли мышь на башню.'''
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        '''Метод для реализации стрельбы (реализуется в подклассах).'''
        pass

    def rotate_towards_target(self, target):
        '''Поворачивает башню в сторону цели.'''
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        '''Находит ближайшую цель среди врагов.'''
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        '''Увеличивает уровень башни на 1.'''
        self.level += 1


class BasicTower(Tower):
    '''    Класс, представляющий базовую башню.

    Наследуется от класса Tower.

    Атрибуты:
        image (Surface): Изображение базовой башни.
        original_image (Surface): Исходное изображение базовой башни.
        tower_range (float): Радиус действия базовой башни (150).
        damage (int): Урон, наносимый базовой башней (20).
        rate_of_fire (int): Время между выстрелами (1000 мс).'''
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        '''Создает пулю и добавляет ее в группу.'''
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    '''    Класс, представляющий снайперскую башню.

    Наследуется от класса Tower.

    Атрибуты:
        image (Surface): Изображение снайперской башни.
        original_image (Surface): Исходное изображение снайперской башни.
        tower_range (float): Радиус действия снайперской башни (300).
        damage (int): Урон, наносимый снайперской башней (40).
        rate_of_fire (int): Время между выстрелами (2000 мс).'''
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        '''Находит врага с наибольшим здоровьем в пределах радиуса действия.'''
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        '''Создает пулю и добавляет ее в группу.'''
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)

class MoneyTower(Tower):
    '''
    Башня, генерирующая деньги для игрока.

    Наследуется от класса Tower.

    Атрибуты:
        image (Surface): Изображение башни.
        original_image (Surface): Исходное изображение башни.
        money_per_tick (int): Сумма денег, добавляемая за один цикл.
        money_rate (int): Время между генерацией денег (в миллисекундах).
    '''
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)

        self.money_per_tick = 10  # Сумма денег за цикл
        self.money_rate = 5000  # Время между циклами (в миллисекундах)
        self.last_money_time = pygame.time.get_ticks()

    def update(self, enemies, current_time, bullets_group):
        '''Генерирует деньги, если прошло достаточно времени.'''
        if current_time - self.last_money_time >= self.money_rate:
            self.game.settings.starting_money += self.money_per_tick
            self.last_money_time = current_time

    def upgrade(self):
        '''Улучшает башню, увеличивая сумму денег за цикл.'''
        super().upgrade()
        self.money_per_tick += 5
        self.money_rate = max(1000, self.money_rate - 500)  # Уменьшаем интервал до минимального значения

    def draw(self, screen):
        super().draw(screen)
        income_text = self.game.font.render(f"+${self.money_per_tick}/cycle", True, (255, 255, 0))
        screen.blit(income_text, (self.rect.x, self.rect.y - 40))

