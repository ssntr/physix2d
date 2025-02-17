import matplotlib.pyplot as plt
from math import sin, cos, radians, sqrt

g = 9.81 # m/s^2
dt = 0.05 # s
k = 0.1 # ilmanvastuskerroin

xlist = [ 0.0 ]
ylist = [ 0.0 ]
v0 = 30 # m/s
kulma = radians(45)
vx = v0 * cos(kulma)
vy = v0 * sin(kulma)

while ylist[-1] >= 0: # m, heittoa jatketaan maahan asti
    v = sqrt(vx**2 + vy**2) # lasketaan nopeus |v|=sqrt(vx^2 + vy^2)

    ax = -k*v*vx
    yx = -g - (k*v*vy) # lasketaan x- ja y-komponenttien kiihtyvyydet (y vähennetään g:stä)
    vx += ax*dt
    vy += yx*dt # lasketaan nopeuden komponentit kiihtyvyydellä ja ajan muutoksella

    xlist.append(xlist[-1] + vx*dt)
    ylist.append(ylist[-1] + vy*dt)

plt.plot(xlist,ylist)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.show()
