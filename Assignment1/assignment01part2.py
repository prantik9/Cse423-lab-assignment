from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import threading


W_Width, W_Height = 500, 500
flag = True  #chk animation func run or not
blink = False
blink_timer = None
balls = []
speed =  1
ball_size = random.randint(6, 10)


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class eBall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        self.dx = direction[0] * speed
        self.dy = direction[1] * speed
        self.size = random.randint(6, 10)
        self.previous_color = None
        self.color = (random.random(), random.random(), random.random()) #random color
        

def coordinates_convert(x, y):
    global W_Width, W_Height
    p = x - (W_Width / 2)
    q = (W_Height / 2) - y
    return p, q

def draw_ball(ball):
    glPointSize(ball.size)
    glBegin(GL_POINTS)
    glColor3f(ball.color[0], ball.color[1], ball.color[2])
    glVertex2f(ball.x, ball.y)
    glEnd()

def keyboardListener(key, x, y):
    global ball_size
    if key == b" ":
        #use space 
        global flag
        if flag == True:
            flag = False
            print("balls are paused")
        else:
            flag = True
            print("resumed animation")
    glutPostRedisplay()
def schedule_blink(delay, value):
    global blink_timer
    if blink_timer:
        blink_timer.cancel()
    blink_timer = threading.Timer(delay, toggle_blink, args=(value,))
    blink_timer.start()


def toggle_blink(value):
    global blink, blink_timer
    if not blink:
        # blinking off cancel timer & restore colors
        if blink_timer:
            blink_timer.cancel()
            blink_timer = None
        for i in balls:
            if i.previous_color:
                i.color = i.previous_color
        glutPostRedisplay()
        return

    if value == 0:
        for i in balls:
            i.previous_color = i.color
            i.color = (0, 0, 0)
        # next  flip after 1 second
        schedule_blink(1.0, 1)
    elif value == 1:
        for i in balls:
            i.color = i.previous_color
        if blink:
            schedule_blink(1.0, 0)
    glutPostRedisplay()
def specialKeyListener(key, x, y):
    global flag, speed
    if flag == False:
        print("paused")
        return
    if key == GLUT_KEY_UP:
        speed += 1
        for i in balls:
            i.dx = (i.dx/abs(i.dx)) * speed
            i.dy = (i.dy/abs(i.dy)) * speed
        print(f"Speed increased, current speed: {speed}")
    
    if key == GLUT_KEY_DOWN:
        speed -= 0.5
        if speed < 0:
            speed = 5
            print(f"Speed low, new speed: {speed}")     
        else:
            for i in balls:
                i.dx = (i.dx / abs(i.dx)) * speed
                i.dy = (i.dy / abs(i.dy)) * speed
            print(f"Speed decreased to {speed}")
            

def mouseListener(button, state, x, y):
    global flag
    global speed
    global blink

    if not flag:
        print("paused, no action")
        return
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print(x, y)
        converted_x, converted_y = coordinates_convert(x, y)
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        new_ball = eBall(converted_x, converted_y)    
        new_ball.dx = direction[0] * speed
        new_ball.dy = direction[1] * speed
        balls.append(new_ball)
    glutPostRedisplay()

    if button == GLUT_LEFT_BUTTON: 
        if state == GLUT_DOWN:
            blink = True
            #  blink immediately
            toggle_blink(0)
        elif state == GLUT_UP:
            blink = False
            toggle_blink(0)
        
        print(f"Blinking state: {blink}")
    glutPostRedisplay()

def scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    for i in balls:
        draw_ball(i)
    glutSwapBuffers()

def animate_balls():
    glutPostRedisplay()
    global flag
    if flag  == False:
        return
    for i in balls:
        i.x += i.dx
        i.y += i.dy
        if i.x <= -W_Width / 2 or i.x >= W_Width / 2: 
            i.dx = -i.dx
        if i.y <= -W_Height / 2 or i.y >= W_Height / 2: 
            i.dy = -i.dy

def display():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(100, 150)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

window = glutCreateWindow(b"lab1task2")
display()

glutDisplayFunc(scene)
glutIdleFunc(animate_balls)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()