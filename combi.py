import pygame
import fractales
import inicio
import derrota
import victoria
from funciones.ball import Ball
from funciones.rectangle import Rectangle

# Para la visualización en 2D
from OpenGL.GL import *
from OpenGL.GLU import *


# Dimensiones de la ventana del juego 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def main():
    # mostrar la pantalla de bienvenida
    inicio.show_welcome_screen()
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)  # Definir el sistema de coordenadas
    # establecer el titulo de la ventana 
    pygame.display.set_caption("Brick Breacker")

    # caracteristicas del rectángulo
    color_rectangle = (1, 1, 1)     # color blanco
    rectangle = Rectangle(350, 0, 100, 20, color_rectangle)

    # lista de posiciones para los ladrillos
    all_position = fractales.gen_positions()

    # ladrillos 
    squares_nivel1 = [] # se rompen de 1 golpe
    squares_nivel2 = [] # se rompen de 2 golpe

 #  for ele in all_position :
 #     print(ele[0],ele[1])


    all_position2 = list(all_position)
    mitad = len(all_position2) // 2
    
    # Para los ladrillos del nivel 1
    color1 =  (0, 1, 0)      # color verde

    for ele in all_position2[:mitad] : 
        squares_nivel1.append(Rectangle(ele[0], ele[1], 20, 20,color1))

    # Para los ladrillos del nivel 2
    color2 = (1, 1, 0)      # color amarillo

    for ele in all_position2[mitad:] : 
        squares_nivel2.append(Rectangle(ele[0], ele[1], 20, 20,color2))
    
    golpes_cuadrados_nivel2 = [2] * mitad

    #squares = [Rectangle(200, 200, 50, 50), Rectangle(500, 200, 50, 50)]

    # Características de la pelota
    color_ball = (1, 0, 0) 
    ball = Ball(400, 37, 15, color_ball)
    ball.speed_x = 0
    ball.speed_y = 0

    # Vida de las pelotas
    lifes = []
    color_life = (148, 0, 211) 
    lifes.append(Ball(750, 550, 15, color_life))
    lifes.append(Ball(700, 550, 15, color_life))
    lifes.append(Ball(650, 550, 15, color_life))

    game_started = False

    # Ciclo principal del juego
    while True:
        i = -1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    game_started = True
                    ball.speed_x = 0.6
                    ball.speed_y = 0.6

            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT)

        
        # Movimiento del rectángulo
        keys = pygame.key.get_pressed()

        # Movimiento de la bola
        ball.move(WINDOW_HEIGHT, WINDOW_WIDTH)
        

        if not game_started:

            if keys[pygame.K_LEFT] and rectangle.x >0:
                rectangle.x -= 2
                ball.x -= 2

            if keys[pygame.K_RIGHT] and rectangle.x < 700:
                rectangle.x += 2
                ball.x += 2


        if game_started:

            if keys[pygame.K_LEFT] and rectangle.x >0:
                rectangle.x -= 2

            if keys[pygame.K_RIGHT] and rectangle.x < 700:
                rectangle.x += 2

            # Colisiones entre la bola y el rectángulo
            if ball.collides_with_rectangle(rectangle):
                #print(len(squares))
                ball.speed_y *= -1

            # Colisiones entre la bola y los ladrillos nivel 1
            for square in squares_nivel1:
                if ball.collides_with_rectangle(square):
                    #print("tocaste cuadrado level 1")
                    squares_nivel1.remove(square)
                    ball.speed_y *= -1
                    ball.speed_x *= -1

            # Colisiones entre la bola y los ladrillos nivel 2
            for square in squares_nivel2:
                i+=1           
                if ball.collides_with_rectangle(square):
                    square.change_color(color1)
                    golpes_cuadrados_nivel2[i] -= 1
                    ball.speed_y *= -1
                    ball.speed_x *= -1
                    #print("tocaste cuadrado nivel 2: ",i)
                    if golpes_cuadrados_nivel2[i] == 0:
                        squares_nivel2.remove(square)
                        #print("Rompiste cuadrado nivel 2: ",i)

            # Si la pelota colisiona con el suelo
            if ball.collide_with_floor():
                ball.life -= 1
                ball.x = 400
                ball.y = 37
                ball.speed_x = 0
                ball.speed_y = 0
                rectangle.x = 350
                # print( ball.life)
                if ball.life == 0 :
                    derrota.show_welcome_screen()
                else:
                    game_started = False
                    lifes.pop()

            # Si los ladrillos son cero 
            if len(squares_nivel1 + squares_nivel2 ) == 0:
                victoria.show_welcome_screen()

        # Dibujar el rectángulo
        rectangle.draw()

        # Dibujar los cuadrados
        for square in squares_nivel1 + squares_nivel2:
            square.draw()

        # Dibujar la bola
        ball.draw()

        # Dibujar las vidas
        for life in lifes:
            life.draw()

        pygame.display.flip()

if __name__ == '__main__':
    main()

