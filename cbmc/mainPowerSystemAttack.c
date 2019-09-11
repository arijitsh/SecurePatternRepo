#include<stdio.h>
#include<stdlib.h>

int main()
{
    
    int K = 15, counter=0, attackLen = 7, startpoint = 3;
    int temp = 0, index = 0;
    int drop[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
    //int drop[] = {1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0};
    //int drop[] = {1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0};
    //int drop[] = {1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0};
    float th = 0.03;
    FILE *fp;
    //fp = fopen("powerSystem_0.0355_0_5_9_10.c","w+");
    fp = fopen("powerSystem_0.03_3_7_15_101000.c","w+");
    fprintf(fp,"#include<stdio.h>\n");
    fprintf(fp,"#include<math.h>\n");
    fprintf(fp,"#include<inttypes.h>\n");
    fprintf(fp,"#include \"library.h\"\n");
    fprintf(fp,"float nondet_float();\n");
    fprintf(fp,"int8_t nondet_int8();\n");
    fprintf(fp,"int const K = %d,attackLen = %d, startpoint = %d;\n",K,attackLen,startpoint);
    fprintf(fp,"int main()\n");
    fprintf(fp,"\t{\n");
    fprintf(fp,"\t\tfloat r1[K], r2[K], r[K], theta[K], omega[K], a1[K], a2[K], ");
    for(counter = 0;counter<=K;counter++)
    {
        fprintf(fp, "x1_%d = 0, x2_%d = 0, u_%d = 0, u_attacked_%d = 0, y1_%d = 0, y2_%d = 0, z1_%d = 0, z2_%d = 0,x1next_%d = 0, x2next_%d = 0, z1next_%d = 0, z2next_%d = 0",
                counter,counter,counter,counter,counter,counter,counter,counter,counter,counter,counter,counter);
        if(counter!=K)
            fprintf(fp,",");
        else
            fprintf(fp,";\n");
    }
    fprintf(fp,"\t\tint8_t syn = 0;\n\n");

    for(counter=0;counter<K;counter++)
    {
            fprintf(fp,"\t\t//pattern=%d;\n",drop[counter]);
            if(index+startpoint == counter)
			{
				fprintf(fp,"\t\tsyn = nondet_int8();\n");
				fprintf(fp,"\t\ta1[%d] = AttackFormat2(syn);\n",counter);
				fprintf(fp,"\t\tsyn = nondet_int8();\n");
				fprintf(fp,"\t\ta2[%d] = AttackFormat2(syn);\n",counter);

				/*fprintf(fp,"\t\ta1[%d] = nondet_float();\n",counter);
				fprintf(fp,"\t\twhile(isnormal(a1[%d])==0 && a1[%d]!=0.0)\n",counter,counter);
                fprintf(fp,"\t\t\ta1[%d] = nondet_float();\n",counter);
				fprintf(fp,"\t\ta2[%d] = nondet_float();\n",counter);
				fprintf(fp,"\t\t\twhile(isnormal(a2[%d])==0 && a2[%d]!=0.0)\n",counter,counter);
                fprintf(fp,"\t\t\ta2[%d] = nondet_float();\n",counter);*/
				index++;
				if(index==attackLen)
                    index = 0;
            }
            else
            {
                fprintf(fp,"\t\ta1[%d] = 0;\n",counter);
                fprintf(fp,"\t\ta2[%d] = 0;\n",counter);
            }
            if(drop[counter])
            {
                fprintf(fp,"\t\tu_%d = -(0.0556*z1_%d) - (0.3306*z2_%d);\n",counter,counter,counter);
                fprintf(fp,"\t\tu_attacked_%d = u_%d + a1[%d];\n",counter,counter,counter);
                fprintf(fp,"\t\ty1_%d = x1_%d + a2[%d];\n",counter,counter,counter);
                fprintf(fp,"\t\ty2_%d = x2_%d;\n",counter,counter);
                fprintf(fp,"\t\tr1[%d] = y1_%d - z1_%d;\n",counter,counter,counter);
                fprintf(fp,"\t\tr2[%d] = y2_%d - z2_%d;\n",counter,counter,counter);
                fprintf(fp,"\t\tr[%d] = max(absolute(r1[%d]),absolute(r2[%d]));\n",counter,counter,counter);
                fprintf(fp,"\t\tz1_%d = (0.66*z1_%d) + (0.53*z2_%d) + (0.34*u_%d) + (0.36*r1[%d]) + (0.27*r2[%d]);\n",counter+1,counter,counter,counter,counter,counter);
                fprintf(fp,"\t\tz2_%d = -(0.53*z1_%d) + (0.13*z2_%d) + (0.53*u_%d) - (0.31*r1[%d]) + (0.08*r2[%d]);\n",counter+1,counter,counter,counter,counter,counter);
                fprintf(fp,"\t\tx1_%d = (0.66*x1_%d) + (0.53*x2_%d) + (0.34*u_attacked_%d);\n",counter+1,counter,counter,counter);
                fprintf(fp,"\t\tx2_%d = - (0.53*x1_%d) + (0.13*x2_%d) + (0.53*u_attacked_%d);\n",counter+1,counter,counter,counter);
            }
            else
            {
                fprintf(fp,"\t\tu_%d = u_%d;\n",counter,counter-1);
                fprintf(fp,"\t\tu_attacked_%d = u_attacked_%d;\n",counter,counter-1);
                fprintf(fp,"\t\tz1_%d = (0.66*z1_%d) + (0.53*z2_%d) + (0.34*u_%d);\n",counter+1,counter,counter,counter);
                fprintf(fp,"\t\tz2_%d = -(0.53*z1_%d) + (0.13*z2_%d) + (0.53*u_%d);\n",counter+1,counter,counter,counter);
                fprintf(fp,"\t\tx1_%d = (0.66*x1_%d) + (0.53*x2_%d) + (0.34*u_attacked_%d);\n",counter+1,counter,counter,counter);
                fprintf(fp,"\t\tx2_%d = - (0.53*x1_%d) + (0.13*x2_%d) + (0.53*u_attacked_%d);\n",counter+1,counter,counter,counter);
            }
            fprintf(fp,"\t\ttheta[%d] = absolute(x1_%d);\n",counter,counter+1);
            fprintf(fp,"\t\tomega[%d] = absolute(x2_%d);\n\n",counter,counter+1);
	}
	fprintf(fp,"\n\t\tassert((");
    for(counter=0;counter<K;counter++)
    {
        if(drop[counter])
        {
            fprintf(fp,"(r[%d]>%f)",
                        counter,th);
            if(counter!=(K-1))
                fprintf(fp," || ");
        }
    }

    fprintf(fp,")||(");

    for(counter=0;counter<K;counter++)
    {
        fprintf(fp,"(theta[%d]<=0.1 && omega[%d]<=0.05)",
                    counter,counter);
        if(counter!=(K-1))
            fprintf(fp," && ");
    }

    fprintf(fp,"));\n");

    fprintf(fp,"\t\treturn 0;\n");
    fprintf(fp,"\t}");
    fclose(fp);
    system("gcc input.c");
    system("nohup ./cbmc powersys_th_09.c --trace &>powersys_th_09.out");
    system("nohup ./cbmc powersys_th_09.c --trace &>powersys_th_09.out");
    return 0;
}
