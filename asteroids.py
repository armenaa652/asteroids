import pygame
import sys
import random
import numpy
import math
from pygame.locals import *

mainClock = pygame.time.Clock()

WHITE = (225,225,225)
BLACK = (0, 0 ,0)
bullets = []

def terminate():
    pygame.quit()
    sys.exit()

def updateShip(xpos, ypos, vel, theta):
    xpos += vel * math.cos(theta)
    ypos += vel * math.sin(theta)
    vel *= .98
    return xpos, ypos, vel

def drawShip(xpos, ypos, theta):
    top =   (xpos + scale * math.cos(theta), ypos + scale * math.sin(theta))
    left =  (xpos - scale * math.cos(theta - (math.pi / 4)), ypos - scale * math.sin(theta - (math.pi / 4)))
    right = (xpos - scale * math.cos(theta + (math.pi / 4)), ypos - scale * math.sin(theta + (math.pi / 4)))
    pygame.draw.line(windowSurface, WHITE, top, left, 3)
    pygame.draw.line(windowSurface, WHITE, top, right, 3)
    #pygame.draw.polygon(windowSurface, WHITE, (top, left, right), 3)
    return [top, left, right]

def addBullet(xpos, ypos, theta):
    bullets.append([xpos + scale * math.cos(theta), ypos + scale * math.sin(theta), theta])

def updateBullets(bullet, i):
    bullet[i][0] += 15 * math.cos(bullet[i][2])
    bullet[i][1] += 15 * math.sin(bullet[i][2])

def drawBullets(bullet):
    size = numpy.shape(bullet)
    for i in range(size[0]):
        if bullet[i][0] > WINDOWWIDTH or bullet[i][0] < 0:
            bullets.remove(bullet[i])
            break
        if bullet[i][1] > WINDOWHEIGHT or bullet[i][1] < 0:
            bullets.remove(bullet[i])
            break
        pygame.draw.circle(windowSurface, (255,255,0), (int(bullet[i][0]),int(bullet[i][1])), 3)
        updateBullets(bullet, i)

def addAsteroids(maxSize):
    minSize = maxSize/3
    xpos = []
    ypos = []
    randNum = random.randint(1, 4)
    if randNum == 1:
        xpos = WINDOWWIDTH
        ypos = random.randint(0, WINDOWHEIGHT)
    elif randNum == 2:
        xpos = 0
        ypos = random.randint(0, WINDOWHEIGHT)
    elif randNum == 3:
        xpos = random.randint(0, WINDOWWIDTH)
        ypos = WINDOWHEIGHT
    elif randNum == 4:
        xpos = random.randint(0, WINDOWWIDTH)
        ypos = 0

    pointNum = random.randint(8,16)
    points = []
    for i in range(pointNum + 1):
        theta = (2*i)*math.pi/pointNum
        r = random.randint(minSize,maxSize)
        points.append([xpos + r * math.cos(theta), ypos + r * math.sin(theta)])
    points.remove(points[0])
    theta = [numpy.cos(random.randint(-90,90)*float(numpy.pi/180)), numpy.sin(random.randint(0,360)*float(numpy.pi/180))]
    size = maxSize
    stats = [theta, size]
    center = [xpos, ypos]
    return center, points, stats

def divideAsteroids(maxSize, xpos, ypos):
    minSize = maxSize/3
    pointNum = random.randint(8,16)
    points = []
    for i in range(pointNum + 1):
        theta = (2*i)*math.pi/pointNum
        r = random.randint(minSize,maxSize)
        points.append([xpos + r * math.cos(theta), ypos + r * math.sin(theta)])
    points.remove(points[0])
    theta = [numpy.cos(random.randint(0,360)*float(numpy.pi/180)), numpy.sin(random.randint(0,360)*float(numpy.pi/180))]
    size = maxSize
    stats = [theta, size]
    center = [xpos, ypos]
    return center, points, stats

def updateAsteroids(center, acoord):
    asterAmount = numpy.shape(acoord)[0]
    for i in range(asterAmount):
        pointAmount = int((numpy.size(acoord[i])) / 2)
        asterSpeed = 120 / asterStats[i][1]
        for j in range(pointAmount):
            acoord[i][j] = [acoord[i][j][0] + asterSpeed * asterStats[i][0][0], acoord[i][j][1] + asterSpeed * asterStats[i][0][1]]
        center[i] = [center[i][0] + asterSpeed * asterStats[i][0][0], center[i][1] + asterSpeed * asterStats[i][0][1]]
        c = [int(center[i][0]), int(center[i][1])]
        pygame.draw.circle(windowSurface, (150, 150, 150), c, 2)
        if center[i][0] < 0 - asterStats[i][1]:
            for j in range(pointAmount):
                acoord[i][j] = [acoord[i][j][0] + WINDOWWIDTH + 2 * asterStats[i][1] - 1, acoord[i][j][1]]
            center[i] = [center[i][0] + WINDOWWIDTH + 2 * asterStats[i][1] - 1, center[i][1]]
        if center[i][0] > WINDOWWIDTH + asterStats[i][1]:
            for j in range(pointAmount):
                acoord[i][j] = [acoord[i][j][0] - WINDOWWIDTH - 2 * asterStats[i][1] + 1, acoord[i][j][1]]
            center[i] = [center[i][0] - WINDOWWIDTH - 2 * asterStats[i][1] + 1, center[i][1]]
        if center[i][1] < 0 - asterStats[i][1]:
            for j in range(pointAmount):
                acoord[i][j] = [acoord[i][j][0], acoord[i][j][1] + WINDOWWIDTH + 2 * asterStats[i][1] - 1]
            center[i] = [center[i][0], center[i][1] + WINDOWWIDTH + 2 * asterStats[i][1] - 1]
        if center[i][1] > WINDOWHEIGHT + asterStats[i][1]:
            for j in range(pointAmount):
                acoord[i][j] = [acoord[i][j][0], acoord[i][j][1] - WINDOWWIDTH - 2 * asterStats[i][1] + 1]
            center[i] = [center[i][0], center[i][1] - WINDOWWIDTH - 2 * asterStats[i][1] + 1]
    return center, acoord

def drawAsteroids(asteroids):
    for a in asteroids:
        pygame.draw.polygon(windowSurface, (150, 150, 150), a, 3)

def bulletCollision(acoord, bcoord, acenter, point):
    for i in range(len(bcoord)):
        for j in range(len(acoord)):
            if distance(bcoord[i],acenter[j]) < asterStats[j][1]:
                point += 10
                bcoord.remove(bcoord[i])
                if asterStats[j][1] > 30:
                    for k in range(2):
                        addedCenter, addedAster, addedAsterStats = divideAsteroids(asterStats[j][1] - 30, acenter[j][0], acenter[j][1])
                        acoord.append(addedAster)
                        asterStats.append(addedAsterStats)
                        acenter.append(addedCenter)
                acenter.remove(acenter[j])
                acoord.remove(acoord[j])
                asterStats.remove(asterStats[j])
                return acenter, acoord, bcoord, point
    return acenter, acoord, bcoord, point

def shipCollision(acoord, scoord, acenter):
    for i in range(len(scoord)):
        for j in range(len(acoord)):
            if distance(scoord[i],acenter[j]) < asterStats[j][1]:
                waitForPlayerToPressKey(font)
                return True
    return False

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def drawText(text, textfont, xpos, ypos):
    textobj = textfont.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (xpos, ypos)
    windowSurface.blit(textobj, textrect)

def waitForPlayerToPressKey(font):
    drawText('YOU DIED', font, (WINDOWWIDTH / 3) + 50, (WINDOWHEIGHT / 3))
    drawText('Press any key to play again.', font, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

pygame.init()
pygame.display.set_caption('Asteroids')
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
font = pygame.font.SysFont(None, 48)

topScore = 0

while True:
    scale = 20
    spawn = 6
    speed = 0
    count = 0
    score = 0
    asterCenter = []
    asterCoords = []
    asterStats = []
    shipCoords = []
    moveUp = rotateLeft = rotateRight = False
    x = WINDOWWIDTH / 2
    y = WINDOWHEIGHT / 2
    heading = angle = 3 * math.pi / 2

    while not shipCollision(asterCoords, shipCoords, asterCenter):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    rotateLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    rotateRight = True
                if event.key == K_UP or event.key == K_w:
                    moveUp = True
                if event.key == K_SPACE:
                    addBullet(x,y,heading)
            if event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == K_q:
                    terminate()
                if event.key == K_LEFT or event.key == K_a:
                    rotateLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    rotateRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False

        windowSurface.fill(BLACK)

        if moveUp:
            if speed < 4:
                speed += .2
                angle = heading
            pygame.draw.polygon(windowSurface, (255, 0, 0),((x - (scale-5)*math.cos(angle - (math.pi / 5)), y - (scale-5)*math.sin(angle - (math.pi / 5))),(x - (scale-5)*math.cos(angle + (math.pi / 5)), y - (scale-5)*math.sin(angle + (math.pi / 5))),(x + (scale+12)*math.cos(angle+math.pi), y + (scale+12)*math.sin(angle + math.pi))))
        if x > WINDOWWIDTH + scale:
            x = -scale + 1
        elif x < -scale:
            x = WINDOWWIDTH + scale - 1
        elif y > WINDOWHEIGHT + scale:
            y = -scale + 1
        elif y < -scale:
            y = WINDOWHEIGHT + scale - 1
        if rotateRight:
            heading += .1
        if rotateLeft:
            heading -= .1

        x, y, speed = updateShip(x, y, speed, angle)

        if len(bullets) > 0:
            drawBullets(bullets)
        if len(asterCoords) > 0:
            drawAsteroids(asterCoords)
            asterCenter, asterCoords = updateAsteroids(asterCenter, asterCoords)
        else:
            for null in range(spawn):
                centerAsteroids, addedAsteroids, addedStats = addAsteroids(90)
                asterCenter.append(centerAsteroids)
                asterCoords.append(addedAsteroids)
                asterStats.append(addedStats)
            spawn += 1

        if score > topScore:
            topScore = score

        shipCoords = drawShip(x, y, heading)
        asterCenter, asterCoords, bullets, score = bulletCollision(asterCoords, bullets, asterCenter, score)
        drawText('Score: %s' % score, font, 15, 5)
        drawText('Top Score: %s' % topScore, font, 15, 45)
        drawText('Level: %s' % str(spawn - 6), font, WINDOWWIDTH - 140, 5)
        pygame.display.update()
        mainClock.tick(60)
