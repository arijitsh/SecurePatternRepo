# Controller type: PID
import os

K = 10
attackLen = 3
safeDistance = 1
Th = 0.5

start = 0
index = start
isSat = 0

f0 = open("doubleintegratorresult.txt", "w+")
f0.write("0")
f0.close()

while index<K and isSat == 0:
    f = open("doubleintegrator.py", "w+")
    f.write("from z3 import *\n")
    f.write("import numpy as np\n\n")
    f.write("s = Solver()\n")
    f.write("set_option(rational_to_decimal=True)\n")
    f.write("set_option(precision=4)\n")
    f.write("attack = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("distance = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("y = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("yhat = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("x1 = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("x2 = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("xhat1 = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("xhat2 = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("u = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("r = np.zeros({0}, dtype=float)\n".format(K+1))

    # Variable declarations
    f.write("a11 = Real('a11')\n")
    f.write("a12 = Real('a12')\n")
    f.write("a21 = Real('a21')\n")
    f.write("a22 = Real('a22')\n")
    f.write("b1 = Real('b1')\n")
    f.write("b2 = Real('b2')\n")
    f.write("c1 = Real('c11')\n")
    f.write("c2 = Real('c12')\n")
    f.write("k1 = Real('k1')\n")
    f.write("k2 = Real('k2')\n")
    f.write("l1 = Real('l11')\n")
    f.write("l2 = Real('l12')\n")

    # Value assignment
    f.write("s.add(a11 == 1 )\n")
    f.write("s.add(a12 == 0.1)\n")
    f.write("s.add(a21 == 0)\n")
    f.write("s.add(a22 == 1)\n")

    f.write("s.add(b1 == 0.005)\n")
    f.write("s.add(b2 == 0.1)\n")

    f.write("s.add(c1 == 1)\n")
    f.write("s.add(c2 == 0)\n")

    f.write("s.add(k1 == 132)\n")
    f.write("s.add(k2 ==16)\n")

    f.write("s.add(l1 == 0.9902)\n")
    f.write("s.add(l2 == 0.0001)\n")

    for i in range(K+1):
        f.write("y_{0} = Real('y_{1}')\n".format(i,i))
        f.write("yhat_{0} = Real('yhat_{1}')\n".format(i,i))

        f.write("x1_{0} = Real('x1_{1}')\n".format(i,i))
        f.write("xhat1_{0} = Real('xhat1_{1}')\n".format(i,i))
        f.write("x2_{0} = Real('x2_{1}')\n".format(i,i))
        f.write("xhat2_{0} = Real('xhat2_{1}')\n".format(i,i))
        
        f.write("r1_{0} = Real('r1_{1}')\n".format(i,i))
        f.write("r2_{0} = Real('r2_{1}')\n".format(i,i))
        f.write("p_{0} = Real('p_{1}')\n".format(i,i))
        f.write("q_{0} = Real('q_{1}')\n".format(i,i))
        f.write("r_{0} = Real('r_{1}')\n".format(i,i))
        f.write("distance_{0} = Real('yr_{1}')\n".format(i,i))
        f.write("u_{0} = Real('u_{1}')\n".format(i,i))

    f.write("\n")
    f.write("s.add(x1_0 == 0)\n")
    f.write("s.add(x2_0 == 0)\n")
    f.write("s.add(xhat1_0 == 0)\n")
    f.write("s.add(xhat2_0 == 0)\n")
    f.write("s.add(u_0 == 0)\n")
    f.write("s.add(distance_0 == x1_0)\n")

    j = 0
    for i in range(K):      
        f.write("s.add(u_{0} == ((-1)*k1*xhat1_{1}) + ((-1)*k2*xhat2_{2}) )\n".format(i,i,i))

        if i == (j+index):
            f.write("attack_{0} = Real('attack_{1}')\n".format(i,i))
            f.write("\ns.add(y_{0} == (c1*x1_{1}) + (c2*x2_{2}) + attack_{3})\n".format(i,i,i,i))
            j = j+1
            if j== attackLen:
                j=0      
        else:
            f.write("\ns.add(y_{0} == (c1*x1_{1}) + (c2*x2_{2}))\n".format(i,i,i))        

        f.write("s.add(yhat_{0} == (c1*xhat1_{1}) + (c2*xhat2_{2}))\n".format(i,i,i))

        f.write("s.add(p_{0} == y_{1} - yhat_{2})\n".format(i,i,i))
        f.write("s.add(r_{0} == If(p_{1}<0,(-1)*p_{2},p_{3}))\n".format(i,i,i,i))

        # f.write("s.add(r_{0}<{1})\n".format(i,Th))
        
        f.write("s.add(x1_{0} == (a11*x1_{1}) + (a12*x2_{2}) + (b1*u_{3}))\n".format(i+1,i,i,i))        
        f.write("s.add(x2_{0} == (a21*x1_{1}) + (a22*x2_{2}) + (b2*u_{3}))\n".format(i+1,i,i,i))

        f.write("s.add(xhat2_{0} == (a21*xhat1_{1}) + (a22*xhat2_{2}) + (b2*u_{3}) + (l2*r_{4}))\n".format(i+1,i,i,i,i))
        f.write("s.add(xhat1_{0} == (a11*xhat1_{1}) + (a12*xhat2_{2}) + (b1*u_{3}) + (l1*r_{4}))\n".format(i+1,i,i,i,i))        

        f.write("s.add(distance_{0} == If(x1_{1}<0,(-1)*x1_{2},x1_{3}))\n".format(i+1,i+1,i+1,i+1))   


    f.write("s.add(Or(")
    for i in range(K):
        f.write("distance_{0}>{1}".format(i,safeDistance))
        if i!=(K-1):
            f.write(",")
    f.write("))\n")

    # f.write("\nprint(s.sexpr())")
    f.write("\nif s.check() == unsat:\n")
    f.write("\tprint( \"unsat\")\n")
    f.write("\tprint(s.check())\n")
    f.write("\tisSat = 0        \n")
    f.write("else:\n")
    f.write("\tprint( \"sat\")\n")
    f.write("\tprint(s.check())\n")
    f.write("\tisSat = 1\n")
    f.write("\tm = s.model()\n")
    f.write("\tfor d in m.decls():\n")
    # f.write("\t\tprint (\"%s = %s\" % (d.name(), m[d]))\n")

    f.write("\t\tif \"attack\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tattack[i] = float(y)\n")

    f.write("\t\telif \"x1_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tx1[i] = float(y)\n")

    f.write("\t\telif \"x2_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tx2[i] = float(y)\n")

    f.write("\t\telif \"xhat1_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\txhat1[i] = float(y)\n")

    f.write("\t\telif \"xhat2_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\txhat2[i] = float(y)\n")

    # f.write("\t\telif \"y_\" in d.name():\n")
    # f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    # f.write("\t\t\tx = str(m[d])\n")
    # f.write("\t\t\tindex = x.find(\"?\")\n")
    # f.write("\t\t\tif index != -1:\n")
    # f.write("\t\t\t\ty = x[:-1]\n")
    # f.write("\t\t\telse:\n")
    # f.write("\t\t\t\ty = x\n")
    # f.write("\t\t\ty[i] = float(y)\n")

    f.write("\t\telif \"yhat_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tyhat[i] = float(y)\n")
    
    f.write("\t\telif \"r_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tr[i] = float(y)\n")

    f.write("\t\telif \"distance_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tdistance[i] = float(y)\n")
    
    f.write("\t\telif \"u_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tu[i] = float(y)\n\n")    

    f.write("\tfor i in range({}):\n".format(K))
    f.write("\t\tprint(\"attack_{0}={1}\".format(i,attack[i]))\n")

    f.write("\t\tprint(\"x1_{0}={1}\".format(i,x1[i]))\n")
    f.write("\t\tprint(\"x2_{0}={1}\".format(i,x2[i]))\n")
    f.write("\t\tprint(\"xhat1_{0}={1}\".format(i,xhat1[i]))\n")
    f.write("\t\tprint(\"xhat2_{0}={1}\".format(i,xhat2[i]))\n")

    f.write("\t\tprint(\"u_{0}={1}\".format(i,u[i]))\n")

    # f.write("\t\tprint(\"y_{0}={1}\".format(i,y[i]))\n")
    f.write("\t\tprint(\"yhat_{0}={1}\".format(i,yhat[i]))\n")

    f.write("\t\tprint(\"r_{0}={1}\".format(i,r[i]))\n")
    f.write("\t\tprint(\"distance_{0}={1}\\n\".format(i,distance[i]))\n")

    f.write("print(\"attack on distance\")\n")
    f.write("print(attack)\n")

    f.write("if isSat==1:\n")
    f.write("\tf0 = open(\"doubleintegratorresult.txt\", \"w+\")\n")
    f.write("\tf0.write(\"1\")\n")
    f.write("\tf0.close()\n")

    f.write("f1 = open(\"distanceAttackVector.csv\", \"w+\")\n")
    f.write("for i in range({0}):\n".format(attackLen))
    f.write("\tf1.write(\"{0}\".format(attack[i]))\n")
    f.write("\tif i != {0}-1:\n".format(attackLen))
    f.write("\t\tf1.write(\",\")\n")
    f.write("f1.close()\n")

    f.close()
    os.system("python doubleintegrator.py>doubleintegrator.out")

    f0 = open("doubleintegratorresult.txt","r")
    if f0.mode == 'r':
        content = f0.read()
        isSat = int(content)
    f0.close()

    index = index + 1