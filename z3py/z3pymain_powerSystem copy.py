# Controller type: PID
import os
import numpy as np

modelName= "powersystem"
A= np.matrix('0.66 0.53; -0.53 0.13')
B= np.matrix('0.34; 0.53')
C= np.matrix('1 0; 0 1')
D= np.matrix('0 ; 0')
Gain= np.matrix('0.0556 0.3306')
L= np.matrix('0.36 0.27;  -0.31 0.08')

u_count=B.shape[1]
x_count=A.shape[1]
y_count=C.shape[0]

u_attack = np.zeros(u_count,dtype=float)
y_attack = np.zeros(y_count,dtype=float)

####### Configure which sensor/control input to attack ########
u_attack[0] = 1
y_attack[0] = 1

safex = [0.1,0.05]
th = 0.03
startpoint=0
K=15
attackLen=6
pattern= 1

start = 0
index = start
isSat = 0

f0 = open("powersystemresult_new.txt", "w+")
f0.write("0")
f0.close()

while index<K and isSat == 0:
    f = open("powersystem_new.py", "w+")
    f.write("from z3 import *\n")
    f.write("import numpy as np\n\n")
    f.write("s = Solver()\n")
    f.write("set_option(rational_to_decimal=True)\n")
    f.write("set_option(precision=4)\n")

    f.write("attack1 = np.zeros({0}, dtype=float)\n".format(K+1))
    f.write("attack2 = np.zeros({0}, dtype=float)\n".format(K+1))
    for varcount in range(1,x_count+1):
        f.write("x"+str(varcount)+"_abs = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("x"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("xhat"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
    for varcount in range(1,y_count+1):
        f.write("y"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("attackOnY"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("yhat"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("r"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
    for varcount in range(1,u_count+1):
        f.write("u"+str(varcount)+"_abs = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("attackOnU"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
    f.write("r = np.zeros("+str(K+1)+", dtype=float)\n")

    # f.write("theta = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("omega = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("y1 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("y2 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("yhat1 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("yhat2 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("x1 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("x2 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("xhat1 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("xhat2 = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("u = np.zeros({0}, dtype=float)\n".format(K+1))
    # f.write("r = np.zeros({0}, dtype=float)\n".format(K+1))

    # Variable declarations
    # f.write("a11 = Real('a11')\n")
    # f.write("a12 = Real('a12')\n")
    # f.write("a21 = Real('a21')\n")
    # f.write("a22 = Real('a22')\n")
    # f.write("b1 = Real('b1')\n")
    # f.write("b2 = Real('b2')\n")
    # f.write("c11 = Real('c11')\n")
    # f.write("c12 = Real('c12')\n")
    # f.write("c21 = Real('c21')\n")
    # f.write("c22 = Real('c22')\n")
    # f.write("k1 = Real('k1')\n")
    # f.write("k2 = Real('k2')\n")
    # f.write("l11 = Real('l11')\n")
    # f.write("l12 = Real('l12')\n")
    # f.write("l21 = Real('l21')\n")
    # f.write("l22 = Real('l22')\n")

    # # Value assignment
    # f.write("s.add(a11 == 0.66)\n")
    # f.write("s.add(a12 == 0.53)\n")
    # f.write("s.add(a21 == -0.53)\n")
    # f.write("s.add(a22 == 0.13)\n")

    # f.write("s.add(b1 == 0.34)\n")
    # f.write("s.add(b2 == 0.53)\n")

    # f.write("s.add(c11 == 1)\n")
    # f.write("s.add(c12 == 0)\n")
    # f.write("s.add(c21 == 0)\n")
    # f.write("s.add(c22 == 1)\n")

    # f.write("s.add(k1 == 0.0556)\n")
    # f.write("s.add(k2 == 0.3306)\n")

    # f.write("s.add(l11 == 0.3600)\n")
    # f.write("s.add(l12 == 0.2700)\n")
    # f.write("s.add(l21 == -0.3100)\n")
    # f.write("s.add(l22 == 0.0800)\n")
    decl=""
    for i in range(K+1):
        # f.write("y1_{0} = Real('y1_{1}')\n".format(i,i))
        # f.write("yhat1_{0} = Real('yhat1_{1}')\n".format(i,i))
        # f.write("y2_{0} = Real('y2_{1}')\n".format(i,i))
        # f.write("yhat2_{0} = Real('yhat2_{1}')\n".format(i,i))

        # f.write("r1_{0} = Real('r1_{1}')\n".format(i,i))
        # f.write("r2_{0} = Real('r2_{1}')\n".format(i,i))
        for varcount in range(1,y_count+1):
            decl+="y"+str(varcount)+"_"+str(i)+" = Real('y"+str(varcount)+"_"+str(i)+"')\n"
            decl+="yhat"+str(varcount)+"_"+str(i)+" = Real('yhat"+str(varcount)+"_"+str(i)+"')\n"
            decl+="r"+str(varcount)+"_"+str(i)+" = Real('r"+str(varcount)+"_"+str(i)+"')\n"
            decl+="y"+str(varcount)+"_attack_"+str(i)+" = Real('y"+str(varcount)+"_"+str(i)+"')\n"

        # f.write("x1_{0} = Real('x1_{1}')\n".format(i,i))
        # f.write("xhat1_{0} = Real('xhat1_{1}')\n".format(i,i))
        # f.write("x2_{0} = Real('x2_{1}')\n".format(i,i))
        # f.write("xhat2_{0} = Real('xhat2_{1}')\n".format(i,i))

        # f.write("theta_{0} = Real('yr_{1}')\n".format(i,i))
        # f.write("omega_{0} = Real('yg_{1}')\n".format(i,i))
        for varcount in range(1,x_count+1):
            decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"
            decl+="xhat"+str(varcount)+"_"+str(i)+" = Real('xhat"+str(varcount)+"_"+str(i)+"')\n"
            decl+="x"+str(varcount)+"_abs_"+str(i)+" = Real('x"+str(varcount)+"_abs_"+str(i)+"')\n"

        # f.write("u_{0} = Real('u_{1}')\n".format(i,i))
        # f.write("u_attacked_{0} = Real('u_{1}')\n".format(i,i))
        for varcount in range(1,u_count+1):
            decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"
            decl+="u"+str(varcount)+"_attacked_"+str(i)+" = Real('u"+str(varcount)+"_attacked_"+str(i)+"')\n"
            decl+="u"+str(varcount)+"_attack_"+str(i)+" = Real('u"+str(varcount)+"_attack_"+str(i)+"')\n"
        

        f.write(decl)
        f.write("r_"+str(i)+" = Real('r_"+str(i)+"')\n")
        

    f.write("\n")
    # f.write("s.add(x1_0 == 0)\n")
    # f.write("s.add(x2_0 == 0)\n")
    # f.write("s.add(xhat1_0 == 0)\n")
    # f.write("s.add(xhat2_0 == 0)\n")
    # f.write("s.add(u_0 == 0)\n")
    # f.write("s.add(theta_0 == x2_0)\n")
    # f.write("s.add(omega_0 == x2_0)\n\n")
    for varcount in range(1,u_count+1):
        f.write("s.add(u"+str(varcount)+"_0 == 0)\n")
    for varcount in range(1,x_count+1):
        f.write("s.add(x"+str(varcount)+"_0 == 0)\n")
        f.write("s.add(xhat"+str(varcount)+"_0 == 0)\n")
        f.write("s.add(x"+str(varcount)+"_abs_0 == 0)\n")


    j = 0
    for i in range(K):
######################### writing equations for u #######################
        #f.write("s.add(u_{0} == ((-1)*k1*xhat1_{1}) + ((-1)*k2*xhat2_{2}) )\n".format(i,i,i))
        expr_u=""
        for varcount1 in range(1,u_count+1):
            expr_u+="s.add(u"+str(varcount1)+"_"+str(i)+" == "
            for varcount2 in range(1,x_count+1):
                expr_u+=" - ("+str(Gain[varcount1-1,varcount2-1])+"*xhat"+str(varcount2)+"_"+str(i)+")"
            expr_u+=")\n"
        f.write(expr_u)
###############################################################################
        if i == (j+index):
            f.write("attack1_{0} = Real('attack1_{1}')\n".format(i,i))
            #f.write("\ns.add(u_attacked_{0} == (u_{1} + attack1_{2}))\n".format(i,i,i))
############################ writing u attacked ###################################
            expr_uatk=""
            for varcount1 in range(1,u_count+1):
                expr_uatk+="s.add(u"+str(varcount1)+"_"+str(i)+" == u"+str(varcount1)+"_"+str(i)+"+ attack1_"+str(i)+"))\n"
            f.write(expr_u)
###################################################################################
            f.write("attack2_{0} = Real('attack2_{1}')\n".format(i,i))
            f.write("\ns.add(y1_{0} == (c11*x1_{1}) + (c12*x2_{2}) + attack2_{3})\n".format(i,i,i,i))
            j = j+1
            if j== attackLen:
                j=0      
        else:
            #f.write("\ns.add(u_attacked_{0} == u_{1})\n".format(i,i))
            f.write("\ns.add(y1_{0} == (c11*x1_{1}) + (c12*x2_{2}))\n".format(i,i,i))
            expr_uatk=""
            for varcount1 in range(1,u_count+1):
                expr_uatk+="s.add(u"+str(varcount1)+"_"+str(i)+" == u"+str(varcount1)+"_"+str(i)+"))\n"
            f.write(expr_u)
        f.write("s.add(y2_{0} == (c21*x1_{1}) + (c22*x2_{2}))\n".format(i,i,i))            

        f.write("s.add(yhat1_{0} == (c11*xhat1_{1}) + (c12*xhat2_{2}))\n".format(i,i,i))
        f.write("s.add(yhat2_{0} == (c21*xhat1_{1}) + (c22*xhat2_{2}))\n".format(i,i,i)) 

        f.write("s.add(r1_{0} == y1_{1} - yhat1_{2})\n".format(i,i,i))
        f.write("s.add(r2_{0} == y2_{1} - yhat2_{2})\n".format(i,i,i))
        f.write("s.add(p_{0} == If(r1_{1}<0,(-1)*r1_{2},r1_{3}))\n".format(i,i,i,i))
        f.write("s.add(q_{0} == If(r2_{1}<0,(-1)*r2_{2},r2_{3}))\n".format(i,i,i,i))
        f.write("s.add(r_{0} == If(p_{1}>q_{2},p_{3},q_{4}))\n".format(i,i,i,i,i))

        f.write("s.add(r_{0}<{1})\n".format(i,Th))
        
        f.write("s.add(x1_{0} == (a11*x1_{1}) + (a12*x2_{2}) + (b1*u_attacked_{3}))\n".format(i+1,i,i,i))        
        f.write("s.add(x2_{0} == (a21*x1_{1}) + (a22*x2_{2}) + (b2*u_attacked_{3}))\n".format(i+1,i,i,i))

        f.write("s.add(xhat2_{0} == (a21*xhat1_{1}) + (a22*xhat2_{2}) + (b2*u_{3}) + (l21*r1_{4}) + (l22*r2_{5}))\n".format(i+1,i,i,i,i,i))
        f.write("s.add(xhat1_{0} == (a11*xhat1_{1}) + (a12*xhat2_{2}) + (b1*u_{3}) + (l11*r1_{4}) + (l12*r2_{5}))\n".format(i+1,i,i,i,i,i))        

        f.write("s.add(theta_{0} == If(x1_{1}<0,(-1)*x1_{2},x1_{3}))\n".format(i+1,i+1,i+1,i+1))
        f.write("s.add(omega_{0} == If(x2_{1}<0,(-1)*x2_{2},x2_{3}))\n".format(i+1,i+1,i+1,i+1))       


    f.write("s.add(Or(")
    for i in range(K):
        f.write("theta_{0}>{1},omega_{2}>{3}".format(i,safeTheta,i,safeOmega))
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

    f.write("\t\tif \"attack1\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tattack1[i] = float(y)\n")

    f.write("\t\telif \"attack2\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tattack2[i] = float(y)\n")

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

    f.write("\t\telif \"y1_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\ty1[i] = float(y)\n")

    f.write("\t\telif \"y2_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\ty2[i] = float(y)\n")

    f.write("\t\telif \"yhat1_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tyhat1[i] = float(y)\n")

    f.write("\t\telif \"yhat2_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tyhat2[i] = float(y)\n")

    
    f.write("\t\telif \"r_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tr[i] = float(y)\n")

    f.write("\t\telif \"theta_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\ttheta[i] = float(y)\n")

    f.write("\t\telif \"omega_\" in d.name():\n")
    f.write("\t\t\ti = int(d.name().split('_')[1])\n")
    f.write("\t\t\tx = str(m[d])\n")
    f.write("\t\t\tindex = x.find(\"?\")\n")
    f.write("\t\t\tif index != -1:\n")
    f.write("\t\t\t\ty = x[:-1]\n")
    f.write("\t\t\telse:\n")
    f.write("\t\t\t\ty = x\n")
    f.write("\t\t\tomega[i] = float(y)\n")
    
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
    f.write("\t\tprint(\"attack1_{0}={1}\".format(i,attack1[i]))\n")
    f.write("\t\tprint(\"attack2_{0}={1}\".format(i,attack2[i]))\n")

    f.write("\t\tprint(\"x1_{0}={1}\".format(i,x1[i]))\n")
    f.write("\t\tprint(\"x2_{0}={1}\".format(i,x2[i]))\n")
    f.write("\t\tprint(\"xhat1_{0}={1}\".format(i,xhat1[i]))\n")
    f.write("\t\tprint(\"xhat2_{0}={1}\".format(i,xhat2[i]))\n")

    f.write("\t\tprint(\"u_{0}={1}\".format(i,u[i]))\n")

    f.write("\t\tprint(\"y1_{0}={1}\".format(i,y1[i]))\n")
    f.write("\t\tprint(\"y2_{0}={1}\".format(i,y2[i]))\n")
    f.write("\t\tprint(\"yhat1_{0}={1}\".format(i,yhat1[i]))\n")
    f.write("\t\tprint(\"yhat2_{0}={1}\".format(i,yhat2[i]))\n")

    f.write("\t\tprint(\"r_{0}={1}\".format(i,r[i]))\n")
    f.write("\t\tprint(\"theta_{0}={1}\\n\".format(i,theta[i]))\n")
    f.write("\t\tprint(\"omega_{0}={1}\\n\".format(i,omega[i]))\n")

    f.write("print(\"attack on control signal\")\n")
    f.write("print(attack1)\n")
    f.write("print(\"attack on theta\")\n")
    f.write("print(attack2)\n")
    f.write("print(\"u\")\n")
    f.write("print(u)\n")

    f.write("if isSat==1:\n")
    f.write("\tf0 = open(\"powersystemresult_new.txt\", \"w+\")\n")
    f.write("\tf0.write(\"1\")\n")
    f.write("\tf0.close()\n")

    f.write("f1 = open(\"actuatorAttackVector_new.csv\", \"w+\")\n")
    f.write("for i in range({0}):\n".format(attackLen))
    f.write("\tf1.write(\"{0}\".format(attack1[i]))\n")
    f.write("\tif i != {0}-1:\n".format(attackLen))
    f.write("\t\tf1.write(\",\")\n")
    f.write("f1.close()\n")

    f.write("f2 = open(\"thetaAttackVector_new.csv\", \"w+\")\n")
    f.write("for i in range({0}):\n".format(attackLen))
    f.write("\tf2.write(\"{0}\".format(attack2[i]))\n")
    f.write("\tif i != {0}-1:\n".format(attackLen))
    f.write("\t\tf2.write(\",\")\n")
    f.write("f2.close()") 

    f.close()
    os.system("python powersystem_new.py>powersystem_new.out")

    f0 = open("powersystemresult_new.txt","r")
    if f0.mode == 'r':
        content = f0.read()
        isSat = int(content)
    f0.close()

    index = index + 1
    isSat=1