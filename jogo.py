import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Jogo Snake')
pygame.font.init()
clock = pygame.time.Clock()

LARGURA = 800
ALTURA = 600

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERMELHO = (120, 0, 0)
VERDE_ESCURO = (0, 120, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)


class cubo(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, cor=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.cor = cor

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, olhos=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.cor, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if olhos:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    corpo = []
    curvas = {}

    def __init__(self, cor, pos):
        self.cor = cor
        self.cabeca = cubo(pos)
        self.corpo.append(self.cabeca)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.curvas[self.cabeca.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.curvas[self.cabeca.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.curvas[self.cabeca.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.curvas[self.cabeca.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.corpo):
            p = c.pos[:]
            if p in self.curvas:
                curva = self.curvas[p]
                c.move(curva[0], curva[1])
                if i == len(self.corpo) - 1:
                    self.curvas.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.cabeca = cubo(pos)
        self.corpo = []
        self.corpo.append(self.cabeca)
        self.curvas = {}
        self.dirnx = 0
        self.dirny = 1

    def addcubo(self):
        rabo = self.corpo[-1]
        dx, dy = rabo.dirnx, rabo.dirny

        if dx == 1 and dy == 0:
            self.corpo.append(cubo((rabo.pos[0] - 1, rabo.pos[1])))
        elif dx == -1 and dy == 0:
            self.corpo.append(cubo((rabo.pos[0] + 1, rabo.pos[1])))
        elif dx == 0 and dy == 1:
            self.corpo.append(cubo((rabo.pos[0], rabo.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.corpo.append(cubo((rabo.pos[0], rabo.pos[1] + 1)))

        self.corpo[-1].dirnx = dx
        self.corpo[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.corpo):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.corpo

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return(x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cubo(randomSnack(rows, s), cor=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.corpo[0].pos == snack.pos:
            s.addcubo()
            snack = cubo(randomSnack(rows, s), cor=(0, 255, 0))

        for x in range(len(s.corpo)):
            if s.corpo[x].pos in list(map(lambda z: z.pos, s.corpo[x + 1:])):
                message_box('Voce Perdeu!!', 'Pontuacao: '+str(len(s.corpo)))
                s.reset((10, 10))
                break

        redrawWindow(win)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def cria_botao(msg, sqr, cor1, cor2, cor_texto, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]:
        pygame.draw.rect(display, cor2, sqr)
        if clique[0] == 1 and acao != None:
            acao()
    else:
        pygame.draw.rect(display, cor1, sqr)

    fontePequena = pygame.font.SysFont('comicsansms', 20)
    surface_texto, rect_texto = text_objects(msg, fontePequena, cor_texto)
    rect_texto.center = (sqr[0] + 60, sqr[1] + 20)
    display.blit(surface_texto, rect_texto)


def menu_jogo():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(PRETO)
        fonte = pygame.font.SysFont('comicsansms', 50)
        surface_texto, rect_texto = text_objects("Jogo Snake", fonte, BRANCO)
        rect_texto.center = ((LARGURA / 2), ALTURA / 3)
        display.blit(surface_texto, rect_texto)

        cria_botao("INICIAR", (LARGURA - 760, ALTURA / 2, 120, 40), VERDE_CLARO, VERDE_ESCURO, BRANCO, main)
        #cria_botao("MANUAL", (LARGURA - 560, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, regras)
        cria_botao("SAIR", (LARGURA - 160, ALTURA / 2, 120, 40), VERMELHO_CLARO, VERMELHO, BRANCO, sair)

        pygame.display.update()
        clock.tick(15)


# SAIR DO JOGO
def sair():
    pygame.quit()
    quit()

menu_jogo()
