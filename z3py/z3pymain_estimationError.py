import os
import numpy as np
import errno
############################## inputs ############################
modelName = "trajectory_pajic"

################## attack length and position ###################
attackLen = 1
patternList = [1]
# patternList = [11011,11110,111100,110011,11011100,11010011,11110100,11110010,11001011,11001110,100011011,100011101,1000011011,1000011101,1000110011,1000111001,110010001011,110010001110,110010100011,110010111000,110011100010,110011101000,110001001011,110001001110,110001010011,110001011100,110001110010,110001110100,110100100011,110100111000,110100010011,110100011100,110111001000,110111000100,111100100010,111100101000,111100010010,111100010100,111101001000,111101000100]
offset = 4
start = 0
isSat = 0
innerCircleDepth = 0.1
isDelayed = 0
####################################################################
if modelName == "tempControl":
    modelName= "tempControl"
    A= np.matrix('0.94648514795348381856143760160194 0.0018971440127071483982418298452899;0 0.000000000013887943864964020896356969649573')
    B= np.matrix('-0.046752721484125708828472056666214;-0.99999999998611222018496391683584')
    C= np.matrix('1 0')
    D= np.matrix('0')
    Gain= np.matrix('-0.3712408426327057364702000086254 -0.0007441187601164687840174516431091')
    L= np.matrix('0.60711740001928504728567759229918;0.39288259998275032458536770718638')
    safex = [30,30]
    tolerance = [1,1]
    th = 0.00001
elif modelName == "trajectory":
    A= np.matrix('1.0000    0.1000;0    1.0000')
    B= np.matrix('0.0050;0.1000')
    C= np.matrix('1 0')
    D= np.matrix('0')
    Gain= np.matrix('16.0302    5.6622')  # settling time around 10
    L = np.matrix('0.9902;0.9892')
    safex = [25,30]
    tolerance = [1,1]
    th = 2
    sensorRange = [30]
    actuatorRange = [0]
elif modelName == "trajectory_pajic":# model from pajic's sporadic MAC CDC paper
    A= np.matrix('1.0000    0.1000;0    1.0000')
    B= np.matrix('0.0001;0.01')             
    C= np.matrix('1 0; 0 1')
    D= np.matrix('0')
    Gain= np.matrix('0.9914    1.7171') 
    L = np.matrix('0.6180 0.0011;0.0011 0.6180')
    safex = 0.035
    tolerance = 0.001
    th = 0.018
    sporadicity = 5
elif modelName == "esp":
    A= np.matrix('0.4450 -0.0458;1.2939 0.4402')
    B= np.matrix('0.0550;4.5607')
    C= np.matrix('0 1')
    D= np.matrix('0')
    Gain= np.matrix('-0.0987 0.1420')
    L= np.matrix('-0.0390;0.4339')
    safex = [1,2]
    tolerance = [0.1,0.1]
    th = 0.8
    sensorRange = [2.5]
    actuatorRange = [0]
elif modelName == "powersystem":
    A= np.matrix('0.66 0.53;-0.53 0.13')
    B= np.matrix('0.34;0.53')
    C= np.matrix('1 0;0 1')
    D= np.matrix('0;0')
    Gain= np.matrix('0.0556 0.3306')
    L= np.matrix('0.36 0.27;  -0.31 0.08')
    safex = [0.1,0.05]
    tolerance = [0.001,0.0001]
    # initialRange = np.matrix('0 0.35;-4 4')
    th = 0.03
elif modelName == "plant":
    A= np.matrix('2.6221    0.3197    1.8335   -1.0664; -0.2381    0.1872   -0.1361    0.2017; 0.1612    0.7888    0.2859    0.6064;-0.1035    0.7641    0.0886    0.7360')
    B= np.matrix('0.4654   -1.5495; 1.3138    0.0851; 2.0549   -0.6730; 2.0227   -0.1597')
    C= np.matrix('1     0     1    -1;0     1     0     0')
    D= np.matrix('0 0;0 0')
    Gain= np.matrix('-0.2580    0.3159   -0.1087    0.3982; -1.6195   -0.1314   -1.1232    0.7073')
    L= np.matrix('2.4701   -0.0499; -0.2144    0.0224; 0.2327    0.0946; -0.0192    0.1004')
    safex = [0.01,0.01,0.01,0.01]
    tolerance = [0.0001,0.0001,0.0001,0.0001]
    th = 0.0001
elif modelName == "powergrid":
    A= np.matrix('-1 -3;3 -5')
    B= np.matrix('2 -1;1 0')
    C= np.matrix('0.8 2.4;1.6 0.8')
    D= np.matrix('0 0; 0 0')
    Gain= np.matrix('2.9846   -4.9827;6.9635   -6.9599')
    L= np.matrix('-1.1751   -0.1412;-2.6599    2.2549')
    safex = [0.1,0.2]
    tolerance = [0.001,0.001]
    th = 0.01

LC = L.dot(C)
LCA = LC.dot(A)
ALCA = A - LCA
CA = C.dot(A)
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

######### Configure which sensor/control input to attack ##########
u_attack_map = np.zeros(u_count,dtype=float)
y_attack_map = np.zeros(y_count,dtype=float)
u_attack_map[0] = 0 
y_attack_map[0] = 1

######### Configure which sensor/control input to attack ##########
# initialRange = np.zeros(shape=(x_count,2), dtype=float)
# for i in range(x_count):
#     initialRange[i,0] = (-1)*safex[i]*innerCircleDepth
#     initialRange[i,1] = safex[i]*innerCircleDepth

print(set(patternList))
#Compute pattern length
for pattern in set(patternList):
    print("Running for "+str(pattern))
    patternLen=len(str(pattern))

    #Compute pattern array
    patternArray = np.zeros((patternLen), dtype=int)
    patternTemp = pattern
    i = patternLen-1
    while patternTemp>0:
        patternArray[i] = patternTemp%10
        patternTemp=patternTemp//10
        i = i-1

    f0 = open(path+modelName+"_downtime.z3result", "w+")
    f0.write("0")
    f0.close()

    print("Finding minimum attack length for "+str(modelName)+" and pattern "+str(pattern))
    isSat = 0
    attackLen = 1
    while isSat == 0:  
        print("attack length:"+str(attackLen)+"\n")
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
            print("\n")
            fileName = modelName + "_sporadic_" + str(th) + "_" +str(index)+"_"+str(attackLen)+"_"+str(K)+"_"+str(pattern)+".py"
            f = open(path+fileName, "w+")
            f.write("from z3 import *\n")
            f.write("import math\n")
            f.write("import numpy as np\n\n")
            f.write("s = Solver()\n")
            # f.write("set_option(precision=40)\n")
            f.write("set_option(rational_to_decimal=True)\n")
            # declaring variables
            for varcount in range(1,x_count+1):
                f.write("est"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
            for varcount in range(1,y_count+1):
                f.write("z"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
                f.write("zabs"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")
                f.write("attackOnY"+str(varcount)+" = np.zeros("+str(K+1)+", dtype=float)\n")

            f.write("z = np.zeros("+str(K+1)+", dtype=float)\n")
            f.write("est = np.zeros("+str(K+1)+", dtype=float)\n")
     
            for i in range(K+1):
                decl=""
                for varcount in range(1,y_count+1):
                    decl+="z"+str(varcount)+"_"+str(i)+" = Real('z"+str(varcount)+"_"+str(i)+"')\n"
                    decl+="zabs"+str(varcount)+"_"+str(i)+" = Real('zabs"+str(varcount)+"_"+str(i)+"')\n"

                for varcount in range(1,x_count+1):
                    decl+="est"+str(varcount)+"_"+str(i)+" = Real('est"+str(varcount)+"_"+str(i)+"')\n"

                decl+="z_"+str(i)+" = Real('z_"+str(i)+"')\n"
                decl+="est_"+str(i)+" = Real('est_"+str(i)+"')\n"
                f.write(decl)
            #initial range declaration of variables    
            f.write("\n")
            for varcount in range(1,x_count+1):
                f.write("s.add(est"+str(varcount)+"_0 == 0)\n")

            expr_est = "s.add(est_0*est_0 =="
            for varcount in range(1,x_count+1):
                expr_est+="+(est"+str(varcount)+"_0 * est"+str(varcount)+"_0)"

            expr_est+=")\n"
            f.write(expr_est)

            expr_attack = ""
            for varcount1 in range(1, y_count+1):
                expr_attack+="attackOnY"+str(varcount1)+"_0 = Real('attackOnY"+str(varcount1)+"_0')\n"
                expr_attack+="s.add(attackOnY"+str(varcount1)+"_0 == 0)\n"
            f.write(expr_attack)

            j = 0
            for i in range(K):
                # Updating residue error
                if i == (j+index):
                    expr_z=""
                    for varcount1 in range(1,y_count+1):
                        expr_z+="s.add(z"+str(varcount1)+"_"+str(i)+" == attackOnY"+str(varcount1)+"_"+str(i)
                        for varcount2 in range(1,x_count+1):
                            print(CA[varcount1-1,varcount2-1])
                            expr_z+=" + ("+str(CA[varcount1-1,varcount2-1])+"*est"+str(varcount2)+"_"+str(i)+")"
                        
                        expr_z+=")\n"
                    f.write(expr_z)

                    if j== attackLen:
                        j=0 
                else:
                    expr_z=""
                    for varcount1 in range(1,y_count+1):
                        expr_z+="s.add(z"+str(varcount1)+"_"+str(i)+" == "
                        for varcount2 in range(1,x_count+1):
                            expr_z+=" + ("+str(CA[varcount1-1,varcount2-1])+"*est"+str(varcount2)+"_"+str(i)+")"
                        
                        expr_z+=")\n"
                    f.write(expr_z)

                expr_zabs=""
                for varcount1 in range(1,y_count+1):
                    expr_zabs+="s.add(zabs"+str(varcount1)+"_"+str(i)+" == If(z"+str(varcount1)+"_"+str(i)+"<0,(-1)*z"+str(varcount1)+"_"+str(i)+",z"+str(varcount1)+"_"+str(i)+"))\n"
                f.write(expr_zabs)
                
                f.write("s.add(z_"+str(i)+"== If(zabs1_"+str(i)+"<zabs2_"+str(i)+",zabs2_"+str(i)+",zabs1_"+str(i)+"))\n")

                # Threshold check
                f.write("s.add(z_{0}<{1})\n".format(i,th))

                # Update estimation error
                if i == (j+index):
                    for varcount in range(1, y_count+1):
                        f.write("attackOnY"+str(varcount)+"_"+str(i+1)+" = Real('attackOnY"+str(varcount)+"_"+str(i+1)+"')\n")
                        if i%sporadicity==0:
                            f.write("s.add(attackOnY"+str(varcount)+"_"+str(i+1)+" == 0)\n")

                    expr_est=""
                    for varcount1 in range(1,x_count+1):
                        expr_est+="s.add(est"+str(varcount1)+"_"+str(i+1)+" == " 
                        for varcount2 in range(1,x_count+1):
                            expr_est+=" + ("+str(ALCA[varcount1-1,varcount2-1])+"*est"+str(varcount2)+"_"+str(i)+") "
                        for varcount3 in range(1,y_count+1):
                            expr_est+=" - ("+str(L[varcount1-1,varcount3-1])+"*attackOnY"+str(varcount3)+"_"+str(i+1)+")"
                        expr_est+=")\n"             
                    
                    j = j+1                    
                else:
                    expr_est=""
                    for varcount1 in range(1,x_count+1):
                        expr_est+="s.add(est"+str(varcount1)+"_"+str(i+1)+" == " 
                        for varcount2 in range(1,x_count+1):
                            expr_est+=" + ("+str(A[varcount1-1,varcount2-1])+"*est"+str(varcount2)+"_"+str(i)+") "
                        expr_est+=")\n"            

                expr_est+="s.add(est_"+str(i+1)+"*est_"+str(i+1)+"=="
                for varcount in (1,x_count):
                    expr_est+="+ est"+str(varcount)+"_"+str(i+1)+"*est"+str(varcount)+"_"+str(i+1)
                expr_est+=")\n"
                f.write(expr_est) 

            # Safety check
            f.write("s.add(Or(")
            assertion=""
            for i in range(K):
                assertion+="(est_"+str(i)+" - "+str(safex)+")>"+str(tolerance)+","
                
            assertion = assertion[:len(assertion)-1]
            f.write(assertion)
            f.write("))\n")

            # f.write("\nprint(s.sexpr())")
            f.write("\nif s.check() != sat:\n")
            f.write("\tprint(s.check())\n")
            f.write("\tisSat = 0\n")
            f.write("else:\n")
            f.write("\tprint(s.check())\n")
            f.write("\tisSat = 1\n")
            f.write("\tf0 = open(\""+path+modelName+"_downtime.z3result\", \"w+\")\n")
            f.write("\tf0.write(\"1\")\n")
            f.write("\tf0.close()\n") 
            f.write("\tm = s.model()\n")
            f.write("\tfor d in m.decls():\n")
            # f.write("\t\tprint (\"%s = %s\" % (d.name(), m[d]))\n")                
            for varcount in range(1,x_count+1): # Parsing x, absolute x and z from z3 py output
                f.write("\t\tif \"est"+str(varcount)+"_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\test"+str(varcount)+"[i] = float(y)\n")
            for varcount in range(1,y_count+1): # Parsing y, attack on y and r from z3 py output
                f.write("\t\tif \"attackOnY"+str(varcount)+"_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\tattackOnY"+str(varcount)+"[i] = float(y)\n")

                f.write("\t\tif \"z"+str(varcount)+"_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\tz"+str(varcount)+"[i] = float(y)\n")
                
                f.write("\t\tif \"zabs"+str(varcount)+"_\" in d.name():\n")
                f.write("\t\t\ti = int(d.name().split('_')[1])\n")
                f.write("\t\t\tx = str(m[d])\n")
                f.write("\t\t\tindex = x.find(\"?\")\n")
                f.write("\t\t\tif index != -1:\n")
                f.write("\t\t\t\ty = x[:-1]\n")
                f.write("\t\t\telse:\n")
                f.write("\t\t\t\ty = x\n")
                f.write("\t\t\tzabs"+str(varcount)+"[i] = float(y)\n")
            
            f.write("\t\tif \"z_\" in d.name():\n")
            f.write("\t\t\ti = int(d.name().split('_')[1])\n")
            f.write("\t\t\tx = str(m[d])\n")
            f.write("\t\t\tindex = x.find(\"?\")\n")
            f.write("\t\t\tif index != -1:\n")
            f.write("\t\t\t\ty = x[:-1]\n")
            f.write("\t\t\telse:\n")
            f.write("\t\t\t\ty = x\n")
            f.write("\t\t\tz[i] = float(y)\n")

            f.write("\t\tif \"est_\" in d.name():\n")
            f.write("\t\t\ti = int(d.name().split('_')[1])\n")
            f.write("\t\t\tx = str(m[d])\n")
            f.write("\t\t\tindex = x.find(\"?\")\n")
            f.write("\t\t\tif index != -1:\n")
            f.write("\t\t\t\ty = x[:-1]\n")
            f.write("\t\t\telse:\n")
            f.write("\t\t\t\ty = x\n")
            f.write("\t\t\test[i] = float(y)\n")

            # Printing the execution sequence
            f.write("\tfor i in range({0}):\n".format(K))
            for varcount in  range(1, y_count+1):
                f.write("\t\tprint(\"attackOnY"+str(varcount)+"_{0}={1}\".format(i,attackOnY"+str(varcount)+"[i]))\n") 
            for varcount in  range(1, y_count+1):
                f.write("\t\tprint(\"z"+str(varcount)+"_{0}={1}\".format(i,z"+str(varcount)+"[i]))\n")
            for varcount in  range(1, y_count+1):
                f.write("\t\tprint(\"zabs"+str(varcount)+"_{0}={1}\".format(i,zabs"+str(varcount)+"[i]))\n")
            f.write("\t\tprint(\"z_{0}={1}\".format(i,z[i]))\n")
            for varcount in  range(1, x_count+1):
                f.write("\t\tprint(\"est"+str(varcount)+"_{0}={1}\".format(i,est"+str(varcount)+"[i]))\n") 
            f.write("\t\tprint(\"est_{0}={1}\".format(i,est[i]))\n")
            
              
            # Printing attack vectors
            for varcount in  range(1, y_count+1):
                f.write("print(\"attack on sensor {0}\")\n".format(varcount))
                f.write("print(attackOnY{0})\n".format(varcount))
       
            f.write("if isSat==1:\n")
            f.write("\tf0 = open(\""+path+modelName+"_downtime.z3result\", \"w+\")\n")
            f.write("\tf0.write(\"1\")\n")
            f.write("\tf0.close()\n")

            f.close()
            os.system("python "+path+fileName+">"+path+fileName+".z3out")
            f0 = open(path+modelName+"_downtime.z3result", "r")
            if f0.mode == 'r':
                content = f0.read()
                isSat = int(content)
            f0.close()
            if isSat==0:
                os.remove(path+fileName)
                os.remove(path+fileName+".z3out")
            else:
                print("go to "+path+fileName+".z3out \n")
            index = index + 1
        attackLen = attackLen + 1

    final = open(path+modelName+"_final_downtime.result", "a+")
    final.write(str(pattern) + ":" + str(attackLen-2)+"\n")
    final.close()