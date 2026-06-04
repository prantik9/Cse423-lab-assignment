from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# window size
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 600

# rain state
drops_arr = [(random.randint(-250, 250), random.randint(-250, 250)) for _ in range(100)] 
tilt = 0        
tilt_angle = 0  
day = 3

def draw_shapes():
    # ghasher square
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)
    glVertex2d(-500, 40)
    glColor3f(0, 1, 0)
    glVertex2d(-500, -250)
    glColor3f(0, 1, 0)
    glVertex2d(500, -250)
    glColor3f(0, 1, 0)
    glVertex2d(500, 40)
    glEnd()     
    # chalar triangle
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 1)
    glVertex2d(0, 60)
    glColor3f(1, 0, 1)
    glVertex2d(-100, 0)
    glColor3f(1, 0, 1)
    glVertex2d(100, 0)
    glEnd()
    # ghorer square
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex2d(90, 0)
    glColor3f(1, 1, 1)
    glVertex2d(-90, 0)
    glColor3f(1, 1, 1)
    glVertex2d(-90, -140)
    glColor3f(1, 1, 1)
    glVertex2d(90, -140)
    glEnd()   
    # dorja
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)
    glVertex2d(15, -140)
    glColor3f(0, 0, 1)
    glVertex2d(15,-50)
    glColor3f(0, 0, 1)
    glVertex2d(-15, -50)
    glColor3f(0, 0, 1)
    glVertex2d(-15, -140)
    glEnd()   
    # bam janala
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)
    glVertex2d(-35, -50)
    glColor3f(0, 0, 1)
    glVertex2d(-60,-50)
    glColor3f(0, 0, 1)
    glVertex2d(-60, -80)
    glColor3f(0, 0, 1)
    glVertex2d(-35, -80)
    glEnd()   
   # dan janala
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)
    glVertex2d(35, -50)
    glColor3f(0, 0, 1)
    glVertex2d(60,-50)
    glColor3f(0, 0, 1)
    glVertex2d(60, -80)
    glColor3f(0, 0, 1)
    glVertex2d(35, -80)
    glEnd()  


def draw_background():

    global day

    colors = [
        (0, 0, 0),  
        (0.3, 0.3, 0.3),  
        (0.6, 0.6, 0.6),  
        (1.0, 1.0, 1.0)  
    ] # for day/night shades

    # current day color
    glBegin(GL_QUADS)
    glColor3f(*colors[day])
    glVertex2f(-250, 250)
    glVertex2f(250, 250)
    glVertex2f(250, -250)
    glVertex2f(-250, -250)
    glEnd()

def draw_rain():
    global drops_arr, tilt_angle, tilt
    import math
    # compute horizontal offset based on angle; tan(45°)=1 yields offset 20
    tilt = math.tan(math.radians(tilt_angle)) * 20

    glColor3f(0.6, 0.6, 1.0)
    glBegin(GL_LINES)
    for i in range(len(drops_arr)):
        p, q = drops_arr[i]
        glVertex2f(p, q)
        glVertex2f(p + tilt, q - 20)

        drops_arr[i] = (p, q - 0.2)  # speed
        if q - 5 < -250:
            drops_arr[i] = (random.randint(-250, 250), 250)
    glEnd()

def animateRain():
    glutPostRedisplay()



def display():
    glClear(GL_COLOR_BUFFER_BIT )
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    draw_background()
    draw_shapes()
    draw_rain()

    glutSwapBuffers()



def special(key, x, y):
    global tilt_angle
    # adjust angle in 5° increments
    if key == GLUT_KEY_LEFT:
        if tilt_angle > -45:
            tilt_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        if tilt_angle < 45:
            tilt_angle += 5
    glutPostRedisplay()


def keyboard(key, x, y):
    global day 

    if key == b'd' and day < 3:  ## increase brightness
        day += 1
        print("It's Day Time. Light theme enabled!")
    elif key == b'n' and day > 0:  # decrease brightness
        day -= 1
        print("It's Night Time. Dark theme enabled!")

    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"House with Rain")
    glutDisplayFunc(display)
    glutSpecialFunc(special)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(animateRain)
    glutMainLoop()


if __name__ == '__main__':
    main()
