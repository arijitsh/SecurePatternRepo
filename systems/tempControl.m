% A=[-0.11 0.1;0 -50];
% B=[0;-50];
% C=[1 0];
% D=[0];
%okay
A1=[-20 1;0 .1];
B1=[0;1];
C1=[1 0];
D1=D;
% sys=ss(A,B,C,D);
sys=ss(A1,B1,C1,D);
step(sys);
% [n,m]=ss2tf(A,B,C,D);
[n1,m1]=ss2tf(A1,B1,C1,D1);
% systf=tf(n,m);
systf=tf(n1,m1);
bode(systf);
damp(systf);
[gm,pm,wgc,wpc]=margin(systf)
sysd=c2d(sys,0.03);
figure(1)
step(sysd);
Q=100000*eye(size(A1));
R=0.001;
K1=dlqr(sysd.a,sysd.b,Q,R);
eig(sysd.a-K1*sysd.b)
sysd.a=sysd.a-K1*sysd.b;
sysd.b=zeros(size(sysd.b));
figure(2)
step(2*sysd)