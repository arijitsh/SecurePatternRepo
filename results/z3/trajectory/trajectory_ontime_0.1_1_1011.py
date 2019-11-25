from z3 import *
import math
import numpy as np

s = Solver()
set_option(rational_to_decimal=True)

x1_0 = Real('x1_0')
z1_0 = Real('z1_0')
xabs1_0 = Real('xabs1_0')
x2_0 = Real('x2_0')
z2_0 = Real('z2_0')
xabs2_0 = Real('xabs2_0')
y1_0 = Real('y1_0')
r1_0 = Real('r1_0')
rabs1_0 = Real('rabs1_0')
u1_0 = Real('u1_0')
r_0 = Real('r_0')

x1_1 = Real('x1_1')
z1_1 = Real('z1_1')
xabs1_1 = Real('xabs1_1')
x2_1 = Real('x2_1')
z2_1 = Real('z2_1')
xabs2_1 = Real('xabs2_1')
y1_1 = Real('y1_1')
r1_1 = Real('r1_1')
rabs1_1 = Real('rabs1_1')
u1_1 = Real('u1_1')
r_1 = Real('r_1')

s.add(Or(And(x1_0 < 1,x1_0 > 0.1),And(x1_0 > -1,x1_0 < -0.1)))
s.add(xabs1_0 == If(x1_0<0,(-1)*x1_0,x1_0))
s.add(Or(And(x2_0 < 10,x2_0 > 1.0),And(x2_0 > -10,x2_0 < -1.0)))
s.add(xabs2_0 == If(x2_0<0,(-1)*x2_0,x2_0))
s.add(y1_0 == 0)
s.add(u1_0 == 0)

# pattern = 1
s.add(r1_0 == y1_0 - (1*z1_0) - (0*z2_0) - (0*u1_0))
s.add(rabs1_0 == If(r1_0<0,(-1)*r1_0,r1_0))
s.add(r_0 ==rabs1_0 )
s.add(r_0<0.05)
s.add(z1_1 ==  (1.0*z1_0) + (0.1*z2_0) + (0.005*u1_0) + (1.8721*r1_0) )
s.add(z2_1 ==  (0.0*z1_0) + (1.0*z2_0) + (0.1*u1_0) + (9.6532*r1_0) )
s.add(x1_1 ==  (1.0*x1_0) + (0.1*x2_0) + (0.005*u1_0) )
s.add(x2_1 ==  (0.0*x1_0) + (1.0*x2_0) + (0.1*u1_0) )
s.add(xabs1_1 == If(x1_1<0,(-1)*x1_1,x1_1))
s.add(xabs2_1 == If(x2_1<0,(-1)*x2_1,x2_1))
s.add(u1_1 ==  - (16.0302*z1_1) - (5.6622*z2_1))
s.add(y1_1 ==  + (1*x1_1) + (0*x2_1) + (0*u1_1))
s.add(Or((xabs1_1>0.1),(xabs2_1>1.0)))

if s.check() != sat:
	print(s.check())
	isSat = 0
else:
	print(s.check())
	isSat = 1
	m = s.model()
	for d in m.decls():
		print ("%s = %s" % (d.name(), m[d]))
if isSat==0:
	f0 = open("../results/z3/trajectory/trajectory_ontime.z3result", "w+")
	f0.write("0")
	f0.close()
