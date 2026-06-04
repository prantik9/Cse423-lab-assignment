from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
a = 0
enm = 5
group = []
fires_bullet = False
guli = []
score = 0
life = 5
bm = 0
cam_pos = (0,800,600)
cam_tar = (0,0,0)
pcam_pos = cam_pos
fovY = 120
flag = False
cx = 0
cy = 0
dead = False
cheating = False
fp_pos = (0, 0, 0)
freeze = False
fp_tar = (0,0,0)
for _ in range(enm):
    group.append({"x": random.randint(-960, 960),
        "y": random.randint(-960, 960),
        "p" : 0,
        "pd" : 1,
        "finished" : False 
    })
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1600, 0, 900)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def draw_shooter():
    global  a, dead, cx, cy
    if not dead:
        glPushMatrix()
        glTranslatef(cx, cy, 0) 
        glRotatef(a, 0, 0, 1)
        glColor3f(0.294, 0.325, 0.125) #body 
        glTranslatef(0, 0, 50)  
        glutSolidCube(40)
        glTranslatef(0, 0, 40)  
        glutSolidCube(40)
        glColor3f(0, 0, 1) #legs
        glTranslatef(20, 0, -120) #r
        gluCylinder(gluNewQuadric(), 6.5, 13, 60, 10, 10)
        glTranslatef(-40, 0, 0) #l
        gluCylinder(gluNewQuadric(), 6.5, 13, 60, 10, 10)
        glColor3f(0, 0, 0) #head
        glTranslatef(20, 0, 160) 
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glColor3f(0.60, 0.60, 0.60) #gun
        glTranslatef(0, -20, -35) 
        glRotatef(90, 1, 0, 0)  
        gluCylinder(gluNewQuadric(), 13, 6, 80, 10, 10) 
        glColor3f(0.76, 0.57, 0.42) #arm
        glTranslatef(25, 0, 0)
        gluCylinder(gluNewQuadric(), 13, 6, 40, 10, 10)
        glTranslatef(-50, 0, 0)
        gluCylinder(gluNewQuadric(), 13, 6, 40, 10, 10)
        glPopMatrix()
    else:
        glPushMatrix()
        glTranslatef(cx, cy, 0)
        glRotatef(a, 0, 0, 1)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.294, 0.325, 0.125)
        glTranslatef(0, 0, 50)  
        glutSolidCube(40)
        glTranslatef(0, 0, 40)  
        glutSolidCube(40)
        glColor3f(0, 0, 1)
        glTranslatef(20, 0, -120)
        gluCylinder(gluNewQuadric(), 6.5, 13, 60, 10, 10)
        glTranslatef(-40, 0, 0)
        gluCylinder(gluNewQuadric(), 6.5, 13, 60, 10, 10)
        glColor3f(0, 0, 0)
        glTranslatef(20, 0, 160) 
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glColor3f(0.60, 0.60, 0.60)
        glTranslatef(0, -20, -35) 
        glRotatef(90, 1, 0, 0)  
        gluCylinder(gluNewQuadric(), 13, 6, 80, 10, 10) 
        glColor3f(0.76, 0.57, 0.42)
        glTranslatef(25, 0, 0)
        gluCylinder(gluNewQuadric(), 13, 6, 40, 10, 10)
        glTranslatef(-50, 0, 0)
        gluCylinder(gluNewQuadric(), 13, 6, 40, 10, 10)
        glPopMatrix()
def draw_enemy(enm):
    global cx, cy
    glPushMatrix()
    glTranslatef(enm["x"], enm["y"], 0)
    ps = 40 + enm["p"]
    glColor3f(1, 0, 0) #body
    glTranslatef(0, 0, ps)
    gluSphere(gluNewQuadric(), ps, 20, 20)
    glColor3f(0, 0, 0) #head
    glTranslatef(0, 0, ps + 25)
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()
def fire():
    global guli, cx, cy, a, fires_bullet
    r = math.radians(a)
    bx = cx + math.sin(r) * 25
    by = cy - math.cos(r) * 25
    disx = math.sin(r)
    disy = -math.cos(r)
    guli.append({"x": bx,
        "y": by,
        "z": 95,
        "disx": disx,
        "disy": disy,
        "speed": 5
    })
    fires_bullet = False
def draw_bullets():
    global guli
    glColor3f(0.6, 0.5, 0.4)
    for b in guli:
        glPushMatrix()
        glTranslatef(b["x"], b["y"], b["z"])
        glutSolidCube(6)
        glPopMatrix()
def guli_going():
    global guli, group, bm, score, fires_bullet
    nguli = []
    for b in guli:
        b["x"] += b["disx"] * b["speed"]
        b["y"] += b["disy"] * b["speed"]
        if not (-975 <= b["x"] <= 975 and -975 <= b["y"] <= 975): #boundary
            bm += 1
            print(f"Bullet Missed: {bm}")
            continue
        hvill = False
        for enm in group:
            dist = math.hypot(b["x"] - enm["x"], b["y"] - enm["y"])
            if dist < 40:
                hvill = True
                enm["x"] = random.randint(-960, 960)
                enm["y"] = random.randint(-960, 960)
                enm["p"] = 0
                enm["pd"] = 1
                score += 1
                break
        if not hvill:
            nguli.append(b)
    guli[:] = nguli
def fp():
    global cam_pos, cam_tar, dead, pcam_pos, fp_pos, fp_tar, freeze, flag, a, cx, cy
    if not dead:
        if flag:
            if not freeze:
                r = math.radians(a)
                lx = cx + math.sin(r) * 50
                ly = cy - math.cos(r) * 50
                cam_pos = (cx, cy, 175)
                cam_tar = (lx, ly, 175)
                fp_pos = cam_pos
                fp_tar = cam_tar
    else:
        cam_pos = pcam_pos
        cam_tar = (0,0,0)
def mayhem():
    global life,group, cx, cy
    for enm in group:
        dist = math.sqrt((cx-enm["x"])**2+(cy-enm["y"])**2)
        if dist < 45:
            life -= 1
            if life < 4:
                print(f"Remaining Player Life: {life}")
            enm["x"] = random.randint(-960, 960)
            enm["y"] = random.randint(-960, 960)
            enm["p"] = 0
            enm["pd"] = 1
            enm["finished"] = False
def keyboardListener(key, x, y):
    global cx, cy, a, dead, flag, cam_tar, cam_pos, pcam_pos, fires_bullet, guli, score, life, bm, group, enm, cheating, fp_tar, freeze, fp_pos
    if key == b'r':
        cam_pos = (0,500,500)
        pcam_pos = cam_pos
        flag = False
        cx = 0
        cy = 0
        a = 0
        enm = 5
        group = []
        cam_tar = (0,0,0)
        fires_bullet = False
        guli = []
        score = 0
        life = 5
        bm = 0
        dead = False
        cheating = False
        fp_pos = (0, 0, 0)
        freeze = False
        fp_tar = (0,0,0)
        for _ in range(enm):
            group.append({
                "x": random.randint(-960, 960),
                "y": random.randint(-960, 960),
                "p" : 0,
                "pd" : 1,
                "finished" : False
            })
    if not dead:
        if cheating:
            move = 25
        else :  
            move = 30  
        r = math.radians(a)
        if key == b'w':
            nx = cx + move * math.sin(r)
            ny = cy - move * math.cos(r)

            if -975 <= nx <= 975 and -975 <= ny <= 975:
                cx, cy = nx, ny
        elif key == b's':
            nx = cx - move * math.sin(r)
            ny = cy + move * math.cos(r)

            if -975 <= nx <= 975 and -975 <= ny <= 975:
                cx, cy = nx, ny
        elif key == b'a':
            a += 10
        elif key == b'd':
            a -= 10
        if key == b'c':
            cheating = not cheating
        if (key == b'v') and cheating and flag:
            freeze = not freeze
    else: 
        pass
def specialKeyListener(key, x, y):
    global cam_pos, pcam_pos, flag, cam_angle, radius, dead
    pcam_pos = cam_pos
    x, y, z = cam_pos
    radius = math.sqrt(x**2 + y**2)
    angle = math.atan2(y, x)
    if not dead:
        if key == GLUT_KEY_UP:
            if z < 1000:
                z += 10
        if key == GLUT_KEY_DOWN:
            if z>10:
                z -=10
        if key == GLUT_KEY_LEFT:
           angle -= math.radians(1)
        if key == GLUT_KEY_RIGHT:
           angle += math.radians(1)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        cam_pos = (x, y, z)
        pcam_pos = cam_pos
    else:
        cam_pos = pcam_pos
def mouseListener(button, state, x, y):
    global flag, cam_pos, cx, cy, fires_bullet, cam_pos, cam_tar, pcam_pos, fp_pos
    if not dead:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            fires_bullet = not fires_bullet
            print(f"Player Bullet Fired!")
            fire()
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            flag = not flag
            if flag:
                pcam_pos = cam_pos
            else:
                cam_pos = pcam_pos
                cam_tar = (0,0,0)
    else: 
        pass
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(fovY, 1600/900, 0.1, 4000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = cam_pos
    lx, ly, lz = cam_tar
    gluLookAt(x, y, z,
              lx, ly, lz,
              0, 0, 1)
def idle():
    global group, cx, cy, bm, life, dead, guli, cam_pos, pcam_pos, a, fires_bullet
    if bm > 9 or life < 1:
        if not dead:
            dead = True
            group.clear()
            guli.clear()
        glutPostRedisplay()
        return
    for enm in group:
        if enm["pd"] == 1:
            enm["p"] += 0.5
            if enm["p"] >= 5:
                enm["pd"] = -1
        else:
            enm["p"] -= 0.05
            if enm["p"] <= -5:
                enm["pd"] = 1
        nx = cx - enm["x"]
        ny = cy - enm["y"]
        st1 = math.sqrt((nx-0)**2+(ny-0)**2)
        if st1 > 0:
            ms = 0.1
            enm["x"] += ms * nx / st1
            enm["y"] += ms * ny / st1
    if cheating and not dead:
        a -= 1
        for enm in group:
            disx = enm["x"] - cx
            disy = enm["y"] - cy
            angle_to_enemy = math.degrees(math.atan2(disx, -disy)) % 360
            diff = (angle_to_enemy - a + 180) % 360 - 180
            if abs(diff) < 1:
                if not enm["finished"]:
                    fire()
                    enm["finished"] = True
            else:
                enm["finished"] = False
    guli_going()
    mayhem() 
    glutPostRedisplay()
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1600, 900)
    fp()
    setupCamera()
    glBegin(GL_QUADS)
    for j in range(13):
        y = 975 - (j+1) * 150
        for i in range(13):
            x = -975 + i * 150
            if (i+j)%2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            glVertex3f(x, y + 150, 0)
            glVertex3f(x + 150, y + 150, 0)
            glVertex3f(x + 150, y, 0)
            glVertex3f(x, y, 0)
    glEnd()

    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-975, -975, 0)
    glVertex3f(-975, 975, 0)
    glVertex3f(-975, 975, 200)
    glVertex3f(-975, -975, 200)
    glEnd()

    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(975, -975, 0)
    glVertex3f(975, 975, 0)
    glVertex3f(975, 975, 200)
    glVertex3f(975, -975, 200)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-975, -975, 0)
    glVertex3f(975, -975, 0)
    glVertex3f(975, -975, 200)
    glVertex3f(-975, -975, 200)
    glEnd()

    glColor3f(0.0, 0.749, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-975, 975, 0)
    glVertex3f(975, 975, 0)
    glVertex3f(975, 975, 200)
    glVertex3f(-975, 975, 200)
    glEnd()

    if dead:
        draw_text(20, 820, f"Game is Over. Your Score is {score}.")
        draw_text(20, 800, f'Press "R" to RESTART the Game.')
    if dead == False:
        draw_text(20, 820, f"Player Life Remaining: {life}")
        draw_text(20, 800, f"Game Score: {score}")
        draw_text(20, 780, f"Player Bullet Missed: {bm}")
    draw_shooter()
    draw_bullets()
    for enm in group:
        draw_enemy(enm)
    glutSwapBuffers()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1600, 900)
    glutInitWindowPosition(200, 50)
    wind = glutCreateWindow(b"ACtion Game")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()
if __name__ == "__main__":
    main()