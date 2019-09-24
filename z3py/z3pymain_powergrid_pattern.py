# Controller type: PID
import os
import numpy as np
import errno

modelName= "powergrid"
A= np.matrix('-1 -3;3 -5')
B= np.matrix('2 -1;1 0')
C= np.matrix('0.8 2.4;1.6 0.8')
D= np.matrix('0 0; 0 0')
Gain= np.matrix('2.9846   -4.9827;6.9635   -6.9599')
L= np.matrix('-1.1751   -0.1412;-2.6599    2.2549')
safex = [0.05,0.15]
th = 0.03
################## creating the path to save results #################
path="../results/z3/"+modelName+"/"
try:
    os.makedirs(path)
except OSError as err:
    if err.errno!= errno.EEXIST:
        raise
#####################################################################
u_count=B.shape[1]
x_count=A.shape[1]
y_count=C.shape[0]

u_attack_map = np.zeros(u_count,dtype=float)
y_attack_map = np.zeros(y_count,dtype=float)

####### Configure which sensor/control input to attack ########
u_attack_map[0] = 1
y_attack_map[0] = 1

attackLen=1
pattern= 1
offset = 5
start = 0
isSat = 0

#Compute pattern length
patternLen=0
patternTemp = pattern
while(patternTemp>0):
    patternLen=patternLen+1
    patternTemp=patternTemp//10

#Compute pattern array
patternArray = np.zeros((patternLen), dtype=int)
patternTemp = pattern
i = patternLen-1
while patternTemp>0:
    patternArray[i] = patternTemp%10
    patternTemp=patternTemp//10
    i = i-1

print("pattern:"+str(pattern))
print("pattern length:"+str(patternLen))

f0 = open(path+modelName+".z3result", "w+")
f0.write("0")
f0.close()

while isSat == 0:  
    index = start
    while (index<patternLen) and (isSat == 0):
        # create drop pattern
        K = index + attackLen + offset
        dropPattern = np.ones((K), dtype=int)
        j=0
        if pattern!=1:
            for i in range(K):
                dropPattern[i] = patternArray[j]
                j = j + 1
                if j == patternLen:
                    j = 0
        print("drop pattern:")
        print(dropPattern)

        fileName = modelName + "_"+str(index)+"_"+str(attackLen)+"_"+str(K)+".py"
        f = open(path+fileName, "w+")
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
            f.write("z"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        for varcount in range(1,y_count+1):
            f.write("y"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
            f.write("attackOnY"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
            f.write("r"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        for varcount in range(1,u_count+1):
            f.write("u"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
            f.write("attackOnU"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
        f.write("r = np.zeros("+str(K+1)+", dtype=float)\n")
 
        for i in range(K+1):
            decl=""
            for varcount in range(1,y_count+1):
                decl+="y"+str(varcount)+"_"+str(i)+" = Real('y"+str(varcount)+"_"+str(i)+"')\n"
                decl+="r"+str(varcount)+"_"+str(i)+" = Real('r"+str(varcount)+"_"+str(i)+"')\n"
                decl+="rabs"+str(varcount)+"_"+str(i)+" = Real('rabs"+str(varcount)+"_"+str(i)+"')\n"

            for varcount in range(1,x_count+1):
                decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"
                decl+="z"+str(varcount)+"_"+str(i)+" = Real('z"+str(varcount)+"_"+str(i)+"')\n"
                decl+="x"+str(varcount)+"_abs_"+str(i)+" = Real('x"+str(varcount)+"_abs_"+str(i)+"')\n"

            for varcount in range(1,u_count+1):
                decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"
                decl+="u"+str(varcount)+"_attacked_"+str(i)+" = Real('u"+str(varcount)+"_attacked_"+str(i)+"')\n"

            decl+="r_"+str(i)+" = Real('r_"+str(i)+"')\n"
            f.write(decl)
            
        f.write("\n")
        for varcount in range(1,u_count+1):
            f.write("s.add(u"+str(varcount)+"_0 == 0)\n")
        for varcount in range(1,x_count+1):
            f.write("s.add(x"+str(varcount)+"_0 == 0)\n")
            f.write("s.add(z"+str(varcount)+"_0 == 0)\n")
            f.write("s.add(x"+str(varcount)+"_abs_0 == 0)\n")
        f.write("\n")

        j = 0
        for i in range(K):
    ######################### writing equations for u #######################
            expr_u=""
            for varcount1 in range(1,u_count+1):
                expr_u+="s.add(u"+str(varcount1)+"_"+str(i)+" == "
                for varcount2 in range(1,x_count+1):
                    expr_u+=" - ("+str(Gain[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+")"
                expr_u+=")\n"
            f.write(expr_u)
    ###############################################################################
            if i == (j+index):            
    ############################ writing u attacked ###################################
                expr_uatk=""
                for varcount1 in range(1,u_count+1):
                    f.write("u"+str(varcount1)+"_attack_"+str(i)+" = Real('u"+str(varcount1)+"_attack_"+str(i)+"')\n")
                    expr_uatk+="s.add(u"+str(varcount1)+"_attacked_"+str(i)+" == u"+str(varcount1)+"_"+str(i)+"+ ("+str(u_attack_map[varcount1-1])+"*u"+str(varcount1)+"_attack_"+str(i)+"))\n"
                f.write(expr_uatk)
    ###################################################################################

                expr_y=""
                expr_r=""
                for varcount1 in range(1,y_count+1):
                    f.write("y"+str(varcount1)+"_attack_"+str(i)+" = Real('y"+str(varcount1)+"_attack_"+str(i)+"')\n")
                    expr_y+="s.add(y"+str(varcount1)+"_"+str(i)+" == ("+str(y_attack_map[varcount1-1])+"*y"+str(varcount1)+"_attack_"+str(i)+")"
                    expr_r+="s.add(r"+str(varcount1)+"_"+str(i)+" == y"+str(varcount1)+"_"+str(i)
                    for varcount2 in range(1,x_count+1):
                        expr_y+=" + ("+str(C[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+")"
                        expr_r+=" - ("+str(C[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+")"
                    for varcount3 in range(1,u_count+1):
                        expr_y+=" + ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+")"         
                        expr_r+=" - ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_attacked_"+str(i)+")"   
                    expr_y+=")\n"
                    expr_r+=")\n"
                f.write(expr_y)
                f.write(expr_r)
                j = j+1
                if j== attackLen:
                    j=0      
            else:
                expr_uatk=""
                for varcount1 in range(1,u_count+1):
                    expr_uatk+="s.add(u"+str(varcount1)+"_attacked_"+str(i)+" == u"+str(varcount1)+"_"+str(i)+")\n"
                f.write(expr_uatk)
                expr_y=""
                expr_r=""
                for varcount1 in range(1,y_count+1):
                    expr_y+="s.add(y"+str(varcount1)+"_"+str(i)+" == "
                    expr_r+="s.add(r"+str(varcount1)+"_"+str(i)+" == y"+str(varcount1)+"_"+str(i)
                    for varcount2 in range(1,x_count+1):
                        expr_y+=" + ("+str(C[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+")"
                        expr_r+=" - ("+str(C[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+")"
                    for varcount3 in range(1,u_count+1):
                        expr_y+=" + ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+")"         
                        expr_r+=" - ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_attacked_"+str(i)+")"   
                    expr_y+=")\n"
                    expr_r+=")\n"
                f.write(expr_y)
                f.write(expr_r)

            expr_rabs = ""
            expr_r = "s.add(r_"+str(i)+" ==" 
            for varcount1 in range(1,y_count+1):
                expr_rabs+= "s.add(rabs"+str(varcount1)+"_"+str(i)+" == If(r"+str(varcount1)+"_"+str(i)+"<0,(-1)*r"+str(varcount1)+"_"+str(i)+",r"+str(varcount1)+"_"+str(i)+"))\n"
                expr_r+="rabs"+str(varcount1)+"_"+str(i)+" +"
            expr_r = expr_r[:len(expr_r)-1] 
            expr_r+=")\n"
            f.write(expr_rabs)
            f.write(expr_r)
            
            f.write("s.add(r_{0}<{1})\n".format(i,th))          
            
            expr_x=""
            expr_z=""
            for varcount1 in range(1,x_count+1):
                expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "
                expr_z+="s.add(z"+str(varcount1)+"_"+str(i+1)+" == "
                for varcount2 in range(1,x_count+1):
                    expr_x+=" ("+str(A[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+") +"
                    expr_z+=" ("+str(A[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+") +"
                for varcount3 in range(1,u_count+1):
                    expr_z+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
                    expr_x+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_attacked_"+str(i)+") +"
                for varcount4 in range(1,y_count+1):
                    expr_z+=" ("+str(L[varcount1-1,varcount4-1])+"*r"+str(varcount4)+"["+str(i)+"]) +"
                expr_x=expr_x[:len(expr_x)-1] 
                expr_x = expr_x + ")\n"
                expr_z=expr_z[:len(expr_z)-1] 
                expr_z = expr_z + ")\n"            

            f.write(expr_z)
            f.write(expr_x)
            
        f.write("s.add(Or(")
        assertion=""
        for varcount in range(1,x_count+1):
            for i in range(K):
                assertion+="x"+str(varcount)+"_abs_"+str(i)+">"+str(safex[varcount-1])+","
        assertion = assertion[:len(assertion)-1]
        f.write(assertion)
        f.write("))\n")

        # f.write("\nprint(s.sexpr())")
        f.write("\nif s.check() != sat:\n")
        f.write("\tprint(s.check())\n")
        f.write("\tisSat = 0\n")
        f.write("else:\n")
        f.write("\tprint( \"sat\")\n")
        f.write("\tprint(s.check())\n")
        f.write("\tisSat = 1\n")
        f.write("\tm = s.model()\n")
        f.write("\tfor d in m.decls():\n")
        f.write("\t\tprint (\"%s = %s\" % (d.name(), m[d]))\n")
        
        f.write("if isSat==1:\n")
        f.write("\tf0 = open(\""+path+modelName+".z3result\", \"w+\")\n")
        f.write("\tf0.write(\"1\")\n")
        f.write("\tf0.close()\n")        

        f.close()
        os.system("python "+path+fileName+">"+path+fileName+".z3out")

        f0 = open(path+modelName+".z3result", "r")
        if f0.mode == 'r':
            content = f0.read()
            isSat = int(content)
        f0.close()

        index = index + 1
        isSat = 1 #remove this once done
        
    attackLen = attackLen + 1