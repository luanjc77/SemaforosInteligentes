import pygame

# Definir as cores
WHITE = (255, 255, 255)  # Pode ser removido se não for mais utilizado
RED = (255, 0, 0)

class Vehicle:
    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        # Se o veículo está perto do semáforo, ele para
        if traffic_light and self.direction == traffic_light.direction and traffic_light.color == RED:
            can_move = False
            traffic_light.vehicle_count += 1  # Incrementar o contador de veículos

        # Se o veículo da frente está parado, pare também
        if vehicle_in_front:
            if self.direction in ['North', 'South']:
                if abs(self.y - vehicle_in_front.y) < self.height + 10:
                    can_move = False
            elif self.direction in ['East', 'West']:
                if abs(self.x - vehicle_in_front.x) < self.width + 10:
                    can_move = False

        # Movimento do veículo
        if can_move and not self.stopped:
            if self.direction == 'North':
                self.y -= self.speed
            elif self.direction == 'South':
                self.y += self.speed
            elif self.direction == 'East':
                self.x += self.speed
            elif self.direction == 'West':
                self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def has_left_screen(self, screen_width, screen_height):
        if self.direction == 'North':
            return self.y + self.height < 0
        elif self.direction == 'South':
            return self.y > screen_height
        elif self.direction == 'East':
            return self.x > screen_width
        elif self.direction == 'West':
            return self.x + self.width < 0


# Subclasses específicas para cada direção
class VehicleNorte:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.direction = 'North'
        self.speed = 2

    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        if can_move:
            self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def has_left_screen(self, screen_width, screen_height):
        # Verifica se o veículo saiu da tela (no caso do Norte, saiu por cima)
        return self.y + self.height < 0

class VehicleSul:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.direction = 'South'
        self.speed = 2

    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        if can_move:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def has_left_screen(self, screen_width, screen_height):
        # Verifica se o veículo saiu da tela (no caso do Sul, saiu por baixo)
        return self.y > screen_height

class VehicleLeste:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.direction = 'East'
        self.speed = 2

    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        if can_move:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def has_left_screen(self, screen_width, screen_height):
        # Verifica se o veículo saiu da tela (no caso do Leste, saiu pela direita)
        return self.x > screen_width

class VehicleOeste:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.direction = 'West'
        self.speed = 2

    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        if can_move:
            self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))

    def has_left_screen(self, screen_width, screen_height):
        # Verifica se o veículo saiu da tela (no caso do Oeste, saiu pela esquerda)
        return self.x + self.width < 0
