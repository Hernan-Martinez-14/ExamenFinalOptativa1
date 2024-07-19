import turtle  # La librería turtle ayuda a construir la interfaz gráfica
import time  # Para obtener el tiempo
import random  # Para usar números random
import pygame  # Para agregar sonido
from tkinter import messagebox, Tk

# Inicializar pygame
pygame.init()
comer_sonido = pygame.mixer.Sound('comiendo.wav')  # Asegúrate de tener un archivo 'comer.wav' en el mismo directorio
perder_sonido = pygame.mixer.Sound('perdiste.mp3')  # Asegúrate de tener un archivo 'perder.wav' en el mismo directorio
pygame.mixer.music.load('sonidofondo.mp3')  # Asegúrate de tener un archivo 'fondo.mp3' en el mismo directorio
pygame.mixer.music.play(-1)  # Reproduce el sonido de fondo en bucle

posponer = 0.1
puntaje = 0
maxPuntaje = 0

# Configuración
window = turtle.Screen()  # Crea una ventana nueva
window.title('Snake')  # Ponemos título
window.bgcolor('#000000')  # Color de fondo
window.setup(width=600, height=600)  # Redimensionar pantalla
window.tracer(0)  # Ayuda a hacer la animación más placentera

# Cabeza de la serpiente
cabeza = turtle.Turtle()  # Crea un objeto para mostrar en pantalla
cabeza.speed(0)  # Se muestra al iniciar
cabeza.shape('square')  # Se le asigna forma de círculo
cabeza.color('#0A2BF7')  # Color a la cabeza
cabeza.penup()  # Elimina el rastro del objeto
cabeza.goto(0, 0)  # Centra el objeto
cabeza.direction = 'stop'  # Asigna dirección, en este caso estático

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape('circle')
comida.color('#F7F702')
comida.penup()
comida.goto(0, 100)

# Texto para el puntaje
texto = turtle.Turtle()
texto.speed(0)
texto.color('white')
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write('Puntaje: 0     Máximo puntaje: 0', align='center', font=('Courier', 20, 'normal'))

# Cuerpo de la serpiente
cuerpo = []  # Una lista que almacena cada segmento
color_cuerpo = '#0A2BF7'  # Color uniforme para el cuerpo

# Funciones

def printText():
    global maxPuntaje
    if puntaje > maxPuntaje:
        maxPuntaje = puntaje
    texto.clear()
    texto.write(f'Puntaje: {puntaje}     Máximo puntaje: {maxPuntaje}', align='center', font=('Courier', 20, 'normal'))

def actualizar_velocidad():
    global posponer
    # Aumenta la velocidad cada 10 puntos
    if puntaje % 10 == 0 and puntaje > 0:
        posponer = max(0.05, posponer - 0.01)  # No permitir que la velocidad sea demasiado rápida

# Definir cada movimiento
def arriba():
    if cabeza.direction != 'down':
        cabeza.direction = 'up'

def abajo():
    if cabeza.direction != 'up':
        cabeza.direction = 'down'

def izquierda():
    if cabeza.direction != 'right':
        cabeza.direction = 'left'

def derecha():
    if cabeza.direction != 'left':
        cabeza.direction = 'right'

# Ejecuta el movimiento
def movimiento():
    if cabeza.direction == 'up':  # Si la dirección es hacia arriba
        y = cabeza.ycor()  # Obtiene la coordenada Y
        cabeza.sety(y + 20)  # Actualiza la posición Y

    elif cabeza.direction == 'down':
        y = cabeza.ycor()  # Obtiene la coordenada Y
        cabeza.sety(y - 20)

    elif cabeza.direction == 'left':
        x = cabeza.xcor()  # Obtiene la coordenada X
        cabeza.setx(x - 20)

    elif cabeza.direction == 'right':
        x = cabeza.xcor()  # Obtiene la coordenada X
        cabeza.setx(x + 20)

# Creación del cuerpo
def crearSegmento():
    global puntaje
    segmento = turtle.Turtle()
    segmento.speed(0)
    segmento.shape('square')  # Cambiar a forma de círculo
    segmento.color(color_cuerpo)  # Mismo color que la cabeza
    segmento.penup()
    cuerpo.append(segmento)
    puntaje += 1
    printText()
    actualizar_velocidad()  # Ajustar velocidad según el puntaje

# Colisión con la comida
def colisionComida():
    if cabeza.distance(comida) < 20:  # Se mira la distancia entre la cabeza y la comida
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)  # Se actualiza la posición de la comida a un random
        crearSegmento()
        pygame.mixer.Sound.play(comer_sonido)  # Reproduce el sonido

# Mover el cuerpo
def movCuerpo():
    totalSeg = len(cuerpo)

    # Cada elemento sigue al anterior, excepto el primero
    for segmento in range(totalSeg - 1, 0, -1):  # Va desde el último segmento hasta el primero
        x = cuerpo[segmento - 1].xcor()  # Detecta las coordenadas del elemento anterior
        y = cuerpo[segmento - 1].ycor()
        cuerpo[segmento].goto(x, y)  # Se dirige a la posición del elemento anterior

    if totalSeg > 0:  # Debe haber al menos un elemento para que este siga a la cabeza
        x = cabeza.xcor()
        y = cabeza.ycor()
        cuerpo[0].goto(x, y)

# Colisión con el borde
def borde():
    global puntaje
    if cabeza.xcor() < -280 or cabeza.xcor() > 280 or cabeza.ycor() < -280 or cabeza.ycor() > 280:
        resetGame()

# Colisión con el propio cuerpo
def mordida():
    for segmento in cuerpo:
        if segmento.distance(cabeza) < 20:
            resetGame()

def resetGame():
    global puntaje
    pygame.mixer.Sound.play(perder_sonido)  # Reproduce el sonido de perder
    time.sleep(0.5)
    cabeza.goto(0, 0)
    cabeza.direction = 'stop'
    for segmento in cuerpo:  # Esconde los segmentos
        segmento.goto(1000, 1000)
    cuerpo.clear()  # Limpia la lista
    puntaje = 0
    printText()
    preguntar_jugar_nuevamente()

def preguntar_jugar_nuevamente():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    respuesta = messagebox.askyesno("Game Over", "¿Quieres jugar de nuevo?")
    root.destroy()  # Destruir la ventana principal de Tkinter
    if respuesta:
        reiniciar_juego()
    else:
        window.bye()  # Cierra la ventana de Turtle

def reiniciar_juego():
    global puntaje, cabeza, comida, cuerpo

    puntaje = 0
    cabeza.goto(0, 0)
    cabeza.direction = 'stop'
    for segmento in cuerpo:
        segmento.goto(1000, 1000)
    cuerpo.clear()
    comida.goto(0, 100)
    printText()

# Conexión con teclado
window.listen()  # Está pendiente si se oprime una tecla
window.onkeypress(arriba, 'Up')  # Ejecuta la función arriba() cuando detecta 'Up'
window.onkeypress(abajo, 'Down')
window.onkeypress(izquierda, 'Left')
window.onkeypress(derecha, 'Right')

# Ciclo permanente
while True:
    window.update()  # Actualizar la pantalla

    borde()
    colisionComida()  # Función que se ejecuta cuando toca la comida
    mordida()
    movCuerpo()  # Agrega movimiento al cuerpo
    movimiento()  # Hace el respectivo movimiento con las teclas

    time.sleep(posponer)  # Hace que se posponga por el tiempo establecido
