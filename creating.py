import pygame 
import config as cfg
from random import randint

pygame.font.init()
default_font = pygame.font.SysFont('javanesetext', 24,True)

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

def createText(fuente,texto,AA,color,source,coordenadas):
    text_rec = fuente.render(texto,AA,color)
    text_rectCentered = text_rec.get_rect(center=(coordenadas[0],coordenadas[1]))
    source.blit(text_rec,text_rectCentered)

def createButton (screen,rect,background,text,textColor):
    pygame.draw.rect(screen,background,rect,border_radius=20)
    createText(default_font,text,True,textColor,screen,(rect.centerx,rect.centery))

    
def createDefaultDb():
    arr = []
    data = dict()
    data['key'] = 'score'
    data['value'] = 0
    arr.append(data)
    dataAttempt = dict()
    dataAttempt['key'] = 'attempts'
    dataAttempt['value'] = 0
    arr.append(dataAttempt)

    return arr

    
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
