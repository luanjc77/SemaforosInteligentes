import pygame

# Definir as cores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)

class TrafficLight:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = RED
        self.wait_time = 0  # Tempo que a faixa está esperando para abrir
        self.vehicle_count = 0  # Quantidade de veículos na faixa

    def open_light(self):
        self.color = GREEN
        self.wait_time = 0  # Resetar o tempo de espera quando abre

    def close_light(self):
        self.color = RED

    def set_yellow(self):
        self.color = YELLOW

    def draw(self, screen):
        if self.direction in ['North', 'South']:
            pygame.draw.rect(screen, DARK_GRAY, [self.x, self.y, 60, 20])
            if self.color == RED:
                pygame.draw.circle(screen, RED, (self.x + 10, self.y + 10), 8)
            elif self.color == GREEN:
                pygame.draw.circle(screen, GREEN, (self.x + 50, self.y + 10), 8)
            elif self.color == YELLOW:
                pygame.draw.circle(screen, YELLOW, (self.x + 30, self.y + 10), 8)
        else:
            pygame.draw.rect(screen, DARK_GRAY, [self.x, self.y, 20, 60])
            if self.color == RED:
                pygame.draw.circle(screen, RED, (self.x + 10, self.y + 10), 8)
            elif self.color == GREEN:
                pygame.draw.circle(screen, GREEN, (self.x + 10, self.y + 50), 8)
            elif self.color == YELLOW:
                pygame.draw.circle(screen, YELLOW, (self.x + 10, self.y + 30), 8)

class TrafficControlSystem:
    def __init__(self, lights):
        self.lights = lights
        self.green_duration = 120  # Duração do semáforo verde (em frames)
        self.yellow_duration = 30  # Duração do semáforo amarelo
        self.timer = 0
        self.state = 'green'
        self.max_wait_time = 200  # Tempo máximo de espera antes de priorizar uma faixa

    def update(self):
        for light in self.lights:
            if light.color == RED:
                light.wait_time += 1

        max_vehicles = max(self.lights, key=lambda l: l.vehicle_count)
        max_waiting = max(self.lights, key=lambda l: l.wait_time)
        
        if max_vehicles.vehicle_count >= 3 or max_waiting.wait_time >= self.max_wait_time:
            priority_light = max_vehicles if max_vehicles.vehicle_count >= 3 else max_waiting
        else:
            priority_light = max_waiting

        self.timer += 1

        if self.state == 'green':
            if self.timer >= self.green_duration or priority_light.wait_time > self.max_wait_time:
                for light in self.lights:
                    if light.color == GREEN:
                        light.set_yellow()
                self.state = 'yellow'
                self.timer = 0
        elif self.state == 'yellow':
            if self.timer >= self.yellow_duration:
                for light in self.lights:
                    light.close_light()
                priority_light.open_light()
                self.state = 'green'
                self.timer = 0

    def get_current_green_direction(self):
        for light in self.lights:
            if light.color == GREEN:
                return light.direction
        return None

    def draw(self, screen):
        for light in self.lights:
            light.draw(screen)
