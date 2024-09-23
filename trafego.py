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
    pygame.draw.rect(screen, BLACK, [250, 0, 100, 600])
    pygame.draw.rect(screen, BLACK, [0, 250, 600, 100])

def main():
    clock = pygame.time.Clock()

    # Criar os semáforos
    traffic_lights = [
        TrafficLight(250, 250, 'North'),
        TrafficLight(250, 330, 'South'),
        TrafficLight(330, 250, 'East'),
        TrafficLight(250, 250, 'West')
    ]

    # Sistema de controle de tráfego
    traffic_control = TrafficControlSystem(traffic_lights)

    vehicles_norte = []
    vehicles_sul = []
    vehicles_leste = []
    vehicles_oeste = []

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Desenhar as ruas e semáforos
        draw_roads()
        traffic_control.draw(screen)

        # Atualizar o sistema de controle de tráfego
        traffic_control.update()

        # Gerar veículos para cada direção
        if len(vehicles_norte) < 5 and (len(vehicles_norte) == 0 or vehicles_norte[-1].has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT)):
            vehicles_norte.append(VehicleNorte(280, 600))
        if len(vehicles_sul) < 5 and (len(vehicles_sul) == 0 or vehicles_sul[-1].has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT)):
            vehicles_sul.append(VehicleSul(320, -40))
        if len(vehicles_leste) < 5 and (len(vehicles_leste) == 0 or vehicles_leste[-1].has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT)):
            vehicles_leste.append(VehicleLeste(-40, 280))
        if len(vehicles_oeste) < 5 and (len(vehicles_oeste) == 0 or vehicles_oeste[-1].has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT)):
            vehicles_oeste.append(VehicleOeste(600, 320))

        # Mover e desenhar veículos
        for vehicle_list in [vehicles_norte, vehicles_sul, vehicles_leste, vehicles_oeste]:
            for i, vehicle in enumerate(vehicle_list):
                relevant_traffic_light = None
                if vehicle.direction == 'North':
                    relevant_traffic_light = traffic_lights[0]
                elif vehicle.direction == 'South':
                    relevant_traffic_light = traffic_lights[1]
                elif vehicle.direction == 'East':
                    relevant_traffic_light = traffic_lights[2]
                elif vehicle.direction == 'West':
                    relevant_traffic_light = traffic_lights[3]

                can_move = True
                vehicle_in_front = vehicle_list[i - 1] if i > 0 else None
                vehicle.move(can_move, vehicle_in_front=vehicle_in_front, traffic_light=relevant_traffic_light)
                vehicle.draw(screen)

            # Remover veículos que saíram da tela
            vehicle_list[:] = [v for v in vehicle_list if not v.has_left_screen(SCREEN_WIDTH, SCREEN_HEIGHT)]

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
