    clear;
clc;
clf;

% parameters
m = 1070; %kg
v = 30; % m/s
lf = 1.1; %m
lr = 1.3; %m
l = lr + lf;
Cf = 90624; %N/rad
Cr = 90624; %N/rad
Iz = 2100; %kg m^2
delta = 0.52;
mu = 0.5;
g = 9.8; %m/s^2
steering_ratio = 0.0625; %15:1
Ku = (m*((lr*Cr)-(lf*Cf)))/(l*Cf*Cr);
max_sideslip = atan(0.02*mu*g);

a11 = (-2)*((Cf+Cr)/(m*v));
a12 = -1-(((2*Cf*lf)-(2*Cr*lr))/(m*v*v));
a21 = (-2)*(((lf*Cf)-(lr*Cr))/Iz);
a22 = (-2)*(((lf*lf*Cf)+(lr*lr*Cr))/(Iz*v));
b1 = (2*Cf)/(m*v);
b2 = (2*Cf*lf)/Iz;
b3 = 0;
b4 = 1/Iz;

% Discretizing the state space
A = [a11 a12;
     a21 a22];
C = [0 1;
    (v*a11) (v*(a12 + 1))];
D = [0 0;
    (v*b1) 0];
B = [b1 b3;
     b2 b4];

sys = ss(A,B,C,D);
Ts = .04;
sys_d = c2d(sys,Ts, 'zoh');

% step(sys_d)

A = sys_d.A;
B = sys_d.B;
C = sys_d.C;
D = sys_d.D;

co = ctrb(sys_d);
isControllable = [rank(A) == rank(co)]
% Q = 1000*eye(size(A,1));
% Q(1,1) = 10000000;
Q = eye(size(A,1));
R = eye(size(B,2));
[K,S,E] = dlqr(A,B,Q,R)
abs(eig(A-B*K))

% K=[ 6.7458171835 0.0076120267;
%   0 65536.0];

% Observer gain computation
QN = 1;
RN = eye(size(C));
[KEST,L,P,M,Z] = kalman(sys_d,QN,RN)
abs(eig(A - L*C))

x = [0.05;0.2];
x0 = [0;0];
xhat = [0;0];
xhat0 = [0;0];
y = C*x;
yhat = C*xhat;

u = [delta;0];

time = 10;
plot_r = zeros(1, time);
plot_r1 = zeros(1, time);
plot_yaw = zeros(1, time);
plot_sideslip = zeros(1, time);
plot_yawhat = zeros(1, time);
plot_sidesliphat = zeros(1, time);

for i=1:time
    r = y - yhat;
    x = A*x + B*u;
    xhat = A*xhat + B*u + L*r;
    u = -(K*xhat) ;%+ [delta;0];
    y = C*x + D*u;
    yhat = C*xhat + D*u;            
    
    plot_r(i) = r(1);
    plot_r1(i) = r(2);
    plot_sideslip(i) = x(1);
    plot_sidesliphat(i) = xhat(1);
    plot_yaw(i) = x(2);
    plot_yawhat(i) = xhat(2);
end

linewidth = 1;
fontsize = 20;

subplot(1,2,1);
hold on;
plot(plot_yaw,'Linewidth',linewidth);
plot(plot_yawhat,'Linewidth',linewidth);
set(gca,'FontSize',fontsize)
xlabel('Time(x40x10^{-3})(s)','FontSize',fontsize);
ylabel('rad/s','Fontsize',fontsize);
legend({'yaw rate','estimated yaw rate'},'FontSize',fontsize);
grid on;
hold off;

subplot(1,2,2);
hold on;
plot(plot_sideslip,'Linewidth',linewidth);
plot(plot_sidesliphat,'Linewidth',linewidth);
set(gca,'FontSize',fontsize)
xlabel('Time(x40x10^{-3})(s)','FontSize',fontsize);
ylabel('rad','Fontsize',fontsize);
legend({'side slip','estimated side slip'},'FontSize',fontsize);
grid on;
hold off;