import matplotlib.pyplot as plt

xlist = [0.2, -0.1, -0.1, 0.2]
ylist = [0, 0.1, -0.1, 0]

xlist2 = [x + 0.7 for x in xlist]
ylist2 = [y + 0.3 for y in ylist]

plt.plot(xlist, ylist)
plt.plot(xlist2, ylist2)
plt.show()