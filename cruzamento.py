import pygame
import random
import time
import threading
import sys

# Coordenadas de imagem de sinal, temporizador e contagem de veículos
signalCoods = [(570,300),(770,230),(770,470),(570,540)]

# Valores padrões para timer
defaultGreen = {0:10, 1:10, 2:10, 3:10}
defaultRed = 150
defaultYellow = 5

signals = []
noOfSignals = 4
currentGreen = 0   
nextGreen = (currentGreen+1)%noOfSignals   
currentYellow = 0  

# Coordenadas de partida dos veículos
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

# Cordenadas da parada dos veículos
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

#Veículos (tipos e direções)
vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bike'}
speeds = {'car':2.25, 'bike':2.5}  
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}


stoppingGap = 15    # gap de parada
movingGap = 15   # gap de movimento

pygame.init()
pygame.font.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.closedTime = 0  

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"#busca a imagem do veículo
        self.image = pygame.image.load(path)

        #Verifica a parada dos veículos e impete que todos parem no mesmo ponto
        if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):    
            if(direction=='right'):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().width - stoppingGap         
            elif(direction=='left'):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().width + stoppingGap
            elif(direction=='down'):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().height - stoppingGap
            elif(direction=='up'):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]
            
        # seta novo start de inicio e parada
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):   # se a imagem for passada para o veiculo
                self.crossed = 1
            if((self.x+self.image.get_rect().width<=self.stop or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                
            # (se a imagem não atingiu sua coordenada de parada ou cruzou a linha de parada ou tem sinal verde) e (é o primeiro veículo naquela faixa ou tem espaço suficiente para o próximo veículo naquela faixa)
                self.x += self.speed  # move o veiculo
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                
                self.y += self.speed
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
            if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):                
                self.x -= self.speed   
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
            if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                
                self.y -= self.speed

# Inicializa os semáforos com valores padrão
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()

def repeat():
    global currentGreen, currentYellow, nextGreen
    while signals[currentGreen].green > 0:  # enquanto o temporizador do sinal verde atual não for zero
        updateValues()
        time.sleep(1)

    currentYellow = 1  # ativar o sinal amarelo

    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    while signals[currentGreen].yellow > 0:  # enquanto o temporizador do sinal amarelo atual não for zero
        updateValues()
        time.sleep(1)

    currentYellow = 0  # seta amarelo zerado

    # resetar todos os tempos dos sinais atuais para os tempos padrões
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    # Lógica para determinar o próximo semáforo a ser ativado com base em stoppedVehiclesCount e closedTime
    stoppedVehiclesCount = {'right': 0, 'down': 0, 'left': 0, 'up': 0}
    closedTimeCount = {'right': 0, 'down': 0, 'left': 0, 'up': 0}

    for vehicle in simulation:
        if isVehicleStopped(vehicle):  # Verifica se o veículo está parado
            stoppedVehiclesCount[vehicle.direction] += 1

    for i in range(noOfSignals):
        direction = directionNumbers[i]
        closedTimeCount[direction] = signals[i].closedTime

    # Encontra a direção com o maior número de veículos parados e mais tempo fechado
    nextGreen = max(stoppedVehiclesCount, key=lambda k: (stoppedVehiclesCount[k], closedTimeCount[k]))

    # Mapeamento de direções para índices
    directionToIndex = {'right': 0, 'down': 1, 'left': 2, 'up': 3}
    nextGreen_index = directionToIndex[nextGreen]  # Converte a direção para índice do semáforo

    # Defina o tempo do vermelho do próximo sinal
    signals[nextGreen_index].red = signals[currentGreen].yellow + signals[currentGreen].green  

    currentGreen = nextGreen_index  # Define o próximo sinal como o sinal verde
    repeat()


# Atualizar os valores dos temporizadores dos sinais a cada segundo
def updateValues():
    global currentGreen
    for i in range(0, noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1
            signals[i].closedTime += 1  # Incrementar o tempo que o sinal ficou fechado


# Gerar veículos na simulação
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0, 1)
        lane_number = random.randint(1, 2)
        temp = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if(temp < dist[0]):
            direction_number = 0
        elif(temp < dist[1]):
            direction_number = 1
        elif(temp < dist[2]):
            direction_number = 2
        elif(temp < dist[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)

def isVehicleStopped(vehicle):
    if vehicle.direction == 'right':
        return vehicle.x + vehicle.image.get_rect().width <= stopLines[vehicle.direction] and vehicle.crossed == 0
    elif vehicle.direction == 'down':
        return vehicle.y + vehicle.image.get_rect().height <= stopLines[vehicle.direction] and vehicle.crossed == 0
    elif vehicle.direction == 'left':
        return vehicle.x >= stopLines[vehicle.direction] and vehicle.crossed == 0
    elif vehicle.direction == 'up':
        return vehicle.y >= stopLines[vehicle.direction] and vehicle.crossed == 0
    return False



class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())    # inicialização
    thread1.daemon = True
    thread1.start()

    # Cores
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Tamanho da tela
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Definindo imagem de fundo, ou seja, imagem do cruzamento
    background = pygame.image.load('images/cruzamento.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Cruzamento")

    # Carregando imagens dos sinais e fonte
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())    # Gerando veículos
    thread2.daemon = True
    thread2.start()

    while True:
        vehicleCountCoods = [(560, 310), (800, 180), (810, 535), (570, 655)]
        stoppedVehiclesCount = {'right': 0, 'down': 0, 'left': 0, 'up': 0}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))  # exibir fundo na simulação

        # Atualizar a contagem de veículos parados antes de exibir na tela
        for vehicle in simulation:
            if isVehicleStopped(vehicle):  # Verifica se o veículo está parado
                stoppedVehiclesCount[vehicle.direction] += 1
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()  # Move o veículo após atualizar sua contagem

        # Exibir sinais e definir o temporizador de acordo com o status atual: verde, amarelo ou vermelho
        for i in range(0, noOfSignals):
            if(i == currentGreen):
                if(currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red <= 10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])

        signalTexts = ["", "", "", ""]

        # Exibir a contagem de veículos parados ao lado de cada semáforo
        for i, direction in enumerate(['right', 'down', 'left', 'up']):
            countText = font.render(str(stoppedVehiclesCount[direction]), True, white, black)
            screen.blit(countText, vehicleCountCoods[i])

        pygame.display.update()

       
Main()