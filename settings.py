class Settings:
    '''
     Класс, представляющий настройки игры.

    Атрибуты:
        screen_width (int): Ширина экрана.
        screen_height (int): Высота экрана.
        bg_color (tuple): Цвет фона в формате RGB.
        rows (int): Количество строк в сетке.
        cols (int): Количество столбцов в сетке.
        grid_size (tuple): Размер ячеек сетки (ширина, высота).
        tower_cost (int): Стоимость размещения башни.
        tower_upgrade_cost (int): Стоимость апгрейда башни.
        tower_sell_percentage (float): Процент возврата от продажи башни.
        enemy_path (list): Путь, по которому будут двигаться враги.
        tower_sprites (dict): Словарь, содержащий пути к изображению башен.
        enemy_sprite (str): Путь к изображению врага.
        bullet_sprite (str): Путь к изображению снаряда.
        background_image (str): Путь к изображению фона игры.
        shoot_sound (str): Путь к звуковому файлу выстрела.
        upgrade_sound (str): Путь к звуковому файлу апгрейда.
        sell_sound (str): Путь к звуковому файлу продажи башни.
        enemy_hit_sound (str): Путь к звуковому файлу попадания по врагу.
        background_music (str): Путь к звуковому файлу фоновой музыки.
        starting_money (int): Начальное количество денег игрока.
        lives (int): Количество жизней игрока.
        tower_positions (list): Список доступных позиций для размещения башен.
    '''
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Сетка
        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_path = [
            (50, 400), (300, 400), (300, 200), (600, 200),
            (600, 600), (900, 600), (900, 300), (1150, 300)
        ]

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/game_background.png'

        self.shoot_sound = 'assets/sounds/shoot.wav'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.background_music = 'assets/sounds/background_music.mp3'
        self.enemy_spawn = 'assets/sounds/enemy_spawn.wav'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [(x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
                                for x in range(1, self.cols) for y in range(3, self.rows)]
