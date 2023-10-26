import pygame , sys 
import config as cfg
from pygame import draw, time,event,display,font
from random import randint
from funciones import *

pygame.init()
font.init()
Speed = cfg.VELOCIDAD 
my_font = pygame.font.SysFont('javanesetext', 24,True)
startFont = pygame.font.SysFont('javanesetext', 28,True)
clock = time.Clock()
width = cfg.WIDTH
height = cfg.HEIGHT
size = (width,height)
ancho=cfg.ANCHO
alto=cfg.ALTO
contadorVidas = 3
contadorScore = cfg.SCORE
pos_y=cfg.POS_Y
pos_x = cfg.POS_X
vidasDificultad = 1

# intervalo de spawn de bloques
enemiesFallingInterval = cfg.TIME_INTERVAL
deathInterval = cfg.DEATH_INTERVAL
shootInterval = cfg.SHOOT_INTERVAL
powerUpFallingIterval = cfg.POWER_UP_INTERVAL
restartPowerInterval = cfg.RESTART_POWERUP

# LLAMO A LOS ASSETS
backgroundImage = pygame.image.load('assets/asfalto.png')
backgroundImage = pygame.transform.rotate(backgroundImage,-90)
powerUpImage = pygame.image.load('./assets/powerUp.png')
# powerUpImage = pygame.transform.rotate(powerUpImage,90)
EnemiesImage0 = pygame.image.load('assets/enemigo0.png')
EnemiesImage0 = pygame.transform.rotate(EnemiesImage0,90)
EnemiesImage1 = pygame.image.load('assets/enemigo1.png')
EnemiesImage1 = pygame.transform.rotate(EnemiesImage1,90)
mainBlockImg = pygame.image.load('assets/autoMain.png')
mainBlockImg = pygame.transform.rotate(mainBlockImg, -90)
bulletImg = pygame.image.load('assets/bullet.png')
dying = pygame.mixer.Sound('assets/dyingsound.mp3')
golpenave = pygame.mixer.Sound('assets/golpenave.mp3')
explosionFinal = pygame.mixer.Sound('assets/explosionFinal.mp3')
explosion = pygame.mixer.Sound('assets/explosion.mp3')
music = pygame.mixer.music.load('assets/8BitMateo.mp3')

# volumen default
pygame.mixer.music.set_volume(0.5)
screen = display.set_mode(size) 
backgroundRect = pygame.Rect(0,0,400,800)
botonPlay = pygame.Rect(250-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)
botonOptions = pygame.Rect(width/2-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)
botonExit = pygame.Rect((width-250)-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)

# flags:
move_up = None
move_down = None
move_left = None
posiciones = True
musicIndex = True
hardcoreMode = False
mute = False
is_running = True
poweredUp = False

# evento personalizado 
# evento personalizado 
deathEvent = pygame.USEREVENT+2
# evento personalizado
deathEvent = pygame.USEREVENT+2
fallingBlock = pygame.USEREVENT+1 
deathEvent = pygame.USEREVENT+2
shootEvent = pygame.USEREVENT+3
powerUpFallingEvent = pygame.USEREVENT+4
restartPowerUp = pygame.USEREVENT+5

# declaro los array de objetos
bloques= []
disparos = []
powerUpList= []
enemiesImages = [EnemiesImage0,EnemiesImage1]

def limpiar():
    bloques.clear()
    disparos.clear()
    mainBlock['rect'].move_ip(pos_x, pos_y)


while True:
    backgroundStartImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundStartImage,backgroundRect)
    mainBlock = crearRecImagen(pos_x,pos_y,cfg.MAINANCHO,cfg.MAINALTO,color=cfg.WHITE,image=mainBlockImg)
    createText(startFont,f'Press Start to start playing.',True,cfg.BLACK,screen,(width/2,200))
    # screen.blit(pressAKey,((width-pressAKey.get_width())/2,100))
    createText(startFont,f'Max Score: {cfg.MAXSCORE}',True,cfg.BLACK,screen,(100,(height-100)))
    createText(startFont,f'Attempts: {cfg.INTENTOS}',True,cfg.BLACK,screen,(width - 100,(height-100)))
    # crearBoton(screen,botonPlay,cfg.GREY,'Play!',cfg.BLACK)
    # crearBoton(screen,botonOptions,cfg.GREY,'Options',cfg.BLACK)
    # crearBoton(screen,botonExit,cfg.GREY,'Exit',cfg.BLACK)
    pygame.display.flip()
    contadorVidas = 3
    contadorScore = 0
    is_running = True
    mute = waitUserClick(botonPlay,botonOptions,botonExit,screen)
    # waitUser()
# volumen default y loop de musica
    pygame.mixer.music.play(-1)
    pygame.time.set_timer(fallingBlock, enemiesFallingInterval)
    pygame.time.set_timer(powerUpFallingEvent, powerUpFallingIterval)
    while is_running:
        
        clock.tick(cfg.FPS)
# DETECTO EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Creo un disparo
                    disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
            if event.type == deathEvent:
                dying.play()
                limpiar()
                is_running = False
            if event.type == shootEvent:
                # Creo un disparo
                disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
            if event.type == restartPowerUp:
                shootInterval = 400
                mainBlock['speed-y'] = randint(2,3)
                poweredUp = False
            if event.type == powerUpFallingEvent:
                # Duplico la velocidad de disparo
                powerUpList.append(crearRecImagen(left=width+ancho,top=randint(50,450),ancho=60,alto=45,image=powerUpImage,vidas=1))
            if event.type == fallingBlock:
                i = randint(0,1)
                if i==0:
                    bloques.append(crearRecImagen(left=width+ancho,ancho=ancho,alto=alto,top=randint(50,450),image=enemiesImages[i],vidas=1))
                else:
                    bloques.append(crearRecImagen(left=width+ancho,ancho=ancho,alto=alto,top=randint(50,450),image=enemiesImages[i],vidas=3))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    limpiar()
                    is_running = False
                if event.key == pygame.K_SPACE:
                    disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_down = False
                    move_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_up = False
                    move_down = True
                if event.key == pygame.K_h:
                    hardcoreMode = not hardcoreMode
                if event.key == pygame.K_m:
                    mute = not mute
                if event.key == pygame.K_k:
                    if musicIndex:
                        music =  pygame.mixer.music.load('./assets/8Bit.mp3')
                        pygame.mixer.music.play(-1)
                        musicIndex = not musicIndex
                    else:
                        music =  pygame.mixer.music.load('./assets/8BitMateo.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        musicIndex = not musicIndex
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False
        # cargo los eventos de mousepressed
        mousepressed = pygame.mouse.get_pressed()

# ACTUALIZO ELEMENTOS

        # Mute
        # if pygame.mixer.music.get_volume() == 0 or pygame.mixer.music.get_volume() == False:
        #     mute == True
        
        if mute == True:
            pygame.mixer.music.set_volume(False)
        else:
            pygame.mixer.music.set_volume(0.5)
# Blit De Textos, background y main block
        # Creo los render y el bliteo por sepearado para poder tener la posibilidad
        # de centrar utilizando el tamano de los textos y hacerlo lo mas reactivo posible
        backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
        screen.blit(backgroundImage,backgroundRect)
        screen.blit(mainBlock['image'],mainBlock['rect'])
        createText(my_font,f'Score: {contadorScore}',True,cfg.BLACK,screen,(200,50))
        createText(my_font,f'Lives: {contadorVidas}',True,cfg.BLACK,screen,((width-200),50))
        # si esta en ejecucion el juego hago el blit de los bloques principales
        if is_running:
            for disparo in disparos:
                screen.blit(disparo['image'],disparo['rect'])
            for bloque in bloques:
                screen.blit(bloque['image'],bloque['rect'])
            for powerUp in powerUpList:
                screen.blit(powerUp['image'],powerUp['rect'])
        # PREGUNTAR PORQUE EL COMPORTAMIENTO DE CUANDO ESTA EN FALSE LO TOMA COMO TRUE Y VICEVERSA, ACA DEBERIA IR UN TRUE PERO LO CONSIDERA UN FALSE Y NO DISPARA. SE QUEDA DISPARANDO CUANDO SOLTAS ES CLICK SI ESTA EN TRUE.
        # Y PORQUE EL COMPORTAMIENTO DE CUANDO PONGO LA BARRA ESPACIADORA TAMBIEN SOLO FUNCIONA CUANDO AMBAS CONDICIONES ESTAN
        # Lo vamos a ver en clase
        if  mousepressed[0] == False : 
            pygame.time.set_timer(shootEvent, shootInterval)
            
# MOVER ELEMENTOS

        # MUEVO LOS ALIENS CAYENDO Y LOS DISPAROS
        for disparo in disparos[:]:
            rectDisparo=disparo['rect']
            rectDisparo.move_ip(Speed*2,0)
            if rectDisparo.right  < 0:
                disparos = borrarItemLista(disparos,disparo)
        for powerUp in powerUpList[:]:
            rectPower = powerUp['rect']
            rectPower.move_ip(-powerUp['speed-x']*0.5,0)
            if rectPower.right< 0:
                if powerUp:
                    powerUpList = borrarItemLista(powerUpList,powerUp)
            if detectar_colision_circ(rectPower,mainBlock['rect']):
                if poweredUp == False:
                    shootInterval = 150
                    mainBlock['speed-y'] = 5
                    poweredUp = True
                    pygame.time.set_timer(restartPowerUp,cfg.RESTART_POWERUP,1)
                powerUpList = borrarItemLista(powerUpList,powerUp)
        # Detecto las colisiones con los disparos para penalizar al usuario cuando dispara a un power up
            for disparo in disparos[:]:
                if detectar_colision_circ(rectPower,disparo['rect']):
                    if powerUp['vidas'] <= 1:
                        powerUpList = borrarItemLista(powerUpList,powerUp)
                    else:
                        powerUp['vidas'] -= 1
                    disparos = borrarItemLista(disparos,disparo)
        # Crear un sonido de muerte de powerUp a mano como los otros.
                    explosion.play()

        for bloque in bloques[:]:
            rect=bloque['rect']
            rect.move_ip(-bloque['speed-y'],0)
        # AUMENTO LA DIFICULTAD CON HARDCORE MODE O CON PUNTOS A 30 PARA QUE EMPIEZEN A MOVERSE LOS OBJETOS
            if contadorScore > 30 or hardcoreMode == True:
                if posiciones == True : 
                    if rect.y > 0 :
                        rect.move_ip(-bloque['speed-x'],-bloque['speed-y'])
                    else:
                        posiciones = False
                else:
                    if rect.y < height - rect.height:
                        rect.move_ip(-bloque['speed-x'],+bloque['speed-y'])
                    else:
                        posiciones = True
# DETECTO COLISIONES

        # Final de pantalla borro bloque para liberar memoria le sumo 5 para que se vea mas prolijo y aseguro
        # Tengo que validar que el bloque exista antes de borrarlo porque puede haber sido borrado por alguna colision (la prioridad la tienen los disparos)
            if rect.right < 0:
                bloques = borrarItemLista(bloques,bloque) 
        # Chequeo la colision con el tiro y los aliens
            for disparo in disparos[:]:
                if detectar_colision_circ(rect,disparo['rect']):
                    if bloque['vidas'] <= 1: 
                        bloques = borrarItemLista(bloques,bloque) 
                        contadorScore +=1
                    else:
                        bloque['vidas'] -= 1
        # Sector dificultad
                    if contadorScore >= 50:
                        vidasDificultad = 2
                    elif contadorScore >= 100:
                        vidasDificultad = 3
                    disparos = borrarItemLista(disparos,disparo)
                    explosion.play()
        # Detecto las colisiones con el mainbody
            if detectar_colision_circ(rect,mainBlock['rect']):
                if contadorVidas == 1 :
                    limpiar()
                    explosionFinal.play()
                    if cfg.MAXSCORE < contadorScore:
                        cfg.MAXSCORE = contadorScore
                        cfg.INTENTOS = 0
                    else:
                        cfg.INTENTOS += 1
                    pygame.time.set_timer(deathEvent,100,1)
                else:
                    contadorVidas -= 1
                    golpenave.play()
                    bloques = borrarItemLista(bloques,bloque) 
# MUEVO EL MAIN BLOCK
        if move_down and mainBlock['rect'].bottom < height:
            mainBlock['rect'].move_ip(0,+mainBlock['speed-y'])
        if move_up and mainBlock['rect'].top > 0 + 5 :
            mainBlock['rect'].move_ip(0,-mainBlock['speed-y'])
            
# ACTUALIZO PANTALLA
        pygame.display.flip()
# AFUERA DEL IS_RUNNING
    backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundImage,backgroundRect)
    createText(startFont,f'Game Over !',True,cfg.BLACK,screen,(width/2,(height - 100)/2))
    # screen.blit(gameOver,((width -gameOver.get_width()) /2,(height - 100)/2))
    createText(startFont,f'Press any key to continue',True,cfg.BLACK,screen,(width/2,(height - 50)/1.7))
    # screen.blit(keyToContinue,((width - keyToContinue.get_width())/2,(height - 50)/1.7))
    pygame.mixer.music.stop()
    pygame.display.flip()
    waitUser()