function[K,L]= getKL(A,B,C,D,h)
sys=ss(A,B,C,D,h);
[num,den]=ss2tf(A,B,C,D);
poles=roots(num);
controllability=[rank(A)==rank(ctrb(sys))];
if(controllability==1)
%     p = 50000;
%     Q = p*eye(size(A));
%     R = 0.001*eye(size(B,2),size(B,2));
%     K = dlqr(A,B,Q,R);
    
    K=place(A,B,poles)
else
    K=[];
    fprintf("plant not controllable at %f sampling rate",h);
end

QN =1;
RN = eye(size(C,1));
[KEST,L,PN] = kalman(sys,QN,RN);