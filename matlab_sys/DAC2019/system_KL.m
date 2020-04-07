function[K,L]= getKL(A,B,C,D,h)

controllability=[rank(A)==rank(ctrb(ss(A,B,C,D,h)))];
if(controllability==1):
    p = 100;
    Q = p*eye(size(A));
    R = 0.1*eye(size(B,2),size(B,2));
    K = dlqr(A,B,Q,R)
else:
    K=[];
    fprintf("plant not controllable at %f sampling rate",h);

QN =1;
RN = eye(size(C,1));
[KEST,L,PN] = kalman(pgrid_d,QN,RN)