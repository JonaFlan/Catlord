import pygame as pg
import random
import sys
import mysql.connector as sql
import datetime

#INICIALIZAR PYGAME Y LA CARGA DE AUDIO
pg.init()
pg.mixer.init()

class Conexion():
        def __init__(self):
                self.db = sql.connect(user = "root", passwd = "root", host = "localhost", database = "catlorddb", port = "3306")
                self.cursor = self.db.cursor()
                self.accion = ""
                self.valor = ""
                self.resultado = ""

        def enviarPuntuacion(self):
                self.accion = ("insert into puntuacion (nombre, eliminaciones, puntuacion, fecha) values (%s,%s,%s,%s)")
                self.valor = (jugador.nombre, jugador.eliminaciones, jugador.puntuacion, fechaFinal)
                self.cursor.execute(self.accion, self.valor)
                self.db.commit()
                input("Puntuación enviada")
        
        def consultarPuntuaciones(self):
                self.cursor.execute("select * from puntuacion")
                self.resultado = self.cursor.fetchall()
                contador = 0
                diferencia = 0
                
                print("ID     NOM    ELI    PUN    FEC\n_____________________________________________")
                for x in range(len(self.resultado)):
                        for y in range(5):
                                if contador < 4:
                                        diferencia = 5 - len(str(self.resultado[x][y]))
                                        print(str(self.resultado[x][y]) + " " * diferencia, end="|" * 2)
                                        contador += 1
                                elif contador == 4:
                                        print(self.resultado[x][y])
                                        contador = 0

        def eliminarPuntuacion(self, puntuacion):
                self.cursor.execute("delete from puntuacion where id_puntuacion =" + str(puntuacion))
                self.db.commit()
                input("Registro eliminado")
        
        def cambiarNombre(self, puntuacion, nombre):
                self.accion = ("update puntuacion set nombre = '%s' where id_puntuacion = '%s'")
                self.valor = (puntuacion, nombre)
                self.cursor.execute("update puntuacion set nombre = '" + nombre + "'where id_puntuacion = " + str(puntuacion))
                self.db.commit()
                input("Registro actualizado")

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
                self.cadenciaDisparo = 750
                self.ultimo_disparo = pg.time.get_ticks()
                self.nivelActual = 1
                self.experienciaActual = 0
                self.experienciaMaxima = 100
                self.eliminaciones = 0
                self.puntuacion = 0
                self.nombre = ""

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
                
        #DISPARO DEL JUGADOR
                if estadoTecla[pg.K_UP]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = -10)
                                balasJugadorSprites.add(bala)
                                self.ultimo_disparo = ahora
                
                if estadoTecla[pg.K_LEFT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = -10)
                                balasJugadorSprites.add(bala)
                                self.ultimo_disparo = ahora
                
                if estadoTecla[pg.K_DOWN]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = 10)
                                balasJugadorSprites.add(bala)
                                self.ultimo_disparo = ahora

                if estadoTecla[pg.K_RIGHT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimo_disparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = 10)
                                balasJugadorSprites.add(bala)
                                self.ultimo_disparo = ahora
        
                #SUBIR DE NIVEL
                if self.experienciaActual >= self.experienciaMaxima:
                        self.nivelActual += 1
                        self.experienciaActual = 0
                        self.experienciaMaxima += 120

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
                self.respawn = random.randint(1, 4)

                #SPAWN ARRIBA
                if self.respawn == 1:
                        self.rect.centerx = random.randrange(ancho)
                        self.rect.centery = random.randrange(-150, 0)
                        self.vel_x = 0
                        self.vel_y = 5
                #SPAWN IZQUIERDA 
                elif self.respawn == 2:
                        self.rect.centerx = random.randrange(-150, 0)
                        self.rect.centery = random.randrange(alto)
                        self.vel_x = 5
                        self.vel_y = 0
                #SPAWN ABAJO
                elif self.respawn == 3:
                        self.rect.centerx = random.randrange(ancho)
                        self.rect.centery = random.randrange(alto, alto + 150)
                        self.vel_x = 0
                        self.vel_y = -5
                #SPAWN DERECHA
                elif self.respawn == 4:
                        self.rect.centerx = random.randrange(ancho, ancho +150)
                        self.rect.centery = random.randrange(alto)
                        self.vel_x = -5
                        self.vel_y = 0
                self.vida = 2
        
        def update(self):
                self.rect[0] += self.vel_x
                self.rect[1] += self.vel_y
                if self.rect.top >= alto + 150 or self.rect.left >= ancho + 150 or self.rect.bottom <= -150 or self.rect.right <= -150:
                        self.kill()

conexion = Conexion()

#MENU EN CONSOLA
inicio = 0
while inicio != 1:
        inicio = int(input("1) Iniciar juego || 2) Puntuaciones \n"))
        if inicio == 2:
                conexion.consultarPuntuaciones()
                menu1 = int(input("1) Eliminar registro || 2) Editar nombre || 3) Volver \n"))
                while menu1 == 1: 
                        conexion.consultarPuntuaciones()
                        eleccionBorrar = int(input("Seleccionar registro: "))
                        for x in range(len(conexion.resultado)):
                                if conexion.resultado[x][0] == eleccionBorrar:
                                        conexion.eliminarPuntuacion(conexion.resultado[x][0])
                        eleccion = int(input("1) Continuar || 2) Volver\n"))
                        if eleccion == 2:
                                menu1 = 0
                                        
                while menu1 == 2:
                        conexion.consultarPuntuaciones()
                        eleccionCambiar = int(input("Seleccionar registro: "))
                        for x in range(len(conexion.resultado)):
                                if conexion.resultado[x][0] == eleccionCambiar:
                                        nombre = ""
                                        while nombre == "" or len(nombre) > 5:
                                                nombre = input("Ingresar nuevo nombre (Máximo 5 carácteres): ")
                                                if nombre == "" or len(nombre) > 5:
                                                        print("Nombre no válido")
                                        conexion.cambiarNombre(conexion.resultado[x][0], nombre)
                        eleccion = int(input("1) Continuar || 2) Volver\n"))
                        if eleccion == 2:
                                menu1 = 0



#GRUPOS DE SPIRITES
jugadorSprite = pg.sprite.Group()
enemigosSprites = pg.sprite.Group()
balasJugadorSprites = pg.sprite.Group()

#CONFIGURACIÓN BÁSICA DE LA VENTANA
clock = pg.time.Clock()
pg.display.set_caption("Catlord 0.03")
tamañoVentana = ancho, alto = 1920, 1080
pantalla = pg.display.set_mode(tamañoVentana)
negro = 0,0,0
blanco = 255,255,255

#ADICIÓN DEl JUGADOR AL GRUPO
jugador = Jugador()
jugadorSprite.add(jugador)

#PARÁMETROS DE REAPARICIÓN DE ENEMIGOS
tiempoRespawn = 1500
ultimoRespawn = pg.time.get_ticks()

final = False


GameOver = False
while not GameOver:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        GameOver = True
        
        estadoTecla = pg.key.get_pressed()

        pantalla.fill(blanco)
        
        ahoraEnemigo = pg.time.get_ticks()
        if ahoraEnemigo - ultimoRespawn > tiempoRespawn:
                for x in range(10):
                        enemigo = Enemigo1()
                        enemigosSprites.add(enemigo)
                        ultimoRespawn = ahoraEnemigo
                                
        
        #CREACIÓN DE COLISIONES
        colisionBalaYEnemigo = pg.sprite.groupcollide(balasJugadorSprites, enemigosSprites, True, True)
        colisionJugadorYEnemigo = pg.sprite.groupcollide(jugadorSprite, enemigosSprites, True, False)
        
        if colisionBalaYEnemigo:
                jugador.experienciaActual += 10
                jugador.puntuacion += 20
                jugador.eliminaciones += 1
        
        if colisionJugadorYEnemigo:
                GameOver = True
                


        #ACTUALIZACIÓN DE SPRITES
        jugadorSprite.update()
        balasJugadorSprites.update()
        enemigosSprites.update()

        #DIBUJO DE LOS SPRITES
        balasJugadorSprites.draw(pantalla)
        jugadorSprite.draw(pantalla)
        enemigosSprites.draw(pantalla)

        pg.display.flip()
        clock.tick(60)

conexion.consultarPuntuaciones()
fechaFinal = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")


while jugador.nombre == "" or len(jugador.nombre) > 5:
        jugador.nombre = input("Ingresar nombre (Máximo 5 carácteres): ")
        if jugador.nombre == "" or len(jugador.nombre) > 5:
                print("Nombre no válido")

print(f"""
Nombre: {jugador.nombre}
Eliminaciones: {jugador.eliminaciones}
Puntuación final: {jugador.puntuacion}
Fecha: {fechaFinal}
""")

enviar = ""
while enviar != "s" and enviar != "n":
        enviar = input("¿Enviar?(s/n)\n")
        
if enviar == "s":
        conexion.enviarPuntuacion()
if enviar == "n":
        input("Puntuación no enviada")

