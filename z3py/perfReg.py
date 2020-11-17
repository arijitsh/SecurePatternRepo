# Controller type: PID
import os
import numpy as np
import errno
############################## inputs ############################
modelName = "trajectory"

################## attack length and position ###################
patternList = [1]
# patternList = [1,10,110, 110,1100,110100,110010,1011,11100,100011,1011100,1010011,10001011,10001110,10111,100111,1000111,10000111,10100111,10111100,100010111,100011110,1000010111,1000011110,1000100111,1000111100,100010100111,100010111100,100010010111,100010011110,100011110100,100011110010]
start = 1
innitialRegionDepth = 0.1
isDelayed = 0

####################################################################
if modelName == "tempControl":
    A= np.matrix('0.94648514795348381856143760160194 0.0018971440127071483982418298452899;0 0.000000000013887943864964020896356969649573')
    B= np.matrix('-0.046752721484125708828472056666214;-0.99999999998611222018496391683584')
    C= np.matrix('1 0')
    D= np.matrix('0')
    Gain= np.matrix('-0.3712408426327057364702000086254 -0.0007441187601164687840174516431091')
    L= np.matrix('0.60711740001928504728567759229918;0.39288259998275032458536770718638')
    outerCircle = [30,30]
elif modelName == "trajectory":
    A= np.matrix('1.0000    0.1000;0    1.0000')
    B= np.matrix('0.0050;0.1000')
    C= np.matrix('1 0')
    D= np.matrix('0')
    Gain= np.matrix('16.0302    5.6622')  # settling time around 10
    L = np.matrix('0.9902; 0.9892')
    # L = np.matrix('1.8721; 9.6532')
    # outerCircle = [1,10]
    outerCircle = [25,30]
    th = 0.05
    settlingTime = 13 #new
    # sensorRange = [3000000] #new
    sensorRange = [30] #new
    actuatorRange = [36] #new
elif modelName == "esp":
    A= np.matrix('0.4450 -0.0458;1.2939 0.4402')
    B= np.matrix('0.0550;4.5607')
    C= np.matrix('0 1')
    D= np.matrix('0')
    Gain= np.matrix('-0.0987 0.1420')
    L= np.matrix('-0.0390;0.4339')
    outerCircle = [1,2]
    th = 0.003
elif modelName == "powersystem":
    A= np.matrix('0.66 0.53;-0.53 0.13')
    B= np.matrix('0.34;0.53')
    C= np.matrix('1 0;0 1')
    D= np.matrix('0;0')
    Gain= np.matrix('0.0556 0.3306')
    L= np.matrix('0.36 0.27;  -0.31 0.08')
    outerCircle = [0.1,0.05]
    th = 0.03
elif modelName == "plant":
    A= np.matrix('2.6221    0.3197    1.8335   -1.0664; -0.2381    0.1872   -0.1361    0.2017; 0.1612    0.7888    0.2859    0.6064;-0.1035    0.7641    0.0886    0.7360')
    B= np.matrix('0.4654   -1.5495; 1.3138    0.0851; 2.0549   -0.6730; 2.0227   -0.1597')
    C= np.matrix('1     0     1    -1;0     1     0     0')
    D= np.matrix('0 0;0 0')
    Gain= np.matrix('-0.2580    0.3159   -0.1087    0.3982; -1.6195   -0.1314   -1.1232    0.7073')
    L= np.matrix('2.4701   -0.0499; -0.2144    0.0224; 0.2327    0.0946; -0.0192    0.1004')
    outerCircle = [0.01,0.01,0.01,0.01]
elif modelName == "powergrid":
    A= np.matrix('-1 -3;3 -5')
    B= np.matrix('2 -1;1 0')
    C= np.matrix('0.8 2.4;1.6 0.8')
    D= np.matrix('0 0; 0 0')
    Gain= np.matrix('2.9846   -4.9827;6.9635   -6.9599')
    L= np.matrix('-1.1751   -0.1412;-2.6599    2.2549')
    outerCircle = [0.1,0.2]

################## creating the path to save results #################
path="results/"+modelName+"/"
try:
    os.makedirs(path)
except OSError as err:
    if err.errno!= errno.EEXIST:
        raise
#####################################################################
u_count=B.shape[1]
x_count=A.shape[1]
y_count=C.shape[0]

#Compute pattern length
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

    ####### Compute inner circle ##########################################################
    innerCircle = []
    for i in range(x_count):
        innerCircle.append(outerCircle[i]*innitialRegionDepth)    

    print("Finding inner circle depth for = "+str(settlingTime))
    
    index = 0
    maxOnTime = 0    
    innerCircleDepth=0.3 #new
    maxIteration = settlingTime+5 #new
    isSat = 1
    while innerCircleDepth < 1 and isSat==1:#new                 
        K = settlingTime #new
        # isBreak = 0
        f0 = open(path+modelName+".result", "w+")
        f0.write(str(K)+":\n")
        f0.close()
        while isSat == 1 and K<maxIteration:  #new
            print("Checking for performance region:"+str(innerCircleDepth))
            # create drop pattern    
            dropPattern = np.ones((K), dtype=int)
            j=index
            if pattern!=1:
                for i in range(K):
                    dropPattern[i] = patternArray[j]
                    j = j + 1
                    if j == patternLen:
                        j = 0
            #new
            print("performance circle:")#new
            print(innerCircleDepth)#new
            print("\n")
            f0 = open(path+modelName+".result", "w+")#new
            f0.write("\t"+str(innerCircleDepth)+",\n")#new
            f0.close()#new
            fileName = modelName + "_performanceReg_"+str(innerCircleDepth)+"_"+str(K)+".py"
            f = open(path+fileName, "w+")
            f.write("from z3 import *\n")
            f.write("import math\n")
            f.write("import numpy as np\n\n")
            f.write("s = Solver()\n")
            # f.write("set_option(precision=40)\n")
            f.write("set_option(rational_to_decimal=True)\n")

            ## declarations
            for i in range(K+1):
                decl="#declarations\n"
                for varcount in range(1,x_count+1):
                    decl+="x"+str(varcount)+"_"+str(i)+" = Real('x"+str(varcount)+"_"+str(i)+"')\n"
                    decl+="z"+str(varcount)+"_"+str(i)+" = Real('z"+str(varcount)+"_"+str(i)+"')\n"
                    decl+="xabs"+str(varcount)+"_"+str(i)+" = Real('xabs"+str(varcount)+"_"+str(i)+"')\n"
                for varcount in range(1,y_count+1):
                    decl+="y"+str(varcount)+"_"+str(i)+" = Real('y"+str(varcount)+"_"+str(i)+"')\n"
                    decl+="r"+str(varcount)+"_"+str(i)+" = Real('r"+str(varcount)+"_"+str(i)+"')\n"
                    decl+="rabs"+str(varcount)+"_"+str(i)+" = Real('rabs"+str(varcount)+"_"+str(i)+"')\n"
                for varcount in range(1,u_count+1):
                    decl+="u"+str(varcount)+"_"+str(i)+" = Real('u"+str(varcount)+"_"+str(i)+"')\n"
                
                decl+="r_"+str(i)+" = Real('r_"+str(i)+"')\n"
                decl+="depth0 = Real('depth0')\n" #new
                f.write(decl)

            ## Initialization
            f.write("#Init\n")
            f.write("s.add(depth0 =="+str(innerCircleDepth)+")\n") #new
            for varcount in range(1,x_count+1):
                f.write("s.add(And(x"+str(varcount)+"_0 < "+str(innitialRegionDepth)+"*"+str(outerCircle[varcount-1])+",x"+str(varcount)+"_0 > "+str(innitialRegionDepth)+"* (-"+str(outerCircle[varcount-1])+")))\n") #new
            for varcount1 in range(1,y_count+1):
                f.write("s.add(y"+str(varcount1)+"_0 == 0)\n")
            for varcount2 in range(1,u_count+1): 
                f.write("s.add(u"+str(varcount2)+"_0 == 0)\n")
            f.write("\n")

            for i in range(K):
                # Update r
                expr_r="#residue calc\n"
                for varcount1 in range(1,y_count+1):
                    expr_r+="s.add(r"+str(varcount1)+"_"+str(i)+" == y"+str(varcount1)+"_"+str(i)
                    for varcount2 in range(1,x_count+1):
                        expr_r+=" - ("+str(C[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+")"
                    for varcount3 in range(1,u_count+1):       
                        expr_r+=" - ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+")"   
                    expr_r+=")\n"
                f.write(expr_r)

                # Compute 1-norm of r
                # expr_rabs = "#residue norm calc\n"
                # expr_r = "s.add(r_"+str(i)+" ==" 
                # for varcount1 in range(1,y_count+1):
                #     expr_rabs+= "s.add(rabs"+str(varcount1)+"_"+str(i)+" == If(r"+str(varcount1)+"_"+str(i)+"<0,(-1)*r"+str(varcount1)+"_"+str(i)+",r"+str(varcount1)+"_"+str(i)+"))\n"
                #     expr_r+="rabs"+str(varcount1)+"_"+str(i)+" +"
                # expr_r = expr_r[:len(expr_r)-1] 
                # expr_r+=")\n"
                # f.write(expr_rabs)
                # f.write(expr_r)

                # f.write("s.add(r_{0}<{1})\n".format(i,th))

                # Update x and z
                expr_x="#state calc\n"
                expr_xabs="#absolute state value calc\n"
                expr_z="#estimated state calc\n"
                for varcount1 in range(1,x_count+1):
                    expr_x+="s.add(x"+str(varcount1)+"_"+str(i+1)+" == "                
                    expr_z+="s.add(z"+str(varcount1)+"_"+str(i+1)+" == "
                    for varcount2 in range(1,x_count+1):
                        expr_x+=" ("+str(A[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i)+") +"
                        expr_z+=" ("+str(A[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+") +"
                    for varcount3 in range(1,u_count+1):
                        expr_z+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
                        expr_x+=" ("+str(B[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i)+") +"
                    for varcount4 in range(1,y_count+1):
                        expr_z+=" ("+str(L[varcount1-1,varcount4-1])+"*r"+str(varcount4)+"_"+str(i)+") +"
                    
                    expr_xabs+="s.add(xabs"+str(varcount1)+"_"+str(i+1)+" == If(x"+str(varcount1)+"_"+str(i+1)+"<0,(-1)*x"+str(varcount1)+"_"+str(i+1)+",x"+str(varcount1)+"_"+str(i+1)+"))\n"

                    expr_x=expr_x[:len(expr_x)-1] 
                    expr_x = expr_x + ")\n"
                    expr_z=expr_z[:len(expr_z)-1] 
                    expr_z = expr_z + ")\n"            

                f.write(expr_z)
                f.write(expr_x)
                f.write(expr_xabs)            

                # Simulate dropping behavior
                if dropPattern[i]: #If there is a 1 in the pattern
                    expr_u="#control input calc no drop\n"
                    for varcount1 in range(1,u_count+1):
                        expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == "
                        for varcount2 in range(1,x_count+1):
                            if isDelayed:
                                expr_u+=" - ("+str(Gain[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i)+")"
                            else:
                                expr_u+=" - ("+str(Gain[varcount1-1,varcount2-1])+"*z"+str(varcount2)+"_"+str(i+1)+")"
                        expr_u+=")\n"
                    f.write(expr_u)
                else:
                    expr_u=""
                    for varcount1 in range(1,u_count+1):
                        expr_u+="s.add(u"+str(varcount1)+"_"+str(i+1)+" == u"+str(varcount1)+"_"+str(i)+")\n"
                    f.write(expr_u)

                # u limit check
                expr_u="#actuation saturation bound\n"
                for varcount1 in range(1,u_count+1):
                        expr_u+="s.add(And(u"+str(varcount1)+"_"+str(i+1)+">-"+str(actuatorRange[varcount1-1])+",u"+str(varcount1)+"_"+str(i+1)+"<"+str(actuatorRange[varcount1-1])+"))\n"
                f.write(expr_u)
                # Update y
                expr_y="#output calc\n"
                for varcount1 in range(1,y_count+1):
                    expr_y+="s.add(y"+str(varcount1)+"_"+str(i+1)+" == "
                    for varcount2 in range(1,x_count+1):
                        expr_y+=" + ("+str(C[varcount1-1,varcount2-1])+"*x"+str(varcount2)+"_"+str(i+1)+")"
                    for varcount3 in range(1,u_count+1):
                        expr_y+=" + ("+str(D[varcount1-1,varcount3-1])+"*u"+str(varcount3)+"_"+str(i+1)+")"         
                    expr_y+=")\n"
                f.write(expr_y)
                # y limit check
                expr_y="#sensor range check\n"
                for varcount1 in range(1,y_count+1):
                        expr_y+="s.add(And(y"+str(varcount1)+"_"+str(i+1)+">-"+str(sensorRange[varcount1-1])+",y"+str(varcount1)+"_"+str(i+1)+"<"+str(sensorRange[varcount1-1])+"))\n"
                f.write(expr_y)
                # x inclusion check
            f.write("#x inclusion in performnce reg check\n")
            expr_inclusion = "s.add(Or("
            for i in range(K):
                for varcount in range(1,x_count+1):
                    expr_inclusion+="xabs"+str(varcount)+"_"+str(i+1)+" > depth0*"+str(outerCircle[varcount-1])+"," #new

            expr_inclusion=expr_inclusion[:len(expr_inclusion)-1] 
            expr_inclusion+="))\n"
            f.write(expr_inclusion)

            # f.write("\nprint(s.sexpr())")
            f.write("\nif s.check() != sat:\n")
            f.write("\tprint(s.check())\n")
            f.write("\tisSat = 0\n")
            f.write("else:\n")
            f.write("\tprint(s.check())\n")
            f.write("\tisSat = 1\n")
            f.write("\tm = s.model()\n")
            f.write("\tfor d in m.decls():\n")
            f.write("\t\tprint (\"%s = %s\" % (d.name(), m[d]))\n") 

            # f.write("if isSat==0:\n")#new
            f.write("\tf0 = open(\""+path+modelName+".z3result\", \"w+\")\n")
            f.write("\tf0.write(str("+str(isSat)+"))\n")
            f.write("\tf0.close()\n")

            f.close()
            
            os.system("python "+path+fileName+">"+path+fileName+".z3out")
            f0 = open(path+modelName+".z3result", "r")
            if f0.mode == 'r':
                content = f0.read()
                isSat = int(content)
            f0.close()
            print("isSat="+str(isSat))
            if isSat==0:
                print("performance region:"+innerCircleDepth)#new
                break#new
            else:
                K=K+1 #new                           
        else:
            innerCircleDepth= innerCircleDepth+0.1 #new
        
    
    
    final = open(path+modelName+".result", "a+")
    final.write("performance region: " + str(innerCircleDepth)+"\n")
    final.close()