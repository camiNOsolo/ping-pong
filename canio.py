#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
# ---------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
# ---------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------
WIDTH = 640
HEIGHT = 480
FPS = 200
BLACK = (0 ,0 ,0)
WHITE = (255,255,255)
LINEA = 10

# ---------------------------------------------------------------------
# Clases
# ---------------------------------------------------------------------
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = 0.4
        self.m = 1
        self.n = self.rect.centery - self.rect.centerx * self.m
 
    def actualizar(self, time, pala_jug, pala_cpu, puntos):
        self.rect.centerx += self.speed * time
        self.rect.centery = self.rect.centerx * self.m + self.n

        if self.rect.left <= 0:
            puntos[1] += 1

        if self.rect.right >= WIDTH:
            puntos[0] += 1


        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed = -self.speed
            self.m = -self.m
            self.n = self.rect.centery - self.rect.centerx * self.m
            self.rect.centerx += self.speed * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.m = -self.m
            self.n = self.rect.centery - self.rect.centerx * self.m
            self.rect.centery = self.rect.centerx * self.m + 4
        
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed = -self.speed
            self.m = -self.m
            self.n = self.rect.centery - self.rect.centerx * self.m
            self.rect.centerx += self.speed * time
        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed = -self.speed
            self.m = -self.m
            self.n = self.rect.centery - self.rect.centerx * self.m
            self.rect.centerx += self.speed * time

        return puntos

class Pala(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5
        
    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time
    def ia(self, time, bola):
        if bola.speed >= 0.4 and bola.rect.centerx >= WIDTH/1.4:
            if self.rect.centery < bola.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > bola.rect.centery:
                self.rect.centery -= self.speed * time

# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    try:
        fuente = pygame.font.Font("ASMAN.TTF", 35)
    except:
        fuente = pygame.font.SysFont('monospace', 35)

    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def pause():
    pausa=True
    while pausa:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT or evento.type == K_ESCAPE:
                pygame.quit()
                quit()
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_c:
                    pausa=False
                if evento.key==pygame.K_q:
                    pygame.quit()
                    quit()
        SCREEN.fill(BLACK)
        fuente = pygame.font.Font(None, 90)
        text = "PAUSE"
	mensaje = fuente.render(text, 1, WHITE)
	SCREEN.blit(mensaje, ((WIDTH/2), (HEIGHT/2)))
	pygame.display.flip()
        CLOCK.tick(15)

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    pygame.init()
    global SCREEN, CLOCK
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Ping&Pong")
    bola = Bola()
    pala_jug = Pala(30)
    pala_cpu = Pala(WIDTH - 30)
    puntos = [0, 0]
    
    while True:
        time = CLOCK.tick(FPS)
        keys = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == QUIT or evento.type == K_ESCAPE:
                pygame.quit()
                sys.exit()
	    if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_p:
		    pause()
        
	fuente = pygame.font.Font(None, 20)
        text = "Pulsa 'p' para Pausar o 'Escape' para Salir"
        mensaje = fuente.render(text, 1, WHITE)
        
        puntos = bola.actualizar(time, pala_jug, pala_cpu, puntos)
        pala_jug.mover(time, keys)
        pala_cpu.ia(time, bola)

        p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH/4, 40)
        p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)
        SCREEN.fill((0,0,0))
        pygame.draw.line(SCREEN, WHITE, ((WIDTH/2),0),((WIDTH/2),HEIGHT), (LINEA/4))
        SCREEN.blit(mensaje, ((WIDTH / 2 + 10), (HEIGHT - 20)))
        
        SCREEN.blit(p_jug, p_jug_rect)
        SCREEN.blit(p_cpu, p_cpu_rect)
        SCREEN.blit(bola.image, bola.rect)
        SCREEN.blit(pala_jug.image, pala_jug.rect)
        SCREEN.blit(pala_cpu.image, pala_cpu.rect)

        pygame.display.update()

    return 0
 
if __name__ == '__main__':
    main()
