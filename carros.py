import pygame

# Definir as cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Vehicle:
    def __init__(self):
        self.passed_light = False  # Flag para indicar se o veículo passou pelo semáforo

    def move(self, can_move, vehicle_in_front=None, traffic_light=None):
        # Definimos um ponto de verificação antes do semáforo
        buffer_distance = 150 #40  # Distância antes do semáforo para parar

        # Se o veículo ainda não passou o semáforo, ele respeita o semáforo
        if not self.passed_light and traffic_light and self.direction == traffic_light.direction:
            # Verificar a cor do semáforo se o veículo estiver antes do ponto de verificação
            if traffic_light.color == RED:
                if self.direction == 'North' and self.y <= traffic_light.y + buffer_distance:
                    can_move = False
                elif self.direction == 'South' and self.y + self.height >= traffic_light.y:
                    can_move = False
                elif self.direction == 'East' and self.x + self.width >= traffic_light.x:
                    can_move = False
                elif self.direction == 'West' and self.x <= traffic_light.x + buffer_distance:
                    can_move = False
            else:
                # Se o semáforo está verde e o veículo passa, marcamos como "passou"
                if self.direction == 'North' and self.y < traffic_light.y:
                    self.passed_light = True
                elif self.direction == 'South' and self.y > traffic_light.y + buffer_distance:
                    self.passed_light = True
                elif self.direction == 'East' and self.x > traffic_light.x + buffer_distance:
                    self.passed_light = True
                elif self.direction == 'West' and self.x < traffic_light.x:
                    self.passed_light = True

        # Se o veículo da frente está muito perto, o carro para também
        if vehicle_in_front:
            if self.direction in ['North', 'South']:
                if abs(self.y - vehicle_in_front.y) < self.height + 10:
                    can_move = False
            elif self.direction in ['East', 'West']:
                if abs(self.x - vehicle_in_front.x) < self.width + 10:
                    can_move = False

        # Movimento do veículo
        if can_move:
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
class VehicleNorte(Vehicle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.direction = 'North'
        self.speed = 2
        self.color = (255, 0, 0)  # Cor do veículo

class VehicleSul(Vehicle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.direction = 'South'
        self.speed = 2
        self.color = (0, 255, 0)  # Cor do veículo

class VehicleLeste(Vehicle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.direction = 'East'
        self.speed = 2
        self.color = (0, 0, 255)  # Cor do veículo

class VehicleOeste(Vehicle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.direction = 'West'
        self.speed = 2
        self.color = (255, 255, 0)  # Cor do veículo
