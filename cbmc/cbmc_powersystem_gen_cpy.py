import os
import numpy as np

modelName= "powersystem"
A= np.matrix('0.66 0.53; -0.53 0.13')
B= np.matrix('0.34; 0.53')
C= np.matrix('1 1; 1 1')
D= np.matrix('0 ; 0')
K= np.matrix('0.0556 0.3306')
L= np.matrix('0.36 0.27;  -0.31 0.08')

u_count=B.shape[1]
x_count=A.shape[1]
y_count=C.shape[0]

safex = [0.1,0.05]
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

filename= modelName+"_"+str(th)+"_"+str(startpoint)+"_"+str(attackLen)+"_"+str(K)+"_"+str(pattern)+".c"
try:
    f = open(filename, "w+");
    f.write("#include<stdio.h>\n");
    f.write("#include<math.h>\n");
    f.write("#include<inttypes.h>\n");
    f.write("#include \"library.h\"\n");
    f.write("float nondet_float();\n");
    f.write("int8_t nondet_int8();\n");
    f.write("int const K ="+str(K)+",attackLen = "+str(attackLen)+", startpoint = "+str(startpoint)+";\n")
    f.write("int main()\n")
    f.write("\t{\n");
    f.write("\t\tfloat r[K], a1[K], a2[K], ");
    for varcount in range(1,x_count+1):
        f.write("x"+str(varcount)+"_abs[K],")
    for varcount in range(1,y_count+1):
        f.write("r"+str(varcount)+"[K],")
    decl=""
    for counter in range(0,K+1):
        for varcount in range(1,x_count+1):
            decl+="x"+str(varcount)+"_"+str(counter)+" = 0, z"+str(varcount)+"_"+str(counter)+" = 0,"
            decl+="x"+str(varcount)+"next_"+str(counter)+" = 0, z"+str(varcount)+"next_"+str(counter)+" = 0,"
        for varcount in range(1,u_count+1):
            decl+="u"+str(varcount)+"_"+str(counter)+" = 0, u"+str(varcount)+"_attacked_"+str(counter)+" = 0,"
        for varcount in range(1,y_count+1):
            decl+="y"+str(varcount)+"_"+str(counter)+" = 0, "
        #f.write("x1_"+str(counter)+" = 0, x2_"+str(counter)+" = 0, u_"+str(counter)+" = 0, u_attacked_"+str(counter)+" = 0, y1_"+str(counter)+" = 0, y2_"+str(counter)+" = 0, z1_"+str(counter)+" = 0, z2_"+str(counter)+" = 0,x1next_"+str(counter)+" = 0, x2next_"+str(counter)+" = 0, z1next_"+str(counter)+" = 0, z2next_"+str(counter)+" = 0");
        
        if counter!=K:
            f.write(decl)
            f.write(",")
        else :
            decl=decl[:len(decl)-2]             #removing last comma
            f.write(decl)
            f.write(";\n")
        ##end of if else
    #end of for
    f.write("\t\tint8_t syn = 0;\n\n");
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
            # end of if
        else:
            f.write("\t\ta1["+str(counter)+"] = 0;\n")
            f.write("\t\ta2["+str(counter)+"] = 0;\n")
        ## end of if else

        if drop[counter]:
            
######################### writing equations for u,u attacked #######################
            #f.write("\t\tu_"+str(counter)+" = -(0.0556*z1_"+str(counter)+") - (0.3306*z2_"+str(counter)+");\n");
            #f.write("\t\tu_attacked_"+str(counter)+" = u_"+str(counter)+" + a1["+str(counter)+"];\n");
            expr_u=""
            expr_uatk=""
            for varcount1 in range(1,u_count+1):
                expr_u+="\t\tu"+str(varcount1)+"_"+str(counter)+" ="
                for varcount2 in range(1,x_count+1):
#                    expr_u+="-("+str(K[varcount1,varcount2])+"*z"+str(varcount2)+"_"+str(counter)+")"
#               end of for
                expr_u+=";\n"
                expr_uatk+="\t\tu"+str(varcount1)+"_attacked_"+str(counter)+" = u"+str(varcount1)+"_"+str(counter)+" + a1["+str(counter)+"];\n"
            ## end of for
            f.write(expr_u)
            f.write(expr_uatk)
###############################################################################
############################ writing equations for y,r,rabs ########################
            #f.write("\t\ty1_"+str(counter)+" = x1_"+str(counter)+" + a2["+str(counter)+"];\n");
            #f.write("\t\ty2_"+str(counter)+" = x2_"+str(counter)+";\n");
            #f.write("\t\tr1["+str(counter)+"] = y1_"+str(counter)+" - z1_"+str(counter)+";\n");
            #f.write("\t\tr2["+str(counter)+"] = y2_"+str(counter)+" - z2_"+str(counter)+";\n");
            #f.write("\t\tr["+str(counter)+"] = max(absolute(r1["+str(counter)+"]),absolute(r2["+str(counter)+"]));\n");
            expr_y=""
            expr_r=""
            expr_rabs="\t\tr["+str(counter)+"] = max("
            for varcount1 in range(1,y_count+1):
                expr_y+="\t\ty"+str(varcount1)+"_"+str(counter)+" = "
                expr_r+="\t\tr"+str(varcount1)+"["+str(counter)+"] = y"+str(varcount1)+"_"+str(counter)
                expr_rabs+="absolute(r"+str(varcount1)+"["+str(counter)+"]),"
                for varcount2 in range(1,x_count+1):
                    expr_y+="+("+str(C[varcount1,varcount2])+"*x"+str(varcount2)+"_"+str(counter)+")"
                    expr_r+="-("+str(C[varcount1,varcount2])+"*z"+str(varcount2)+"_"+str(counter)+")"
                # end of for 
                for varcount3 in range(1,u_count+1):
                    expr_y+="+("+str(D[varcount1,varcount3])+"*u"+str(varcount3)+"_"+str(counter)+")"
                    expr_r+="-("+str(D[varcount1,varcount3])+"*u"+str(varcount3)+"_attacked_"+str(counter)+")"
                # end of for 
                expr_rabs=expr_rabs[:len(expr_rabs)-2]          #removing last comma
                expr_rabs=");\n"
                expr_y+=";\n"
                expr_r+=";\n"
            ## end of for
            f.write(expr_y)
            f.write(expr_r)
            f.write(expr_rabs)
##################################################################################
########################### writing equations for x,z ############################
            #f.write("\t\tz1_"+str(counter+1)+" = (0.66*z1_"+str(counter)+") + (0.53*z2_"+str(counter)+") + (0.34*u_"+str(counter)+") + (0.36*r1["+str(counter)+"]) + (0.27*r2["+str(counter)+"]);\n");
            #f.write("\t\tz2_"+str(counter+1)+" = -(0.53*z1_"+str(counter)+") + (0.13*z2_"+str(counter)+") + (0.53*u_"+str(counter)+") - (0.31*r1["+str(counter)+"]) + (0.08*r2["+str(counter)+"]);\n");
            #f.write("\t\tx1_"+str(counter+1)+" = (0.66*x1_"+str(counter)+") + (0.53*x2_"+str(counter)+") + (0.34*u_attacked_"+str(counter)+");\n");
            #f.write("\t\tx2_"+str(counter+1)+" = - (0.53*x1_"+str(counter)+") + (0.13*x2_"+str(counter)+") + (0.53*u_attacked_"+str(counter)+");\n");
            
            expr_x=""
            expr_z=""
            for varcount1 in range(1,x_count+1):
                expr_x+="\t\tx"+str(varcount1)+"_"+str(counter+1)+" = "
                expr_z+="\t\tz"+str(varcount1)+"_"+str(counter+1)+" = "
                for varcount2 in range(1,x_count+1):
                    expr_x+="+("+str(A[varcount1,varcount2])+"*x"+str(varcount2)+"_"+str(counter)+")"
                    expr_z+="+("+str(A[varcount1,varcount2])+"*z"+str(varcount2)+"_"+str(counter)+")"
                # end of for 
                for varcount3 in range(1,u_count+1):
                    expr_x+="+("+str(B[varcount1,varcount3])+"*u"+str(varcount3)+"_"+str(counter)+")"
                    expr_z+="+("+str(B[varcount1,varcount3])+"*u"+str(varcount3)+"_attacked_"+str(counter)+")"
                # end of for 
                expr_x+=";\n"
                expr_z+=";\n"
            ## end of for
            f.write(expr_z)
            f.write(expr_x)
#################################################################################
        else:
######################### writing equations for u,u attacked #######################
            #f.write("\t\tu_"+str(counter)+" = u_"+str(counter-1)+";\n");
            #f.write("\t\tu_attacked_"+str(counter)+" = u_attacked_"+str(counter-1)+";\n");
            expr_u=""
            expr_uatk=""
            for varcount1 in range(1,u_count+1):
                expr_u+="\t\tu"+str(varcount1)+"_"+str(counter)+" = u_"+str(counter-1)+";\n"
                expr_uatk+="\t\tu"+str(varcount1)+"_attacked_"+str(counter)+" = u_attacked_"+str(counter-1)+";\n"
                # dropped---------------------------
                #for varcount2 in range(1,x_count+1):
                #    expr_u+="-("+K[varcount1,varcount2]+"*z"+str(varcount2)+"_"+str(counter)+")"
                # end of for
            ## end of for
            f.write(expr_u)
            f.write(expr_uatk)
###############################################################################
############################ writing equations for y,r,rabs ########################
            #f.write("\t\tr1["+str(counter)+"] = y1_"+str(counter)+" - z1_"+str(counter)+";\n");
            #f.write("\t\tr2["+str(counter)+"] = y2_"+str(counter)+" - z2_"+str(counter)+";\n");
            #f.write("\t\tr["+str(counter)+"] = max(absolute(r1["+str(counter)+"]),absolute(r2["+str(counter)+"]));\n");
            #expr_y=""
            expr_r=""
            expr_rabs="\t\tr["+str(counter)+"] = max("
            for varcount1 in range(1,y_count+1):
                #expr_y+="\t\ty"+str(varcount1)+"_"+str(counter)+" = "
                expr_r+="\t\tr"+str(varcount1)+"["+str(counter)+"] = r"+str(varcount1)+"["+str(counter-1)+"]"
                expr_rabs+="absolute(r"+str(varcount1)+"["+str(counter)+"]),"
                # drop ---------------------------------------------------------
                #for varcount2 in range(1,x_count+1):
                    #expr_y+="+("+C[varcount1,varcount2]+"*x"+str(varcount2)+"_"+str(counter)+")"
                    #expr_r+="-("+C[varcount1,varcount2]+"*z"+str(varcount2)+"_"+str(counter)+")"
                # end of for 
                #for varcount3 in range(1,u_count+1):
                    #expr_y+="+("+D[varcount1,varcount3]+"*u"+str(varcount3)+"_"+str(counter)+")"
                    #expr_r+="-("+D[varcount1,varcount3]+"*u"+str(varcount3)+"_attacked_"+str(counter)+")"
                # end of for 
                expr_rabs=expr_rabs[:len(expr_rabs)-2]          #removing last comma
                expr_rabs=");\n"
                #expr_y+=";\n"
                expr_r+=";\n"
            ## end of for
            #f.write(expr_y)
            f.write(expr_r)
            f.write(expr_rabs)
##################################################################################
########################### writing equations for x,z ############################
            #f.write("\t\tz1_"+str(counter+1)+" = (0.66*z1_"+str(counter)+") + (0.53*z2_"+str(counter)+") + (0.34*u_"+str(counter)+");\n");
            #f.write("\t\tz2_"+str(counter+1)+" = -(0.53*z1_"+str(counter)+") + (0.13*z2_"+str(counter)+") + (0.53*u_"+str(counter)+");\n");
            #f.write("\t\tx1_"+str(counter+1)+" = (0.66*x1_"+str(counter)+") + (0.53*x2_"+str(counter)+") + (0.34*u_attacked_"+str(counter)+");\n");
            #f.write("\t\tx2_"+str(counter+1)+" = - (0.53*x1_"+str(counter)+") + (0.13*x2_"+str(counter)+") + (0.53*u_attacked_"+str(counter)+");\n");
            
            expr_x=""
            expr_z=""
            for varcount1 in range(1,x_count+1):
                expr_x+="\t\tx"+str(varcount1)+"_"+str(counter+1)+" = "
                expr_z+="\t\tz"+str(varcount1)+"_"+str(counter+1)+" = "
                for varcount2 in range(1,x_count+1):
                    expr_x+="+("+A[varcount1,varcount2]+"*x"+str(varcount2)+"_"+str(counter)+")"
                    expr_z+="+("+A[varcount1,varcount2]+"*z"+str(varcount2)+"_"+str(counter)+")"
                # end of for 
                for varcount3 in range(1,u_count+1):
                    expr_x+="+("+B[varcount1,varcount3]+"*u"+str(varcount3)+"_"+str(counter)+")"
                    expr_z+="+("+B[varcount1,varcount3]+"*u"+str(varcount3)+"_attacked_"+str(counter)+")"
                # end of for 
                expr_x+=";\n"
                expr_z+=";\n"
                
            ## end of for
            f.write(expr_z)
            f.write(expr_x)
           
#################################################################################
        ##end of if else
############################# saving absolute values of x #####################
        expr_xabs=""
        #f.write("\t\ttheta["+str(counter)+"] = absolute(x1_"+str(counter+1)+");\n");
        #f.write("\t\tomega["+str(counter)+"] = absolute(x2_"+str(counter+1)+");\n\n");
        for varcount1 in range(1,x_count+1):
            expr_xabs+="\t\tx"+str(varcount1)+"_abs["+str(counter)+"] = absolute(x"+str(varcount1)+"_"+str(counter+1)+");\n"
        f.write(expr_xabs)    
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
        for varcount in range(1,x_count+1):
            f.write("(x"+str(varcount)+"_abs["+str(counter)+"]<="+str(safex[varcount-1]))
            if counter!=(x_count):
                f.write(" && ");
            #end of if
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
