
try:
    from creating import *
    from handlersUser import *
    from colisiones import *
    import config as cfg
    import json
    from pygame import draw, time,event,display,font
    from random import randint
except ImportError as Err:
    errMsg("Error found while importing modules essentials for the game to function")
    print(Err)
    errMsg('Please validate the install and try again. This files are crutial for the game to run.')
    exit()

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
liveCounter = 3
scoreCounter = cfg.SCORE
pos_y=cfg.POS_Y
pos_x = cfg.POS_X
livesIncremental = 1
maxScoreFileData = 0
attemptsFileData = 0

# interevals from config file
enemiesFallingInterval = cfg.TIME_INTERVAL
deathInterval = cfg.DEATH_INTERVAL
shootInterval = cfg.SHOOT_INTERVAL
powerUpFallingIterval = cfg.POWER_UP_INTERVAL
restartPowerInterval = cfg.RESTART_POWERUP

# loading assets
try:
    backgroundImage = pygame.image.load('assets/asfalto.png')
    powerUpImage = pygame.image.load('assets/powerUp.png')
    EnemiesImage0 = pygame.image.load('assets/enemigo0.png')
    EnemiesImage1 = pygame.image.load('assets/enemigo1.png')
    mainBlockImg = pygame.image.load('assets/autoMain.png')
    bulletImg = pygame.image.load('assets/bullet.png')
    music = pygame.mixer.music.load('assets/8BitMateo.mp3')

except FileNotFoundError:
    errMsg('Error when attempting to load main assets. Recomended to verify integrity of the files or do a re-install')
    errMsg('Game cannot run, closing...')
    exit()


# Rotation of the images to fit screen
backgroundImage = pygame.transform.rotate(backgroundImage,-90)
EnemiesImage0 = pygame.transform.rotate(EnemiesImage0,90)
EnemiesImage1 = pygame.transform.rotate(EnemiesImage1,90)
mainBlockImg = pygame.transform.rotate(mainBlockImg, -90)
# mixer setup of the sounds
dying = pygame.mixer.Sound('assets/dyingsound.mp3')
hitSpaceShip = pygame.mixer.Sound('assets/golpenave.mp3')
finalExplosion = pygame.mixer.Sound('assets/explosionFinal.mp3')
explosion = pygame.mixer.Sound('assets/explosion.mp3')
powerUpSound = pygame.mixer.Sound('assets/powerUpsound.mp3')


# volumen default

pygame.mixer.music.set_volume(0.5)
# set rectangules and screen
try:
    screen = display.set_mode(size)
    
except pygame.error as Err:
    errMsg(Err)
    exit()
display.set_caption('StreetShoot')
backgroundRect = pygame.Rect(0,0,400,800)
buttonPlay = pygame.Rect(250-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)
buttonOptions = pygame.Rect(width/2-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)
buttonExit = pygame.Rect((width-250)-(cfg.BUTTON_WIDTH//2),height//1.95,cfg.BUTTON_WIDTH,cfg.BUTTON_HEIGHT)

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
cheatOn = False
menuState = 'main'

# evento personalizado
deathEvent = pygame.USEREVENT+2
fallingBlock = pygame.USEREVENT+1 
shootEvent = pygame.USEREVENT+3
powerUpFallingEvent = pygame.USEREVENT+4
restartPowerUp = pygame.USEREVENT+5

# declaro los array de objetos
blockList = []
shotsList = []
powerUpList= []
enemiesImages = [EnemiesImage0,EnemiesImage1]

def limpiar():
    blockList.clear()
    shotsList.clear()
    mainBlock['rect'].move_ip(pos_x, pos_y)


while True:
    try:
        with open('./db.json') as db:
            data = json.load(db)
        maxScoreFileData = data[0]['value']
        attemptsFileData = data[1]['value']
    except FileNotFoundError as Err:
        data = createDefaultDb()
        with open('./db.json','w') as file:
            json.dump(data,file,indent=2)
        errMsg("Error while trying to read data for the scores")
        print(Err)
        errMsg('Please validate the install and try again. The game can run without it but the db has been reseted to default (0)')
        maxScoreFileData = data[0]['value']
        attemptsFileData = data[1]['value']

    backgroundStartImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundStartImage,backgroundRect)
    mainBlock = createRectWithImage(pos_x,pos_y,cfg.MAINANCHO,cfg.MAINALTO,color=cfg.WHITE,image=mainBlockImg)
    createText(startFont,f'Press Start to start playing.',True,cfg.BLACK,screen,(width/2,200))
    createText(startFont,f'Max Score: {maxScoreFileData}',True,cfg.BLACK,screen,(100,(height-100)))
    createText(startFont,f'Attempts: {attemptsFileData}',True,cfg.BLACK,screen,(width - 100,(height-100)))
    pygame.display.flip()
    liveCounter = 3
    scoreCounter = 0
    is_running = True
    mute = waitUserClick(buttonPlay,buttonOptions,buttonExit,screen,menuState)
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
                    # Creo un shot
                    shotsList.append(createShot(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
            if event.type == deathEvent:
                dying.play()
                limpiar()
                is_running = False
            if event.type == shootEvent:
                # Creo un shot
                shotsList.append(createShot(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
            if event.type == restartPowerUp:
                shootInterval = 400
                mainBlock['speed-y'] = randint(2,3)
                poweredUp = False
            if event.type == powerUpFallingEvent:
                # Duplico la velocidad de shot
                powerUpList.append(createRectWithImage(left=width+ancho,top=randint(50,450),ancho=60,alto=45,image=powerUpImage,vidas=1))
            if event.type == fallingBlock:
                i = randint(0,1)
                if i==0:
                    blockList.append(createRectWithImage(left=width+ancho,ancho=ancho,alto=alto,top=randint(100,400),image=enemiesImages[i],vidas=1))
                else:
                    blockList.append(createRectWithImage(left=width+ancho,ancho=ancho,alto=alto,top=randint(50,450),image=enemiesImages[i],vidas=3))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    limpiar()
                    is_running = False
                if event.key == pygame.K_SPACE:
                    shotsList.append(createShot(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg,offsetBlock=cfg.MAINANCHO//2))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = True
                    move_down = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = True
                    move_up = False
                if event.key == pygame.K_h:
                    hardcoreMode = not hardcoreMode
                if event.key == pygame.K_m:
                    mute = not mute
                if event.key == pygame.K_SEMICOLON:
                    cheatOn = not cheatOn
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

# Blit De Textos, background y main block
        backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
        screen.blit(backgroundImage,backgroundRect)
        screen.blit(mainBlock['image'],mainBlock['rect'])
        createText(my_font,f'Score: {scoreCounter}',True,cfg.BLACK,screen,(200,50))
        createText(my_font,f'Lives: {liveCounter}',True,cfg.BLACK,screen,((width-200),50))
        # si esta en ejecucion el juego hago el blit de los blockList principales
        if is_running:
            for shot in shotsList:
                screen.blit(shot['image'],shot['rect'])
            for block in blockList:
                screen.blit(block['image'],block['rect'])
            for powerUp in powerUpList:
                screen.blit(powerUp['image'],powerUp['rect'])

                
        if mute == True:
            pygame.mixer.music.set_volume(False)
        else:
            pygame.mixer.music.set_volume(0.5)
        # PREGUNTAR PORQUE EL COMPORTAMIENTO DE CUANDO ESTA EN FALSE LO TOMA COMO TRUE Y VICEVERSA, ACA DEBERIA IR UN TRUE PERO LO CONSIDERA UN FALSE Y NO DISPARA. SE QUEDA DISPARANDO CUANDO SOLTAS ES CLICK SI ESTA EN TRUE.
        # Y PORQUE EL COMPORTAMIENTO DE CUANDO PONGO LA BARRA ESPACIADORA TAMBIEN SOLO FUNCIONA CUANDO AMBAS CONDICIONES ESTAN
        # Lo vamos a ver en clase
        if  mousepressed[0] == False : 
            pygame.time.set_timer(shootEvent, shootInterval)

        if cheatOn == True:
            shootInterval = 90
            mainBlock['speed-y'] = 10
            poweredUp = True
            
# MOVER ELEMENTOS

        # MUEVO LOS ALIENS CAYENDO Y LOS shotsList
        for shot in shotsList[:]:
            rectshot=shot['rect']
            rectshot.move_ip(Speed*2,0)
            if rectshot.right  < 0:
                shotsList = borrarItemLista(shotsList,shot)
        for powerUp in powerUpList[:]:
            rectPower = powerUp['rect']
            rectPower.move_ip(-powerUp['speed-x']*0.5,0)
            if rectPower.right< 0:
                if powerUp:
                    powerUpList = borrarItemLista(powerUpList,powerUp)
            if detectCollisionRect(powerUp,mainBlock):
                if poweredUp == False:
                    shootInterval = 150
                    mainBlock['speed-y'] = 5
                    poweredUp = True
                    powerUpSound.play()
                    pygame.time.set_timer(restartPowerUp,cfg.RESTART_POWERUP,1)
                powerUpList = borrarItemLista(powerUpList,powerUp)
        # Detecto las colisiones con los shotsList para penalizar al usuario cuando dispara a un power up
            for shot in shotsList[:]:
                if detectCollisionRect(powerUp,shot):
                    if powerUp['vidas'] <= 1:
                        powerUpList = borrarItemLista(powerUpList,powerUp)
                    else:
                        powerUp['vidas'] -= 1
                    shotsList = borrarItemLista(shotsList,shot)
        # Crear un sonido de muerte de powerUp a mano como los otros.s
                    explosion.play()

        for block in blockList[:]:
            rect=block['rect']
            rect.move_ip(-block['speed-y'],0)
        # AUMENTO LA DIFICULTAD CON HARDCORE MODE O CON PUNTOS A 30 PARA QUE EMPIEZEN A MOVERSE LOS OBJETOS EN AMBAS DIRECCIONES
        # TAMBIEN ACELERO AL PERSONAJE PRINCIPAL PARA QUE ESQUIVAR SEA MAS POSIBLE, LA IDEA ES BUSCAR TECNICA Y POSIBILITAR QUE SIGA LO MAS POSIBLE TAMBIEN
            if scoreCounter > 30 or hardcoreMode == True:
                mainBlock['speed-y'] = 5
                if posiciones == True : 
                    if rect.y > 0 :
                        rect.move_ip(-block['speed-x'],-block['speed-y'])
                        
                    else:
                        posiciones = False
                else:
                    if rect.y < height - rect.height:
                        rect.move_ip(-block['speed-x'],+block['speed-y'])
                    else:
                        posiciones = True
# DETECTO COLISIONES

        # Final de pantalla borro block para liberar memoria le sumo 5 para que se vea mas prolijo y aseguro
        # Tengo que validar que el block exista antes de borrarlo porque puede haber sido borrado por alguna colision (la prioridad la tienen los shotsList)
            if rect.right < 0:
                blockList = borrarItemLista(blockList,block) 
        # Chequeo la colision con el tiro y los aliens
            for shot in shotsList[:]:
                if detectCollisionRect(block,shot):
                    if block['vidas'] <= 1: 
                        blockList = borrarItemLista(blockList,block) 
                        scoreCounter +=1
                    else:
                        block['vidas'] -= 1
        # Sector dificultad
                    if scoreCounter >= 50:
                        livesIncremental = 2
                    elif scoreCounter >= 100:
                        livesIncremental = 3
                    shotsList = borrarItemLista(shotsList,shot)
                    explosion.play()
        # Detecto las colisiones con el mainbody
            if detectCollisionRect(block,mainBlock):
                if liveCounter == 1 :
                    limpiar()
                    finalExplosion.play()
                    pygame.time.set_timer(deathEvent,100,1)
                else:
                    liveCounter -= 1
                    hitSpaceShip.play()
                    blockList = borrarItemLista(blockList,block) 
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
    # screen.blit(keyToContinue,((width - keyToContinue.get_width())/2,(height - 50)/1.7))\
    if maxScoreFileData < scoreCounter:
        # Escribo el puntaje max nuevo
        data[0]['value'] = scoreCounter
        data[1]['value'] = 0
    else:
        # Sumo uno a los intentos
        data[1]['value'] = attemptsFileData + 1
    
    try:
        with open("./db.json",'w') as dataEnd:
            json.dump(data,dataEnd,indent=2)
    except OSError.filename as Err:
        errMsg("Error while writing the scores to the datafile. The score wont be saved")
        print(Err)
        errMsg('Please validate the files and check again. If the problem persist re-install the files')
    pygame.mixer.music.stop()
    pygame.display.flip()
    waitUser()