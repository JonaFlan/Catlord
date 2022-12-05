import pygame as pg
import mysql.connector as sql
import random
import datetime

class Conexion():
        def __init__(self):
                #self.db = sql.connect(user = "remoto", passwd = "remoto", host = "3.213.130.86", database = "catlorddb", port = "3306")
                self.db = sql.connect(user = "root", passwd = "root", host = "localhost", database = "catlorddb", port = "3306")
                self.cursor = self.db.cursor()
                self.accion = ""
                self.valor = ""
                self.resultado = ""

        def enviarPuntuacion(self):
                self.accion = ("insert into puntuacion (nombre, eliminaciones, puntuacion, fecha) values (%s,%s,%s,%s)")
                self.valor = (jugador.nombre, jugador.eliminaciones, jugador.puntuacion, menu.fechaFinal)
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

class Menu():
        def __init__(self):
                self.inicio = 0
                self.opcion1 = 0
                self.opcionBorrar = 0
                self.opcionCambiar = 0

        def mostrarMenuPrincipal(self):
                while self.inicio != 1:
                        self.inicio = int(input("1) Iniciar juego || 2) Puntuaciones \n"))
                        if self.inicio == 2:
                                conexion.consultarPuntuaciones()
                                self.opcion1 = int(input("1) Eliminar registro || 2) Editar nombre || 3) Volver \n"))
                                while self.opcion1 == 1: 
                                        conexion.consultarPuntuaciones()
                                        self.opcionBorrar = int(input("Seleccionar registro: "))
                                        for x in range(len(conexion.resultado)):
                                                if conexion.resultado[x][0] == self.opcionBorrar:
                                                        conexion.eliminarPuntuacion(conexion.resultado[x][0])
                                        eleccion = int(input("1) Continuar || 2) Volver\n"))
                                        if eleccion == 2:
                                                self.opcion1 = 0
                                                        
                                while self.opcion1 == 2:
                                        conexion.consultarPuntuaciones()
                                        self.opcionCambiar = int(input("Seleccionar registro: "))
                                        for x in range(len(conexion.resultado)):
                                                if conexion.resultado[x][0] == self.opcionCambiar:
                                                        nombre = ""
                                                        while nombre == "" or len(nombre) > 5:
                                                                nombre = input("Ingresar nuevo nombre (Máximo 5 carácteres): ")
                                                                if nombre == "" or len(nombre) > 5:
                                                                        print("Nombre no válido")
                                                        conexion.cambiarNombre(conexion.resultado[x][0], nombre)
                                        eleccion = int(input("1) Continuar || 2) Volver\n"))
                                        if eleccion == 2:
                                                self.opcion1 = 0
        
        def mostrarMenuFinal(self):
                self.fechaFinal = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                self.enviar = ""


                while jugador.nombre == "" or len(jugador.nombre) > 5:
                        jugador.nombre = input("Ingresar nombre (Máximo 5 carácteres): ")
                        if jugador.nombre == "" or len(jugador.nombre) > 5:
                                print("Nombre no válido")

                print(f"""
Nombre: {jugador.nombre}
Eliminaciones: {jugador.eliminaciones}
Puntuación final: {jugador.puntuacion}
Fecha: {self.fechaFinal}
""")

                while self.enviar != "s" and self.enviar != "n":
                        self.enviar = input("¿Enviar?(s/n)\n")
                        
                if self.enviar == "s":
                        conexion.enviarPuntuacion()
                if self.enviar == "n":
                        input("Puntuación no enviada")

class Principal():
        def __init__(self):
                #INICIALIZAR PYGAME Y LA CARGA DE AUDIO
                pg.init()
                pg.mixer.init()

                #GRUPOS DE SPIRITES
                self.jugadorSprite = pg.sprite.Group()
                self.enemigosSprites = pg.sprite.Group()
                self.balasJugadorSprites = pg.sprite.Group()

                #CONFIGURACIÓN BÁSICA DE LA VENTANA
                self.clock = pg.time.Clock()
                pg.display.set_caption("Catlord 0.2")
                self.tamañoVentana = self.ancho, self.alto = 1920, 1080
                self.pantalla = pg.display.set_mode(self.tamañoVentana)
                self.fondo = pg.image.load("cielo.png").convert()

                #PARÁMETROS DE REAPARICIÓN DE ENEMIGOS
                self.tiempoRespawn = 1500
                self.ultimoRespawn = pg.time.get_ticks()

                

        def bucleJuego(self):
                self.gameOver = False
                while not self.gameOver:
                        for event in pg.event.get():
                                if event.type == pg.QUIT:
                                        self.gameOver = True
                        
                        self.estadoTecla = pg.key.get_pressed()
                        
                        ahoraEnemigo = pg.time.get_ticks()
                        if ahoraEnemigo - self.ultimoRespawn > self.tiempoRespawn:
                                for x in range(10):
                                        enemigo = Enemigo1()
                                        self.enemigosSprites.add(enemigo)
                                        self.ultimoRespawn = ahoraEnemigo
                                                
                        
                        #COLISIONES
                        self.colisionBalaYEnemigo = pg.sprite.groupcollide(self.balasJugadorSprites, self.enemigosSprites, True, True)
                        self.colisionJugadorYEnemigo = pg.sprite.groupcollide(self.jugadorSprite, self.enemigosSprites, True, False)
                        
                        if self.colisionBalaYEnemigo:
                                jugador.experienciaActual += 10
                                jugador.puntuacion += 20
                                jugador.eliminaciones += 1
                        
                        if self.colisionJugadorYEnemigo:
                                self.gameOver = True

                        #FONDO DE PANTALLA
                        self.pantalla.blit(self.fondo, (0,0))

                        #ACTUALIZACIÓN DE SPRITES
                        self.jugadorSprite.update()
                        self.balasJugadorSprites.update()
                        self.enemigosSprites.update()

                        #DIBUJO DE LOS SPRITES
                        self.balasJugadorSprites.draw(self.pantalla)
                        self.jugadorSprite.draw(self.pantalla)
                        self.enemigosSprites.draw(self.pantalla)

                        pg.display.flip()
                        self.clock.tick(60)
        
class Jugador(pg.sprite.Sprite):
        def __init__(self):
                #ATRIBUTOS BÁSICOS
                super().__init__()
                #SPRITES DEL JUGADOR
                self.willyBase = pg.image.load("willyCachorro.png")
                self.willyRugido = pg.image.load("willyCachorroRugido.png")
                self.willyBase2 = pg.image.load("caraWilly.png")
                self.willyRugido2 = pg.image.load("willyRugido.png")
                
                self.image = self.willyBase
                self.rect = self.image.get_rect()
                self.rect.centerx = principal.ancho//2
                self.rect.centery = principal.alto//2
                self.vel_x = 5
                self.vel_y = 5
                self.sonidoParry2 = pg.mixer.Sound("rugidoWilly.ogg")
                self.sonidoParry = pg.mixer.Sound("rugidoWillyCachorro.ogg")
                self.duracionCambio = 100
                self.cadenciaDisparo = 750
                self.cadenciaParry = 1000
                self.ultimoDisparo = pg.time.get_ticks()
                self.ultimoParry = pg.time.get_ticks()
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
                if principal.estadoTecla[pg.K_w]:
                        self.vel_y = -5
                        self.rect[1] += self.vel_y
                #MOVER IZQUIERDA
                if principal.estadoTecla[pg.K_a]:
                        self.vel_x = -5
                        self.rect[0] += self.vel_x
                #MOVER ABAJO
                if principal.estadoTecla[pg.K_s]:
                        self.vel_y = 5
                        self.rect[1] += self.vel_y
                #MOVER DERECHA
                if principal.estadoTecla[pg.K_d]:
                        self.vel_x = 5
                        self.rect[0] += self.vel_x
                #LIMITES DE MOVIMIENTO
                if self.rect.left < 0:
                        self.rect.left = 0
                if self.rect.right > principal.ancho:
                        self.rect.right = principal.ancho
                if self.rect.top < 0:
                        self.rect.top = 0
                if self.rect.bottom > principal.alto:
                        self.rect.bottom = principal.alto
                
                #DISPARO DEL JUGADOR
                if principal.estadoTecla[pg.K_UP]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimoDisparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = -10)
                                principal.balasJugadorSprites.add(bala)
                                self.ultimoDisparo = ahora
                
                if principal.estadoTecla[pg.K_LEFT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimoDisparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = -10)
                                principal.balasJugadorSprites.add(bala)
                                self.ultimoDisparo = ahora
                
                if principal.estadoTecla[pg.K_DOWN]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimoDisparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_y = 10)
                                principal.balasJugadorSprites.add(bala)
                                self.ultimoDisparo = ahora
                
                if principal.estadoTecla[pg.K_RIGHT]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimoDisparo > self.cadenciaDisparo:
                                bala = Bala(self.rect.centerx, self.rect.centery, vel_x = 10)
                                principal.balasJugadorSprites.add(bala)
                                self.ultimoDisparo = ahora
                
                if principal.estadoTecla[pg.K_SPACE]:
                        ahora = pg.time.get_ticks()
                        if ahora - self.ultimoParry > self.cadenciaParry:
                                if self.nivelActual < 3:
                                        self.sonidoParry.play()
                                        self.lanzamiento = pg.time.get_ticks()
                                        self.image = self.willyRugido
                                        parry = Parry(self.rect.centerx, self.rect.centery, ahora)
                                        principal.balasJugadorSprites.add(parry)
                                        self.ultimoParry = ahora
                                elif self.nivelActual >= 3:
                                        self.sonidoParry2.play()
                                        self.lanzamiento = pg.time.get_ticks()
                                        self.image = self.willyRugido2
                                        parry = Parry(self.rect.centerx, self.rect.centery, ahora)
                                        principal.balasJugadorSprites.add(parry)
                                        self.ultimoParry = ahora
                
                self.contador = pg.time.get_ticks()
                try:
                        if self.contador - self.lanzamiento > self.duracionCambio:
                                if self.nivelActual < 3:
                                        self.image = self.willyBase
                                elif self.nivelActual >= 3:
                                        self.image = self.willyBase2
                except:
                        pass
                
                #SUBIR DE NIVEL
                if self.experienciaActual >= self.experienciaMaxima:
                        self.nivelActual += 1
                        self.experienciaActual = 0
                        self.experienciaMaxima *= 1.5
                        self.cadenciaDisparo  *= 0.8

class Bala(pg.sprite.Sprite):
        def __init__(self,x, y, vel_x = 0, vel_y = 0):
                super().__init__()
                self.image = pg.image.load("bala2.png")
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.y = y
                self.vel_x = vel_x
                self.vel_y = vel_y
                self.daño = 1

        def update(self):
                self.rect[0] += self.vel_x
                self.rect[1] += self.vel_y
                if self.rect.bottom < 0 or self.rect.top > principal.alto or self.rect.right < 0 or self.rect.left > principal.ancho:
                        self.kill()

class Parry(pg.sprite.Sprite):
        def __init__(self,x, y, lanzamiento):
                super().__init__()
                self.escudo = pg.image.load("escudo.png")
                self.escudo2 = pg.image.load("escudo2.png")
                self.image = self.escudo
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.centery = y
                self.daño = 1
                self.lanzamiento = lanzamiento
                self.duracion = 100

        def update(self):
                self.rect.centerx = jugador.rect.centerx
                self.rect.centery = jugador.rect.centery
                self.contador = pg.time.get_ticks()
                if self.contador - self.lanzamiento > self.duracion:
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
                        self.rect.centerx = random.randrange(principal.ancho)
                        self.rect.centery = random.randrange(-150, 0)
                        self.vel_x = 0
                        self.vel_y = 5
                #SPAWN IZQUIERDA 
                elif self.respawn == 2:
                        self.rect.centerx = random.randrange(-150, 0)
                        self.rect.centery = random.randrange(principal.alto)
                        self.vel_x = 5
                        self.vel_y = 0
                #SPAWN ABAJO
                elif self.respawn == 3:
                        self.rect.centerx = random.randrange(principal.ancho)
                        self.rect.centery = random.randrange(principal.alto, principal.alto + 150)
                        self.vel_x = 0
                        self.vel_y = -5
                #SPAWN DERECHA
                elif self.respawn == 4:
                        self.rect.centerx = random.randrange(principal.ancho, principal.ancho +150)
                        self.rect.centery = random.randrange(principal.alto)
                        self.vel_x = -5
                        self.vel_y = 0
                self.vida = 2
        
        def update(self):
                self.rect[0] += self.vel_x
                self.rect[1] += self.vel_y
                if self.rect.top >= principal.alto + 150 or self.rect.left >= principal.ancho + 150 or self.rect.bottom <= -150 or self.rect.right <= -150:
                        self.kill()

#CREACIÓN DE OBJETOS
principal = Principal()
menu = Menu()
conexion = Conexion()
jugador = Jugador()
principal.jugadorSprite.add(jugador)

#JUEGO
menu.mostrarMenuPrincipal()
principal.bucleJuego()
conexion.consultarPuntuaciones()
menu.mostrarMenuFinal()



