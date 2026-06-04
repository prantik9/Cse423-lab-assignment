from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rand
import time as t

play = True
cat_x = 250
diamonds_x = 250
diamonds_y = 500
diamonds_r = 0.0
diamonds_g = 0.0
diamonds_b = 0.0
prev_time = 0
velocity = -100
score = 0
game_over = False
cheat_mode = False
base_velocity = -100

        
def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy < 0:
            return 7
        elif dx < 0 and dy >= 0:
            return 3
        else:
            return 4
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx >= 0 and dy < 0:
            return 6
        elif dx < 0 and dy >= 0:
            return 2
        else:
            return 5


def convert_to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def original_coordinates(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)

    x1, y1 = convert_to_zone_0(x1, y1, zone)
    x2, y2 = convert_to_zone_0(x2, y2, zone)
    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    e = 2*dy
    ne = 2*(dy-dx) 
    x = x1
    y = y1

    while x <= x2:
        ox, oy = original_coordinates(x, y, zone)
        draw_points(ox, oy)  

        if d <= 0:
            d += e
            x += 1
        else:
            d += ne
            y += 1
            x += 1


def diamond():
    global diamonds_x, diamonds_y, diamonds_r, diamonds_g, diamonds_b
    glColor3f(diamonds_r, diamonds_g, diamonds_b)
    draw_line(-20 + diamonds_x, diamonds_y ,   diamonds_x, -20 + diamonds_y)
    draw_line( diamonds_x, diamonds_y-20 , 20 + diamonds_x,  diamonds_y)
    draw_line(20 + diamonds_x,  diamonds_y,  diamonds_x, 20 + diamonds_y)
    draw_line( diamonds_x, 20 + diamonds_y, -20 + diamonds_x,  diamonds_y)

def catcher():
    global cat_x
    if game_over:
      glColor3f(1,0,0)
    else:
      glColor3f(1, 1, 1)
    draw_line(cat_x + 75, 10, cat_x - 75, 10)
    draw_line(cat_x + 100,35, cat_x - 100, 35)
    draw_line(cat_x - 75, 10, cat_x - 100, 35)
    draw_line(cat_x + 75, 10, cat_x + 100, 35)


def cheatmode():
    global cat_x, diamonds_x, cheat_mode
    
    if not cheat_mode:
        return
    
    if cat_x < diamonds_x - 5:
        cat_x = min(cat_x + 4, 400)
    elif cat_x > diamonds_x + 5:
        cat_x = max(cat_x - 4, 100)
    else:
        cat_x = diamonds_x  # same thakbe


def collision_check():
    global diamonds_x, diamonds_y, cat_x, score, velocity, diamonds_r, diamonds_g, diamonds_b
    global cheat_mode, base_velocity, game_over

    d_left = -20 + diamonds_x
    d_right = 20 + diamonds_x
    d_top = 20 + diamonds_y
    d_bottom = -20 + diamonds_y

    c_left = cat_x - 100
    c_right = cat_x + 100
    c_top = 30
    c_bottom = 10

    if d_right >= c_left and d_left <= c_right:
      if d_bottom <= c_top and d_bottom > c_bottom:
        score += 1
        print("Score: ", score)
        
        diamonds_y = 590  # reset to TOP 
        base_velocity = -100 - (score * 25)  # increases Gradually 
        velocity = base_velocity
        
        diamonds_r = rand.random()
        diamonds_g = rand.random()
        diamonds_b = rand.random()
        diamonds_x = rand.randint(30, 480)
        return True

    if diamonds_y <= 0:
        print("Game Over! Score: ", score)
        game_over = True
        return False    
    return False


def animate():
    global play, diamonds_y, velocity, prev_time, game_over, score

    if not play or game_over:
        return

    current_time = t.time()
    delta_time = current_time - prev_time
    prev_time = current_time

    cheatmode()
    velocity -= 5 * delta_time
    diamonds_y += velocity * delta_time 

    collision_check()

    glutPostRedisplay()


def pause():
    global play, prev_time
    prev_time = t.time()
    play = not play


def restart():
    global play, prev_time, velocity, diamonds_y, score, game_over
    global diamonds_r, diamonds_g, diamonds_b, diamonds_x, cat_x, cheat_mode, base_velocity

    cat_x = 250
    prev_time = t.time()
    velocity = -100
    base_velocity = -100
    diamonds_y = 590
    score = 0
    play = True
    game_over = False
    cheat_mode = False
    diamonds_r = rand.random()
    diamonds_g = rand.random()
    diamonds_b = rand.random()
    diamonds_x = rand.randint(20, 480)
    print("Starting Over")


def keyboard_handler(key, x, y):
    if key == b'c':
        global cheat_mode
        cheat_mode = not cheat_mode

def special_key_handler(key, x, y):
    global cat_x, play, game_over, cheat_mode

    if not play or game_over or cheat_mode:
        return
    if key == GLUT_KEY_LEFT:
            if cat_x > 100:
                cat_x -= 15

    elif key == GLUT_KEY_RIGHT:
            if cat_x < 400:
                cat_x += 15


def mouse_listener(button, state, x, y):
    global score, play
    gl_x = x
    gl_y = 700 - y
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 10 <= gl_x <= 50 and 650 <= gl_y <= 690:
            restart()
            print("Restarted!")
        elif 235 <= gl_x <= 265 and 650 <= gl_y <= 690:
            pause()
            print("Paused!" if not play else "Playing!")
        elif 460 <= gl_x <= 490 and 650 <= gl_y <= 690:
            print("Goodbye! Score: ", score)
            glutLeaveMainLoop()


def draw_ui():
    # left arrow
    glColor3f(0, 0.5, 0.5)
    draw_line(30, 690, 10, 670)
    draw_line(10, 670, 30, 650)
    draw_line(10, 670, 50, 670)

    # pause/play button
    glColor3f(1.0, 0.75, 0)
    if play:
        draw_line(240, 690, 240, 630)
        draw_line(260, 690, 260, 630)
    else:
        draw_line(240, 690, 240, 630)
        draw_line(240, 690, 270, 660)
        draw_line(270, 660, 240, 630)

    # quit cross
    glColor3f(1.0, 0, 0)
    draw_line(460, 690, 490, 650)
    draw_line(490, 690, 460, 650)


def setup_projection():
    glViewport(0, 0, 500, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    glColor3f(1.0, 1.0, 1.0)
    draw_ui()
    catcher()
    diamond()

    glutSwapBuffers()


def main():
    global prev_time, diamonds_r, diamonds_g, diamonds_b, diamonds_x

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(500, 700)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Catch diamonds!")

    prev_time = t.time()
    diamonds_r = rand.random()
    diamonds_g = rand.random()
    diamonds_b = rand.random()
    diamonds_x = rand.randint(20, 480)

    glutDisplayFunc(showScreen)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_handler)
    glutKeyboardFunc(keyboard_handler)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


if __name__ == '__main__':
    main()
