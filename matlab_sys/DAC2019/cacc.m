clear;
clc;
cla;
clf;

tau = 0.8;

A = [0 -1 0; 0 0 1; 0 0 -(1/tau)];
B = [0;0;1];
C = [1 0 0;0 1 0];
D = [0 ; 0];

Ts = 0.01;

sys_ss = ss(A,B,C,D);

sys_d = c2d(sys_ss,Ts,'zoh');

A = sys_d.a;
B = sys_d.b;
C = sys_d.c;
D = sys_d.d;

p = 1;
Q = p*(C'*C);
R = 1
[K,S,E] = dlqr(A,B,Q,R);
abs(eig(A-B*K))

QN=0.01;
RN=0.0001*eye(size(C,1));

[KEST,L,P] = kalman(sys_d,QN,RN)
abs(eig(A-L*C))

x = [1;10;2];
y = C*x;
z = [0;0;0];
u = 0;

time=1000;
plot_dist=zeros(1,time);
plot_vel=zeros(1,time);
plot_acc=zeros(1,time);

for i=1:time
   x = A*x + B*u; 
   r = C*x - C*z;
   z = A*z + B*u + L*r;
   u = -K*z;
   
   plot_dist(i) = x(1);
   plot_vel(i) = x(2);
   plot_acc(i) = x(3);
end

hold on;
plot(plot_dist);
plot(plot_vel);
plot(plot_acc);
hold off;