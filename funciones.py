import math
import pygame
import config
import sys
from random import randint

pygame.font.init()
default_font = pygame.font.SysFont('javanesetext', 24,True)

def detectar_colision_circ(rect1 ,rect2):
    distancia = distancia_entre_puntos(rect1.center,rect2.center)
    r1 = calcular_radio_rectangulo(rect1)
    r2 = calcular_radio_rectangulo(rect2)

    return distancia <= (r1+r2)

def distancia_entre_puntos(punto1,punto2):
    x1,y1 = punto1
    x2,y2 = punto2
    return math.sqrt((y1-y2) ** 2 + (x1-x2) ** 2)

def calcular_radio_rectangulo (rect):
    return rect.width // 2

def crearRecImagen (left=0,top=0,ancho=25,alto=25,color=config.GREEN, borde = 0, radio= -1,image=None,vidas= 1):
    if image:
        image = pygame.transform.scale(image,(ancho,alto))
    else:
        image = None
    rect = pygame.Rect(left,top,ancho,alto)
    return { 'rect':rect , 'color':color, 'borde':borde,'radio':radio,'image':image,'vidas':vidas,'speed-y':randint(2,3),'speed-x':randint(2,3)}


def crearDisparo(left,top,imagen,offsetBlock=0,ancho=20,alto=10):
    imagen = pygame.transform.scale(imagen,(ancho,alto))
    
    disparoRec = pygame.Rect(left+offsetBlock*2,top+offsetBlock/2,ancho,alto)
    return { 'rect':disparoRec,"image":imagen}

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

def waitUserClick (rect_1:pygame.Rect):
    # agregar la funcion crear_boton que crea un rect con texto y background que cuando el mouse esta encima cambia el color del fondo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Hasta luego lucassss')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('See ya laater lucass')
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_1.collidepoint(pygame.mouse.get_pos()):
                        # print('See ya laater lucass')
                        # sys.exit()
                        return

def mostrarTexto (fuente,texto,AA,color,coordinates,screen):
    text_score = fuente.render(texto,AA,color)
    screen.blit(text_score,coordinates)

def crearBoton (screen,rect,texto,background,backgroundHover):
    if rect.collidepoint(pygame.mouse.get_pos()):
        text_button = default_font.render(texto,True,config.WHITE,backgroundHover)
    else:
        text_button = default_font.render(texto,True,config.WHITE,background)

    screen.blit(text_button,rect)
    


def exit():
    print('Nos vemos en la proxima!')
    pygame.quit()
    sys.exit()