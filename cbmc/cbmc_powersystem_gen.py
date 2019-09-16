import os

A= []
safeTheta = 0.1
safeOmega = 0.05
Th = 0.03
startpoint=0
K=15
attackLen=7
drop = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
start = 0
index = start
isSat = 0
try:
    f = open("powerSystem_0.0355_0_5_9_10.c", "w+");
    f.write("#include<stdio.h>\n");
    f.write("#include<math.h>\n");
    f.write("#include<inttypes.h>\n");
    f.write("#include \"library.h\"\n");
    f.write("float nondet_float();\n");
    f.write("int8_t nondet_int8();\n");
    f.write("int const K ="+K+",attackLen = "+attackLen+", startpoint = "+startpoint+";\n")
    f.write("int main()\n");
    f.write("\t{\n");
    f.write("\t\tfloat r1[K], r2[K], r[K], theta[K], omega[K], a1[K], a2[K], ");
    for counter in range(0,K+1):
        f.write("x1_"+counter+" = 0, x2_"+counter+" = 0, u_"+counter+" = 0, u_attacked_"+counter+" = 0, y1_"+counter+" = 0, y2_"+counter+" = 0, z1_"+counter+" = 0, z2_"+counter+" = 0,x1next_"+counter+" = 0, x2next_"+counter+" = 0, z1next_"+counter+" = 0, z2next_"+counter+" = 0");
        if counter!=K:
            f.write(",");
        else :
            f.write(";\n");
        ##end of if else
    f.write("\t\tint8_t syn = 0;\n\n");
    #end of for
    for counter in range(K+1):
        f.write("\t\t//pattern="+drop[counter]+";\n");
        if index+startpoint == counter :
            f.write("\t\tsyn = nondet_int8();\n");
            f.write("\t\ta1["+counter+"] = AttackFormat2(syn);\n");
            f.write("\t\tsyn = nondet_int8();\n");
            f.write("\t\ta2["+counter+"] = AttackFormat2(syn);\n");
            index=index+1
            if index==attackLen:
                index = 0
            #end of if
        else:
            f.write("\t\ta1["+counter+"] = 0;\n")
            f.write("\t\ta2["+counter+"] = 0;\n")
        ##end of if else
        if drop[counter]:
            f.write("\t\tu_"+counter+" = -(0.0556*z1_"+counter+") - (0.3306*z2_"+counter+");\n",counter,counter,counter);
            f.write("\t\tu_attacked_"+counter+" = u_"+counter+" + a1["+counter+"];\n",counter,counter,counter);
            f.write("\t\ty1_"+counter+" = x1_"+counter+" + a2["+counter+"];\n",counter,counter,counter);
            f.write("\t\ty2_"+counter+" = x2_"+counter+";\n",counter,counter);
            f.write("\t\tr1["+counter+"] = y1_"+counter+" - z1_"+counter+";\n",counter,counter,counter);
            f.write("\t\tr2["+counter+"] = y2_"+counter+" - z2_"+counter+";\n",counter,counter,counter);
            f.write("\t\tr["+counter+"] = max(absolute(r1["+counter+"]),absolute(r2["+counter+"]));\n",counter,counter,counter);
            f.write("\t\tz1_"+counter+" = (0.66*z1_"+counter+") + (0.53*z2_"+counter+") + (0.34*u_"+counter+") + (0.36*r1["+counter+"]) + (0.27*r2["+counter+"]);\n",counter+1,counter,counter,counter,counter,counter);
            f.write("\t\tz2_"+counter+" = -(0.53*z1_"+counter+") + (0.13*z2_"+counter+") + (0.53*u_"+counter+") - (0.31*r1["+counter+"]) + (0.08*r2["+counter+"]);\n",counter+1,counter,counter,counter,counter,counter);
            f.write("\t\tx1_"+counter+" = (0.66*x1_"+counter+") + (0.53*x2_"+counter+") + (0.34*u_attacked_"+counter+");\n",counter+1,counter,counter,counter);
            f.write("\t\tx2_"+counter+" = - (0.53*x1_"+counter+") + (0.13*x2_"+counter+") + (0.53*u_attacked_"+counter+");\n",counter+1,counter,counter,counter);
        else:
            f.write("\t\tu_"+counter+" = u_"+counter+";\n",counter,counter-1);
            f.write("\t\tu_attacked_"+counter+" = u_attacked_"+counter+";\n",counter,counter-1);
            f.write("\t\tz1_"+counter+" = (0.66*z1_"+counter+") + (0.53*z2_"+counter+") + (0.34*u_"+counter+");\n",counter+1,counter,counter,counter);
            f.write("\t\tz2_"+counter+" = -(0.53*z1_"+counter+") + (0.13*z2_"+counter+") + (0.53*u_"+counter+");\n",counter+1,counter,counter,counter);
            f.write("\t\tx1_"+counter+" = (0.66*x1_"+counter+") + (0.53*x2_"+counter+") + (0.34*u_attacked_"+counter+");\n",counter+1,counter,counter,counter);
            f.write("\t\tx2_"+counter+" = - (0.53*x1_"+counter+") + (0.13*x2_"+counter+") + (0.53*u_attacked_"+counter+");\n",counter+1,counter,counter,counter);
        ##end of if else
        f.write("\t\ttheta["+counter+"] = absolute(x1_"+counter+1+");\n");
        f.write("\t\tomega["+counter+"] = absolute(x2_"+counter+1+");\n\n");
    ###end of for
	f.write("\n\t\tassert((");
    for counter in range(0,K):
        if drop[counter]:
            f.write("(r["+counter+"]>"+th+")");
            if counter!=(K-1):
                f.write(" || ");
            #end of if
        ##end of if
    ###end of for

    f.write(")||(");

    for counter in range(0,K):
        f.write("(theta["+counter+"]<=0.1 && omega["+counter+"]<=0.05)");
        if counter!=(K-1):
            f.write(" && ");
        #end of if
    ##end of for
    f.write("));\n");

    f.write("\t\treturn 0;\n");
    f.write("\t}");
    os.system("gcc input.c");
    os.system("nohup ./cbmc powersys_th_09.c --trace &>powersys_th_09.out")
finally:
    f.close()
