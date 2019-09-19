#include<inttypes.h>

double max(double a, double b)
{
    if(a>=b)
        return a;
    else
        return b;
}

double absolute(double a)
{
    if(a<0)
        return (-1)*a;
    else
        return a;
}
float AttackFormat1(int8_t attackValue)
{
    float result = 0;
    int isNegative = 0;

    if(attackValue<0)
    {
    	isNegative = 1;
    	attackValue = (-1)*attackValue;
	}

    //result = (float)attackValue/(float)((-1)*INT8_MIN + 1);
    result = (attackValue % 10);
    if(isNegative)
    	result = (-1)*result;

    return result;
}

float AttackFormat2(int8_t attackValue)
{
    float result = 0;
    result = (float)attackValue/(float)((-1)*INT8_MIN + 1);

    return result;
}

float AttackFormat3(int8_t integer, int8_t fraction)
{
    float result = 0;

    result = integer + (float)fraction/(float)((-1)*INT8_MIN + 1);

    return result;
}

int generateDrop(int8_t dropValue, int patternLen)
{
    int dropIndex = 0;

    if(dropValue<0)
        dropValue = (-1)*dropValue;
    dropIndex = dropValue % patternLen;

    return dropIndex;
}
