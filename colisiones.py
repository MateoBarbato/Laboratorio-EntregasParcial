import math
import pygame

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


