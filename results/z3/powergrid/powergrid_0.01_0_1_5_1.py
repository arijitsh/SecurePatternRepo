from z3 import *
import math
import numpy as np

s = Solver()
set_option(rational_to_decimal=True)
xabs1 = np.zeros(6, dtype=float)
x1 = np.zeros(6, dtype=float)
z1 = np.zeros(6, dtype=float)
xabs2 = np.zeros(6, dtype=float)
x2 = np.zeros(6, dtype=float)
z2 = np.zeros(6, dtype=float)
y1 = np.zeros(6, dtype=float)
attackOnY1 = np.zeros(6, dtype=float)
r1 = np.zeros(6, dtype=float)
y2 = np.zeros(6, dtype=float)
attackOnY2 = np.zeros(6, dtype=float)
r2 = np.zeros(6, dtype=float)
u1 = np.zeros(6, dtype=float)
uattacked1 = np.zeros(6, dtype=float)
attackOnU1 = np.zeros(6, dtype=float)
u2 = np.zeros(6, dtype=float)
uattacked2 = np.zeros(6, dtype=float)
attackOnU2 = np.zeros(6, dtype=float)
r = np.zeros(6, dtype=float)

y1_0 = Real('y1_0')
r1_0 = Real('r1_0')
rabs1_0 = Real('rabs1_0')
y2_0 = Real('y2_0')
r2_0 = Real('r2_0')
rabs2_0 = Real('rabs2_0')
x1_0 = Real('x1_0')
z1_0 = Real('z1_0')
xabs1_0 = Real('xabs1_0')
x2_0 = Real('x2_0')
z2_0 = Real('z2_0')
xabs2_0 = Real('xabs2_0')
u1_0 = Real('u1_0')
uattacked1_0 = Real('uattacked1_0')
u2_0 = Real('u2_0')
uattacked2_0 = Real('uattacked2_0')
r_0 = Real('r_0')
y1_1 = Real('y1_1')
r1_1 = Real('r1_1')
rabs1_1 = Real('rabs1_1')
y2_1 = Real('y2_1')
r2_1 = Real('r2_1')
rabs2_1 = Real('rabs2_1')
x1_1 = Real('x1_1')
z1_1 = Real('z1_1')
xabs1_1 = Real('xabs1_1')
x2_1 = Real('x2_1')
z2_1 = Real('z2_1')
xabs2_1 = Real('xabs2_1')
u1_1 = Real('u1_1')
uattacked1_1 = Real('uattacked1_1')
u2_1 = Real('u2_1')
uattacked2_1 = Real('uattacked2_1')
r_1 = Real('r_1')
y1_2 = Real('y1_2')
r1_2 = Real('r1_2')
rabs1_2 = Real('rabs1_2')
y2_2 = Real('y2_2')
r2_2 = Real('r2_2')
rabs2_2 = Real('rabs2_2')
x1_2 = Real('x1_2')
z1_2 = Real('z1_2')
xabs1_2 = Real('xabs1_2')
x2_2 = Real('x2_2')
z2_2 = Real('z2_2')
xabs2_2 = Real('xabs2_2')
u1_2 = Real('u1_2')
uattacked1_2 = Real('uattacked1_2')
u2_2 = Real('u2_2')
uattacked2_2 = Real('uattacked2_2')
r_2 = Real('r_2')
y1_3 = Real('y1_3')
r1_3 = Real('r1_3')
rabs1_3 = Real('rabs1_3')
y2_3 = Real('y2_3')
r2_3 = Real('r2_3')
rabs2_3 = Real('rabs2_3')
x1_3 = Real('x1_3')
z1_3 = Real('z1_3')
xabs1_3 = Real('xabs1_3')
x2_3 = Real('x2_3')
z2_3 = Real('z2_3')
xabs2_3 = Real('xabs2_3')
u1_3 = Real('u1_3')
uattacked1_3 = Real('uattacked1_3')
u2_3 = Real('u2_3')
uattacked2_3 = Real('uattacked2_3')
r_3 = Real('r_3')
y1_4 = Real('y1_4')
r1_4 = Real('r1_4')
rabs1_4 = Real('rabs1_4')
y2_4 = Real('y2_4')
r2_4 = Real('r2_4')
rabs2_4 = Real('rabs2_4')
x1_4 = Real('x1_4')
z1_4 = Real('z1_4')
xabs1_4 = Real('xabs1_4')
x2_4 = Real('x2_4')
z2_4 = Real('z2_4')
xabs2_4 = Real('xabs2_4')
u1_4 = Real('u1_4')
uattacked1_4 = Real('uattacked1_4')
u2_4 = Real('u2_4')
uattacked2_4 = Real('uattacked2_4')
r_4 = Real('r_4')
y1_5 = Real('y1_5')
r1_5 = Real('r1_5')
rabs1_5 = Real('rabs1_5')
y2_5 = Real('y2_5')
r2_5 = Real('r2_5')
rabs2_5 = Real('rabs2_5')
x1_5 = Real('x1_5')
z1_5 = Real('z1_5')
xabs1_5 = Real('xabs1_5')
x2_5 = Real('x2_5')
z2_5 = Real('z2_5')
xabs2_5 = Real('xabs2_5')
u1_5 = Real('u1_5')
uattacked1_5 = Real('uattacked1_5')
u2_5 = Real('u2_5')
uattacked2_5 = Real('uattacked2_5')
r_5 = Real('r_5')

s.add(x1_0 >= -0.010000000000000002)
s.add(x1_0 <= 0.010000000000000002)
s.add(z1_0 == 0)
s.add(xabs1_0 == If(x1_0<0,(-1)*x1_0,x1_0))
s.add(x2_0 >= -0.020000000000000004)
s.add(x2_0 <= 0.020000000000000004)
s.add(z2_0 == 0)
s.add(xabs2_0 == If(x2_0<0,(-1)*x2_0,x2_0))
s.add(y1_0 == 0)
s.add(y2_0 == 0)
s.add(u1_0 == 0)
s.add(uattacked1_0 == 0)
s.add(u2_0 == 0)
s.add(uattacked2_0 == 0)

# pattern = 1
s.add(r1_0 == y1_0 - (0.8*z1_0) - (2.4*z2_0) - (0*u1_0) - (0*u2_0))
s.add(r2_0 == y2_0 - (1.6*z1_0) - (0.8*z2_0) - (0*u1_0) - (0*u2_0))
s.add(rabs1_0 == If(r1_0<0,(-1)*r1_0,r1_0))
s.add(rabs2_0 == If(r2_0<0,(-1)*r2_0,r2_0))
s.add(r_0 ==rabs1_0 +rabs2_0 )
s.add(r_0<0.01)
s.add(z1_1 ==  (-1*z1_0) + (-3*z2_0) + (2*u1_0) + (-1*u2_0) + (-1.1751*r1_0) + (-0.1412*r2_0) )
s.add(z2_1 ==  (3*z1_0) + (-5*z2_0) + (1*u1_0) + (0*u2_0) + (-2.6599*r1_0) + (2.2549*r2_0) )
s.add(x1_1 ==  (-1*x1_0) + (-3*x2_0) + (2*uattacked1_0) + (-1*uattacked2_0) )
s.add(x2_1 ==  (3*x1_0) + (-5*x2_0) + (1*uattacked1_0) + (0*uattacked2_0) )
s.add(xabs1_1 == If(x1_1<0,(-1)*x1_1,x1_1))
s.add(xabs2_1 == If(x2_1<0,(-1)*x2_1,x2_1))
s.add(u1_1 ==  - (2.9846*z1_0) - (-4.9827*z2_0))
s.add(u2_1 ==  - (6.9635*z1_0) - (-6.9599*z2_0))
attackOnU1_0 = Real('attackOnU1_0')
attackOnU2_0 = Real('attackOnU2_0')
s.add(uattacked1_1 == u1_1+ (1.0*attackOnU1_0))
s.add(uattacked2_1 == u2_1+ (0.0*attackOnU2_0))
attackOnY1_0 = Real('attackOnY1_0')
attackOnY2_0 = Real('attackOnY2_0')
s.add(y1_1 == (1.0*attackOnY1_0) + (0.8*x1_1) + (2.4*x2_1) + (0*u1_1) + (0*u2_1))
s.add(y2_1 == (0.0*attackOnY2_0) + (1.6*x1_1) + (0.8*x2_1) + (0*u1_1) + (0*u2_1))
# pattern = 1
s.add(r1_1 == y1_1 - (0.8*z1_1) - (2.4*z2_1) - (0*u1_1) - (0*u2_1))
s.add(r2_1 == y2_1 - (1.6*z1_1) - (0.8*z2_1) - (0*u1_1) - (0*u2_1))
s.add(rabs1_1 == If(r1_1<0,(-1)*r1_1,r1_1))
s.add(rabs2_1 == If(r2_1<0,(-1)*r2_1,r2_1))
s.add(r_1 ==rabs1_1 +rabs2_1 )
s.add(r_1<0.01)
s.add(z1_2 ==  (-1*z1_1) + (-3*z2_1) + (2*u1_1) + (-1*u2_1) + (-1.1751*r1_1) + (-0.1412*r2_1) )
s.add(z2_2 ==  (3*z1_1) + (-5*z2_1) + (1*u1_1) + (0*u2_1) + (-2.6599*r1_1) + (2.2549*r2_1) )
s.add(x1_2 ==  (-1*x1_1) + (-3*x2_1) + (2*uattacked1_1) + (-1*uattacked2_1) )
s.add(x2_2 ==  (3*x1_1) + (-5*x2_1) + (1*uattacked1_1) + (0*uattacked2_1) )
s.add(xabs1_2 == If(x1_2<0,(-1)*x1_2,x1_2))
s.add(xabs2_2 == If(x2_2<0,(-1)*x2_2,x2_2))
s.add(u1_2 ==  - (2.9846*z1_1) - (-4.9827*z2_1))
s.add(u2_2 ==  - (6.9635*z1_1) - (-6.9599*z2_1))
s.add(uattacked1_2 == u1_2)
s.add(uattacked2_2 == u2_2)
s.add(y1_2 ==  + (0.8*x1_2) + (2.4*x2_2) + (0*u1_2) + (0*u2_2))
s.add(y2_2 ==  + (1.6*x1_2) + (0.8*x2_2) + (0*u1_2) + (0*u2_2))
# pattern = 1
s.add(r1_2 == y1_2 - (0.8*z1_2) - (2.4*z2_2) - (0*u1_2) - (0*u2_2))
s.add(r2_2 == y2_2 - (1.6*z1_2) - (0.8*z2_2) - (0*u1_2) - (0*u2_2))
s.add(rabs1_2 == If(r1_2<0,(-1)*r1_2,r1_2))
s.add(rabs2_2 == If(r2_2<0,(-1)*r2_2,r2_2))
s.add(r_2 ==rabs1_2 +rabs2_2 )
s.add(r_2<0.01)
s.add(z1_3 ==  (-1*z1_2) + (-3*z2_2) + (2*u1_2) + (-1*u2_2) + (-1.1751*r1_2) + (-0.1412*r2_2) )
s.add(z2_3 ==  (3*z1_2) + (-5*z2_2) + (1*u1_2) + (0*u2_2) + (-2.6599*r1_2) + (2.2549*r2_2) )
s.add(x1_3 ==  (-1*x1_2) + (-3*x2_2) + (2*uattacked1_2) + (-1*uattacked2_2) )
s.add(x2_3 ==  (3*x1_2) + (-5*x2_2) + (1*uattacked1_2) + (0*uattacked2_2) )
s.add(xabs1_3 == If(x1_3<0,(-1)*x1_3,x1_3))
s.add(xabs2_3 == If(x2_3<0,(-1)*x2_3,x2_3))
s.add(u1_3 ==  - (2.9846*z1_2) - (-4.9827*z2_2))
s.add(u2_3 ==  - (6.9635*z1_2) - (-6.9599*z2_2))
s.add(uattacked1_3 == u1_3)
s.add(uattacked2_3 == u2_3)
s.add(y1_3 ==  + (0.8*x1_3) + (2.4*x2_3) + (0*u1_3) + (0*u2_3))
s.add(y2_3 ==  + (1.6*x1_3) + (0.8*x2_3) + (0*u1_3) + (0*u2_3))
# pattern = 1
s.add(r1_3 == y1_3 - (0.8*z1_3) - (2.4*z2_3) - (0*u1_3) - (0*u2_3))
s.add(r2_3 == y2_3 - (1.6*z1_3) - (0.8*z2_3) - (0*u1_3) - (0*u2_3))
s.add(rabs1_3 == If(r1_3<0,(-1)*r1_3,r1_3))
s.add(rabs2_3 == If(r2_3<0,(-1)*r2_3,r2_3))
s.add(r_3 ==rabs1_3 +rabs2_3 )
s.add(r_3<0.01)
s.add(z1_4 ==  (-1*z1_3) + (-3*z2_3) + (2*u1_3) + (-1*u2_3) + (-1.1751*r1_3) + (-0.1412*r2_3) )
s.add(z2_4 ==  (3*z1_3) + (-5*z2_3) + (1*u1_3) + (0*u2_3) + (-2.6599*r1_3) + (2.2549*r2_3) )
s.add(x1_4 ==  (-1*x1_3) + (-3*x2_3) + (2*uattacked1_3) + (-1*uattacked2_3) )
s.add(x2_4 ==  (3*x1_3) + (-5*x2_3) + (1*uattacked1_3) + (0*uattacked2_3) )
s.add(xabs1_4 == If(x1_4<0,(-1)*x1_4,x1_4))
s.add(xabs2_4 == If(x2_4<0,(-1)*x2_4,x2_4))
s.add(u1_4 ==  - (2.9846*z1_3) - (-4.9827*z2_3))
s.add(u2_4 ==  - (6.9635*z1_3) - (-6.9599*z2_3))
s.add(uattacked1_4 == u1_4)
s.add(uattacked2_4 == u2_4)
s.add(y1_4 ==  + (0.8*x1_4) + (2.4*x2_4) + (0*u1_4) + (0*u2_4))
s.add(y2_4 ==  + (1.6*x1_4) + (0.8*x2_4) + (0*u1_4) + (0*u2_4))
# pattern = 1
s.add(r1_4 == y1_4 - (0.8*z1_4) - (2.4*z2_4) - (0*u1_4) - (0*u2_4))
s.add(r2_4 == y2_4 - (1.6*z1_4) - (0.8*z2_4) - (0*u1_4) - (0*u2_4))
s.add(rabs1_4 == If(r1_4<0,(-1)*r1_4,r1_4))
s.add(rabs2_4 == If(r2_4<0,(-1)*r2_4,r2_4))
s.add(r_4 ==rabs1_4 +rabs2_4 )
s.add(r_4<0.01)
s.add(z1_5 ==  (-1*z1_4) + (-3*z2_4) + (2*u1_4) + (-1*u2_4) + (-1.1751*r1_4) + (-0.1412*r2_4) )
s.add(z2_5 ==  (3*z1_4) + (-5*z2_4) + (1*u1_4) + (0*u2_4) + (-2.6599*r1_4) + (2.2549*r2_4) )
s.add(x1_5 ==  (-1*x1_4) + (-3*x2_4) + (2*uattacked1_4) + (-1*uattacked2_4) )
s.add(x2_5 ==  (3*x1_4) + (-5*x2_4) + (1*uattacked1_4) + (0*uattacked2_4) )
s.add(xabs1_5 == If(x1_5<0,(-1)*x1_5,x1_5))
s.add(xabs2_5 == If(x2_5<0,(-1)*x2_5,x2_5))
s.add(u1_5 ==  - (2.9846*z1_4) - (-4.9827*z2_4))
s.add(u2_5 ==  - (6.9635*z1_4) - (-6.9599*z2_4))
s.add(uattacked1_5 == u1_5)
s.add(uattacked2_5 == u2_5)
s.add(y1_5 ==  + (0.8*x1_5) + (2.4*x2_5) + (0*u1_5) + (0*u2_5))
s.add(y2_5 ==  + (1.6*x1_5) + (0.8*x2_5) + (0*u1_5) + (0*u2_5))
s.add(Or((xabs1_0 - 0.1)>0.001,(xabs1_1 - 0.1)>0.001,(xabs1_2 - 0.1)>0.001,(xabs1_3 - 0.1)>0.001,(xabs1_4 - 0.1)>0.001,(xabs2_0 - 0.2)>0.001,(xabs2_1 - 0.2)>0.001,(xabs2_2 - 0.2)>0.001,(xabs2_3 - 0.2)>0.001,(xabs2_4 - 0.2)>0.001))

if s.check() != sat:
	print(s.check())
	isSat = 0
else:
	print(s.check())
	isSat = 1
	f0 = open("../results/z3/powergrid/powergrid.z3result", "w+")
	f0.write("1")
	f0.close()
	m = s.model()
	for d in m.decls():
		if "attackOnU1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			attackOnU1[i] = float(y)
		if "uattacked1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			uattacked1[i] = float(y)
		if "u1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			u1[i] = float(y)
		if "attackOnU2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			attackOnU2[i] = float(y)
		if "uattacked2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			uattacked2[i] = float(y)
		if "u2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			u2[i] = float(y)
		if "z1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			z1[i] = float(y)
		if "xabs1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			xabs1[i] = float(y)
		if "x1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			x1[i] = float(y)
		if "z2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			z2[i] = float(y)
		if "xabs2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			xabs2[i] = float(y)
		if "x2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			x2[i] = float(y)
		if "attackOnY1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			attackOnY1[i] = float(y)
		if "y1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			y1[i] = float(y)
		if "r1_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			r1[i] = float(y)
		if "attackOnY2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			attackOnY2[i] = float(y)
		if "y2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			y2[i] = float(y)
		if "r2_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			r2[i] = float(y)
		if "r_" in d.name():
			i = int(d.name().split('_')[1])
			x = str(m[d])
			index = x.find("?")
			if index != -1:
				y = x[:-1]
			else:
				y = x
			r[i] = float(y)
	for i in range(5):
		print("x1_{0}={1}".format(i,x1[i]))
		print("x2_{0}={1}".format(i,x2[i]))
		print("z1_{0}={1}".format(i,z1[i]))
		print("z2_{0}={1}".format(i,z2[i]))
		print("xabs1_{0}={1}".format(i,xabs1[i]))
		print("xabs2_{0}={1}".format(i,xabs2[i]))
		print("attackOnU1_{0}={1}".format(i,attackOnU1[i]))
		print("attackOnU2_{0}={1}".format(i,attackOnU2[i]))
		print("u1_{0}={1}".format(i,u1[i]))
		print("u2_{0}={1}".format(i,u2[i]))
		print("uattacked1_{0}={1}".format(i,uattacked1[i]))
		print("uattacked2_{0}={1}".format(i,uattacked2[i]))
		print("attackOnY1_{0}={1}".format(i,attackOnY1[i]))
		print("attackOnY2_{0}={1}".format(i,attackOnY2[i]))
		print("y1_{0}={1}".format(i,y1[i]))
		print("y2_{0}={1}".format(i,y2[i]))
		print("r1_{0}={1}".format(i,r1[i]))
		print("r2_{0}={1}".format(i,r2[i]))
		print("r_{0}={1}".format(i,r[i]))
print("attack on control signal component 1")
print(attackOnU1)
print("attack on control signal component 2")
print(attackOnU2)
print("attack on sensor 1")
print(attackOnY1)
print("attack on sensor 2")
print(attackOnY2)
if isSat==1:
	f0 = open("../results/z3/powergrid/powergrid.z3result", "w+")
	f0.write("1")
	f0.close()
