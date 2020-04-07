clear;
clc;
cla;
clf;
Aa = [0 1;
      0 0];
Bb = [0;
      1];
Cc = [1 0];
Dd = 0;
sys_ss = ss(Aa,Bb,Cc,Dd);

Ts = 0.1;
sys_d = c2d(sys_ss,Ts,'zoh');

A = sys_d.a;
B = sys_d.b;
C = sys_d.c;
D = sys_d.d;


p = 1;
Q = p*(C'*C);
R = 0.1;
% [K,S,E] = dlqr(A,B,Q,R)
K = [16.0302    5.6622];
abs(eig(A-B*K))

P = [0.1519    0.1073;
    0.1073    0.1465];
QN=0.01;
RN=0.0001;

% [KEST,L,P] = kalman(sys_d,QN,RN)
% L = [1.8721;9.6532];

for i=1:100000
    L=(P*C')/(C*P*C'+RN);
    P=(eye(2)-L*C)*P;
    P=A*P*A'+QN;
end
L
abs(eig(A-L*C))

time=30;
plot_dist=zeros(1,time);
plot_vel=zeros(1,time);
plot_dist_hat=zeros(1,time);
plot_vel_hat=zeros(1,time);

ak1 = 0;
ak2 = 0;

au = [ak1 zeros(1, time-size(ak1,2))];
ay = [ak2 zeros(1, time-size(ak2,2))];

pattern = ones(1,time);
% subseq = [1 1 1 1 0 0 1 0 1 0 0 0];
% repeat = ceil(size(pattern,2)/size(subseq,2));
% offset = 0;
% for i=1:repeat    
%     for j=1:2
%         if offset+j< size(pattern,2)
%             pattern(offset+j) = subseq(j);
%         end
%     end
%     offset = offset + size(subseq,2);
% end

x = [3;3];
xhat = [0;0];
u_attacked = 0;
y = C*x;
yhat = C*xhat;

u = 0;
  
for i=1:time
    i;
    r = y - yhat;
    r_norm = abs(r);
    xhat = A*xhat + B*u + L*r;
    x = A*x + B*u_attacked    ;
    
    if pattern(i)==1
        u = -(K*xhat);
        u_attacked = u + au(i);
    else
        u = u;
        u_attacked = u_attacked;
    end
    
    y = C*x + ay(i);
    yhat = C*xhat;
    
    plot_dist(i) = x(1);
    plot_vel(i) = x(2);
    plot_dist_hat(i) = xhat(1);
    plot_vel_hat(i) = xhat(2);
   
end

fontsize = 10;
linewidth = 1;
markersize = 10;


hold on;
plot(plot_dist);
plot(plot_dist_hat);
hold off;