import math
import pygame
import config as cfg
import sys
from random import randint

pygame.font.init()
default_font = pygame.font.SysFont('javanesetext', 24,True)

def detectCollisionRect(rect1:dict, rect2:dict):
    # obtengo las mascaras del diccionario del rect1 y 2 y hago la formula del offset y checkeo el overlap

    # la funcion devuelve la tupla de coordenadas o none || Se pueden considerar como truthy o falsy
    mask1 = rect1['mask']
    mask2 = rect2['mask']
    offset = (rect2['rect'].x - rect1['rect'].x ,rect2['rect'].y - rect1['rect'].y)
    resultCollision = mask1.overlap(mask2,offset)
    return resultCollision

def distanceBetweenPoints(punto1,punto2):
    x1,y1 = punto1
    x2,y2 = punto2
    return math.sqrt((y1-y2) ** 2 + (x1-x2) ** 2)

def calculateRadiusRect (rect:pygame.Rect):
    return rect.width // 2

def createRectWithImage(left=0,top=0,ancho=25,alto=25,color=cfg.GREEN, borde = 0, radio= -1,image=None,vidas= 1):
    if image:
        image = pygame.transform.scale(image,(ancho,alto))
        mask = pygame.mask.from_surface(image)
        rect = image.get_rect()
        rect.move_ip(left,top)
    else:
        image = None
    
    return { 'rect':rect , 'color':color, 'borde':borde,'radio':radio,'image':image,'vidas':vidas,'speed-y':randint(2,3),'speed-x':randint(2,3),'mask':mask}


def createShot(left,top,imagen,offsetBlock=0,ancho=20,alto=10):
    imagen = pygame.transform.scale(imagen,(ancho,alto))
    mask = pygame.mask.from_surface(imagen)
    disparoRec = imagen.get_rect()
    disparoRec.move_ip(left+offsetBlock*2,top+offsetBlock/2)
    return { 'rect':disparoRec,"image":imagen,'mask':mask}

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
        createButton(screen,rect_1,cfg.GREY,'Play!',cfg.BLACK)
        createButton(screen,rect_3,cfg.GREY,'Exit',cfg.BLACK)
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
                        exit()
        pygame.display.flip()
                    
def createText(fuente,texto,AA,color,source,coordenadas):
    text_rec = fuente.render(texto,AA,color)
    text_rectCentered = text_rec.get_rect(center=(coordenadas[0],coordenadas[1]))
    source.blit(text_rec,text_rectCentered)

def createButton (screen,rect,background,text,textColor):
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