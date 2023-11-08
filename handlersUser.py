import pygame
from creating import createButton
import sys
import config as cfg

def waitUserClick (rect_1:pygame.Rect,rect_2:pygame.Rect,rect_3:pygame.Rect,screen,menuState):
    colorMuted = True
    # agregar la funcion crear_boton que crea un rect con texto y background que cuando el mouse esta encima cambia el color del fondo
    while menuState == 'main':
        createButton(screen,rect_1,cfg.GREY,'Play!',cfg.BLACK)
        createButton(screen,rect_3,cfg.GREY,'Exit',cfg.BLACK)
        createButton(screen,rect_2,cfg.GREY,'Options',cfg.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor = event.pos
                if event.button == 1:
                    if rect_1.collidepoint(cursor[0],cursor[1]):
                        return not colorMuted
                    if rect_2.collidepoint(cursor[0],cursor[1]):
                        menuState = 'options'
                    if rect_3.collidepoint(cursor[0],cursor[1]):
                        exit()
        pygame.display.flip()
    
        while menuState == 'options':
            # options(screen,rect_1,rect_2,rect_3)
            createButton(screen,rect_3,cfg.GREY,'Go Back',cfg.BLACK)
            if colorMuted:
                createButton(screen,rect_2,cfg.GREEN,'Music On',cfg.BLACK)
                pygame.mixer.music.set_volume(0.5)
            else:
                createButton(screen,rect_2,cfg.RED,'Music Off',cfg.BLACK)
                pygame.mixer.music.set_volume(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor = event.pos
                    if event.button == 1:
                        if rect_1.collidepoint(cursor[0],cursor[1]):
                            return not colorMuted
                        if rect_2.collidepoint(cursor[0],cursor[1]):
                            colorMuted =  not colorMuted
                        if rect_3.collidepoint(cursor[0],cursor[1]):
                            menuState = 'main'
            pygame.display.flip()

def waitUser ():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Hasta luego lucassss')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('See ya laater lucass')
                    sys.exit()
                return




def exit():
    print('Nos vemos en la proxima!')
    pygame.quit()
    sys.exit()

def errMsg(msg):
    print("")
    print(msg)
    print("")

# def options(screen,rect_1,rect_2,rect_3):
