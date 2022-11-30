import pygame as pg
import random
import sys
#INICIALIZAR PYGAME Y LA CARGA DE AUDIO
pg.init()
pg.mixer.init

#CLASE DEL JUGADOR
class Jugador(pg.sprite.Sprite):
        def __init__(self):
                #ATRIBUTOS BÁSICOS
                super().__init__()
                self.image = pg.image.load("caraWilly.png")
                self.rect = self.image.get_rect()
                self.rect.centerx = ancho//2
                self.rect.centery = alto//2
                self.vel_x = 5
                self.vel_y = 5
                self.cadencia = 750
                self.ultimo_disparo = pg.time.get_ticks()
                self.nivelActual = 1
                self.experienciaActual = 0
                self.experienciaMaxima = 100

        #MOVIMIENTO DEL JUGADOR Y SUS LIMITES
        def update(self):
                self.vel_x = 0
                self.vel_y = 0
                #MOVER ARRIBA
                if estadoTecla[pg.K_w]:
                        self.vel_y = -5
                        self.rect[1] += self.vel_y
                #MOVER IZQUIERDA
                if estadoTecla[pg.K_a]:
                        self.vel_x = -5
                        self.rect[0] += self.vel_x
                #MOVER ABAJO
                if estadoTecla[pg.K_s]:
                        self.vel_y = 5
                        self.rect[1] += self.vel_y
                #MOVER DERECHA
                if estadoTecla[pg.K_d]:
                        self.vel_x = 5
                        self.rect[0] += self.vel_x
                #LIMITES DE MOVIMIENTO
                if self.rect.left < 0:
                        self.rect.left = 0
                if self.rect.right > ancho:
                        self.rect.right = ancho
                if self.rect.top < 0:
                        self.rect.top = 0
                if self.rect.bottom > alto:
                        self.rect.bottom = alto
                #SUBIR DE NIVEL
                if self.experienciaActual >= self.experienciaMaxima:
                        self.nivelActual += 1
                        self.experienciaActual = 0
                        self.experienciaMaxima += 120
        #DISPAROS DEL JUGADOR
        def dis_arri(self):
                if estadoTecla[pg.K_UP]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadencia:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = -10)
                                totalSprites.add(bala)
                                balasJugador.add(bala)
                                self.ultimo_disparo = ahora
        
        def dis_izqu(self):
                if estadoTecla[pg.K_LEFT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadencia:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = -10)
                                totalSprites.add(bala)
                                balasJugador.add(bala)
                                self.ultimo_disparo = ahora
        
        def dis_abaj(self):
                if estadoTecla[pg.K_DOWN]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadencia:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = 10)
                                totalSprites.add(bala)
                                balasJugador.add(bala)
                                self.ultimo_disparo = ahora
        
        def dis_dere(self):
                if estadoTecla[pg.K_RIGHT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadencia:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = 10)
                                totalSprites.add(bala)
                                balasJugador.add(bala)
                                self.ultimo_disparo = ahora

class Bala(pg.sprite.Sprite):
        def __init__(self,x, y, vel_x = 0, vel_y = 0):
                super().__init__()
                self.image = pg.image.load("bala2.png")
                #self.image_resize = pg.transform.scale(self.image, (10,10))
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.y = y
                self.vel_x = vel_x
                self.vel_y = vel_y
                self.daño = 1

        def update(self):
                self.rect[0] += self.vel_x
                self.rect[1] += self.vel_y
                if self.rect.bottom < 0 or self.rect.top > alto or self.rect.right < 0 or self.rect.left > ancho:
                        self.kill()

class Enemigo1(pg.sprite.Sprite):
        def __init__(self):
                #ATRIBUTOS BÁSICOS
                super().__init__()
                self.image = pg.image.load("caraJunior.png")
                self.rect = self.image.get_rect()
                self.rect.centerx = random.randrange(ancho + 40, ancho +150)
                self.rect.centery = random.randrange(alto)
                self.vida = 2
                self.vel_x = 2
                self.vel_y = 2 
        
        def update(self, x, y):
                if x < self.rect.centerx:
                        self.rect[0] -= self.vel_x
                if x > self.rect.centerx:
                        self.rect[0] += self.vel_x
                if y < self.rect.centery:
                        self.rect[1] -= self.vel_y
                if y > self.rect.centery:
                        self.rect[1] += self.vel_y


#GRUPOS DE SPIRITES
totalSprites = pg.sprite.Group()
enemigos = pg.sprite.Group()
balasJugador = pg.sprite.Group()

#CONFIGURACIÓN BÁSICA DE LA VENTANA
clock = pg.time.Clock()
pg.display.set_caption("Catlord 0.03")
tamañoVentana = ancho, alto = 1920, 1080
pantalla = pg.display.set_mode(tamañoVentana)
negro = 0,0,0
blanco = 255,255,255

jugador = Jugador()
totalSprites.add(jugador)


for x in range(20):
        enemigo = Enemigo1()
        enemigos.add(enemigo)


GameOver = False
while not GameOver:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        GameOver = True
        
        estadoTecla = pg.key.get_pressed()

        pantalla.fill(blanco)
        
        totalSprites.update()
        balasJugador.update()
        enemigos.update(jugador.rect.centerx , jugador.rect.centery)
        
        print(jugador.experienciaActual)
        print(jugador.nivelActual)
        
        colisionBalaYEnemigo = pg.sprite.groupcollide(balasJugador, enemigos, True, True)
        if colisionBalaYEnemigo:
                jugador.experienciaActual += 10
        colisionEnemigoYEnemigo = pg.sprite.groupcollide(enemigos, enemigos, False, False)
        if colisionEnemigoYEnemigo:
                for x in enemigos:
                        x.rect.bottom = x.rect.bottom

        jugador.dis_arri()
        jugador.dis_izqu()
        jugador.dis_abaj()
        jugador.dis_dere()
        

        balasJugador.draw(pantalla)
        totalSprites.draw(pantalla)
        enemigos.draw(pantalla)
        

        pg.display.flip()
        clock.tick(60)