import math
import pygame
import config as cfg
import sys
from random import randint

pygame.font.init()
default_font = pygame.font.SysFont('javanesetext', 24,True)

def detectar_colision_circ(rect1:pygame.Rect ,rect2:pygame.Rect):
    distancia = distancia_entre_puntos(rect1.center,rect2.center)
    r1 = calcular_radio_rectangulo(rect1)
    r2 = calcular_radio_rectangulo(rect2)

    return distancia <= (r1+r2)

def distancia_entre_puntos(punto1,punto2):
    x1,y1 = punto1
    x2,y2 = punto2
    return math.sqrt((y1-y2) ** 2 + (x1-x2) ** 2)

def calcular_radio_rectangulo (rect:pygame.Rect):
    return rect.width // 2

def crearRecImagen (left=0,top=0,ancho=25,alto=25,color=cfg.GREEN, borde = 0, radio= -1,image=None,vidas= 1):
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

def waitUserClick (rect_1:pygame.Rect,rect_2:pygame.Rect,rect_3:pygame.Rect,screen):
    colorMuted = True
    # agregar la funcion crear_boton que crea un rect con texto y background que cuando el mouse esta encima cambia el color del fondo
    while True:
        crearBoton(screen,rect_1,cfg.GREY,'Play!',cfg.BLACK)
        crearBoton(screen,rect_3,cfg.GREY,'Exit',cfg.BLACK)
        if colorMuted:
            crearBoton(screen,rect_2,cfg.GREEN,'Music On',cfg.BLACK)
            pygame.mixer.music.set_volume(0.5)
        else:
            crearBoton(screen,rect_2,cfg.RED,'Music Off',cfg.BLACK)
            pygame.mixer.music.set_volume(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Hasta luego lucassss')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('See ya laater lucass')
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor = event.pos
                if event.button == 1:
                    if rect_1.collidepoint(cursor[0],cursor[1]):
                        print('Clickeado')
                        # sys.exit()
                        return not colorMuted
                    if rect_2.collidepoint(cursor[0],cursor[1]):
                        colorMuted =  not colorMuted
                    if rect_3.collidepoint(cursor[0],cursor[1]):
                        print('Hasta la vista!')
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()
                    
def createText(fuente,texto,AA,color,source,coordenadas):
    text_rec = fuente.render(texto,AA,color)
    text_rectCentered = text_rec.get_rect(center=(coordenadas[0],coordenadas[1]))
    source.blit(text_rec,text_rectCentered)

def crearBoton (screen,rect,background,text,textColor):
    pygame.draw.rect(screen,background,rect,border_radius=20)
    createText(default_font,text,True,textColor,screen,(rect.centerx,rect.centery))
    
def borrarItemLista(lista:list,item:dict):
    # Tuve que crear esta funcion porque me tiraba value error al eliminar un objeto de la lista demasiado rapido y llegaba un punto en el que eliminaba algo que no existia en esa posicion
    # encontre esta solucion investigando que lo que hace es copiar la lista y chequear antes de borrar si el item puede ser borrado, si no puede ser borrado devuelve la lista como esta
    # no genera problema porque cuando sucede el error esta fuera de pantalla o a punto de ser renderizado.
    # Por ahora lo testee y no tuve mas errores de ejecucion ni objetos que deberian ser borrados y no se borran asi que estaria cumpliendo con el objetivo 
    # ESTO SOLO SUCENDE CON EL CHIT DE DISPARAR CON EL CLICK Y LA BARRA SPAM (SIN MANTENER APRETADO). Con el funcionamiento normal no generaba problema pero lo aplico para evitar de erorres de ejecucion
    listaAEditar =  lista[:]
    try:
        listaAEditar.remove(item)
    except ValueError:
        pass
    return listaAEditar

def exit():
    print('Nos vemos en la proxima!')
    pygame.quit()
    sys.exit()