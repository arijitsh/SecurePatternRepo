import os
import numpy as np

A= np.matrix('0.66 0.53; -0.53 0.13')
B= np.matrix('0.34; 0.53')
C= np.matrix('1 1; 1 1')
D= np.matrix('0 ; 0')
K= np.matrix('0.0556 0.3306')
L= np.matrix('0.36 0.27;  -0.31 0.08')


safeTheta = 0.1
safeOmega = 0.05
th = 0.03
startpoint=0
K=15
attackLen=7
pattern= 1
#rpt=K/length(pattern)

drop = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
start = 0
index = start
isSat = 0
modelName= "powersystem"
filename= modelName+"_"+str(th)+"_"+str(startpoint)+"_"+str(attackLen)+"_"+str(K)+"_"+str(pattern)+"_old.c"
try:
    f = open(filename, "w+");
    f.write("#include<stdio.h>\n");
    f.write("#include<math.h>\n");
    f.write("#include<inttypes.h>\n");
    f.write("#include \"library.h\"\n");
    f.write("float nondet_float();\n");
    f.write("int8_t nondet_int8();\n");
    f.write("int const K ="+str(K)+",attackLen = "+str(attackLen)+", startpoint = "+str(startpoint)+";\n")
    f.write("int main()\n");
    f.write("\t{\n");
    f.write("\t\tfloat r1[K], r2[K], r[K], theta[K], omega[K], a1[K], a2[K], ");
    for counter in range(0,K+1):
        f.write("x1_"+str(counter)+" = 0, x2_"+str(counter)+" = 0, u_"+str(counter)+" = 0, u_attacked_"+str(counter)+" = 0, y1_"+str(counter)+" = 0, y2_"+str(counter)+" = 0, z1_"+str(counter)+" = 0, z2_"+str(counter)+" = 0,x1next_"+str(counter)+" = 0, x2next_"+str(counter)+" = 0, z1next_"+str(counter)+" = 0, z2next_"+str(counter)+" = 0");
        if counter!=K:
            f.write(",");
        else :
            f.write(";\n");
        ##end of if else
    f.write("\t\tint8_t syn = 0;\n\n");
    #end of for
    for counter in range(K+1):
        f.write("\t\t//pattern="+str(drop[counter])+";\n");
        if index+startpoint == counter :
            f.write("\t\tsyn = nondet_int8();\n");
            f.write("\t\ta1["+str(counter)+"] = AttackFormat2(syn);\n");
            f.write("\t\tsyn = nondet_int8();\n");
            f.write("\t\ta2["+str(counter)+"] = AttackFormat2(syn);\n");
            index=index+1
            if index==attackLen:
                index = 0
            #end of if
        else:
            f.write("\t\ta1["+str(counter)+"] = 0;\n")
            f.write("\t\ta2["+str(counter)+"] = 0;\n")
        ##end of if else
        if drop[counter]:
            f.write("\t\tu_"+str(counter)+" = -(0.0556*z1_"+str(counter)+") - (0.3306*z2_"+str(counter)+");\n");
            f.write("\t\tu_attacked_"+str(counter)+" = u_"+str(counter)+" + a1["+str(counter)+"];\n");
            f.write("\t\ty1_"+str(counter)+" = x1_"+str(counter)+" + a2["+str(counter)+"];\n");
            f.write("\t\ty2_"+str(counter)+" = x2_"+str(counter)+";\n");
            f.write("\t\tr1["+str(counter)+"] = y1_"+str(counter)+" - z1_"+str(counter)+";\n");
            f.write("\t\tr2["+str(counter)+"] = y2_"+str(counter)+" - z2_"+str(counter)+";\n");
            f.write("\t\tr["+str(counter)+"] = max(absolute(r1["+str(counter)+"]),absolute(r2["+str(counter)+"]));\n");
            f.write("\t\tz1_"+str(counter+1)+" = (0.66*z1_"+str(counter)+") + (0.53*z2_"+str(counter)+") + (0.34*u_"+str(counter)+") + (0.36*r1["+str(counter)+"]) + (0.27*r2["+str(counter)+"]);\n");
            f.write("\t\tz2_"+str(counter+1)+" = -(0.53*z1_"+str(counter)+") + (0.13*z2_"+str(counter)+") + (0.53*u_"+str(counter)+") - (0.31*r1["+str(counter)+"]) + (0.08*r2["+str(counter)+"]);\n");
            f.write("\t\tx1_"+str(counter+1)+" = (0.66*x1_"+str(counter)+") + (0.53*x2_"+str(counter)+") + (0.34*u_attacked_"+str(counter)+");\n");
            f.write("\t\tx2_"+str(counter+1)+" = - (0.53*x1_"+str(counter)+") + (0.13*x2_"+str(counter)+") + (0.53*u_attacked_"+str(counter)+");\n");
        else:
            f.write("\t\tu_"+str(counter)+" = u_"+str(counter-1)+";\n");
            f.write("\t\tu_attacked_"+str(counter)+" = u_attacked_"+str(counter-1)+";\n");
            f.write("\t\tz1_"+str(counter+1)+" = (0.66*z1_"+str(counter)+") + (0.53*z2_"+str(counter)+") + (0.34*u_"+str(counter)+");\n");
            f.write("\t\tz2_"+str(counter+1)+" = -(0.53*z1_"+str(counter)+") + (0.13*z2_"+str(counter)+") + (0.53*u_"+str(counter)+");\n");
            f.write("\t\tx1_"+str(counter+1)+" = (0.66*x1_"+str(counter)+") + (0.53*x2_"+str(counter)+") + (0.34*u_attacked_"+str(counter)+");\n");
            f.write("\t\tx2_"+str(counter+1)+" = - (0.53*x1_"+str(counter)+") + (0.13*x2_"+str(counter)+") + (0.53*u_attacked_"+str(counter)+");\n");
        ##end of if else
        f.write("\t\ttheta["+str(counter)+"] = absolute(x1_"+str(counter+1)+");\n");
        f.write("\t\tomega["+str(counter)+"] = absolute(x2_"+str(counter+1)+");\n\n");
    ###end of for
    f.write("\n\t\tassert((");
    for counter in range(0,K):
        if drop[counter]:
            f.write("(r["+str(counter)+"]>"+str(th)+")");
            if counter!=(K-1):
                f.write(" || ");
            #end of if
        ##end of if
    ###end of for

    f.write(")||(");

    for counter in range(0,K):
        f.write("(theta["+str(counter)+"]<=0.1 && omega["+str(counter)+"]<=0.05)");
        if counter!=(K-1):
            f.write(" && ");
        #end of if
    ##end of for
    f.write("));\n");

    f.write("\t\treturn 0;\n");
    f.write("\t}");
    #os.system("gcc input.c");
    #os.system("nohup ./cbmc powersys_th_09.c --trace &>powersys_th_09.out")
finally:
    f.close()
