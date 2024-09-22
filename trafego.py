import pygame
import random
from carros import VehicleNorte, VehicleSul, VehicleLeste, VehicleOeste
from semaforo import TrafficControlSystem, TrafficLight

# Inicialização do pygame
pygame.init()

# Definir as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

# Dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Função para desenhar as ruas
def draw_roads():
    screen.fill(GRAY)

    # Ruas horizontais
    pygame.draw.rect(screen, BLACK, [0, 250, SCREEN_WIDTH, 100])
    pygame.draw.rect(screen, BLACK, [250, 0, 100, SCREEN_HEIGHT])

    # Linhas amarelas
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(screen, YELLOW, (x, 300), (x + 20, 300), 5)
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(screen, YELLOW, (300, y), (300, y + 20), 5)

def main():
    running = True
    clock = pygame.time.Clock()

    traffic_lights = [
        TrafficLight(250, 360, 'North'),
        TrafficLight(250, 230, 'South'),
        TrafficLight(370, 290, 'West'),
        TrafficLight(210, 290, 'East')
    ]

    control_system = TrafficControlSystem(traffic_lights)

    vehicles = {
        'North': [],
        'South': [],
        'East': [],
        'West': []
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_roads()

        control_system.update()
        control_system.draw(screen)

        # Gerar veículos e priorizar fila
        if random.random() < 0.05:
            direction = control_system.get_current_green_direction()
            if direction == 'North':
                vehicles['North'].append(VehicleNorte(265, 600))
            elif direction == 'South':
                vehicles['South'].append(VehicleSul(320, 0))
            elif direction == 'East':
                vehicles['East'].append(VehicleLeste(0, 310))
            elif direction == 'West':
                vehicles['West'].append(VehicleOeste(600, 255))

        # Atualizar os veículos
                # Atualizar os veículos
        for direction, vehicle_list in vehicles.items():
            for vehicle in vehicle_list[:]:
                can_move = vehicle.direction == control_system.get_current_green_direction()
                
                # Passa o semáforo correspondente para contar veículos
                relevant_traffic_light = next(light for light in traffic_lights if light.direction == vehicle.direction)
                vehicle.move(can_move, traffic_light=relevant_traffic_light)
                vehicle.draw(screen)

                if vehicle.has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    vehicle_list.remove(vehicle)
                    relevant_traffic_light.vehicle_count -= 1  # Reduzir o contador quando o veículo sair


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()