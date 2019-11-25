% Steering angle as input
% side slip and yaw rate

clear;
clear;
clc;
cla;
clf;

% parameters
m = 1573; %kg
v = 30; % m/s
lf = 1.1; %m
lr = 1.58; %m
l = lr + lf;
Cf = 80000; %N/rad
Cr = 80000; %N/rad
Iz = 2873; %kg m^2
mu = 0.5;
g = 9.8; %m/s^2
steering_angle = 30; % degree
steering_ratio = 0.0625;
Ku = (m*((lr*Cr)-(lf*Cf)))/(l*Cf*Cr);

a11 = (-2)*((Cf+Cr)/(m*v));
a12 = -1-(((2*Cf*lf)-(2*Cr*lr))/(m*v*v));
a21 = (-2)*(((lf*Cf)-(lr*Cr))/Iz);
a22 = (-2)*(((lf*lf*Cf)+(lr*lr*Cr))/(Iz*v));
b1 = (2*Cf)/(m*v);
b2 = (2*Cf*lf)/Iz;

A = [a11 a12;
     a21 a22];
B = [b1;
      b2];
C = [0 1];
D = 0;

sys = ss(A,B,C,D);
Ts = 0.04;
sys_d = c2d(sys,Ts, 'zoh');

A = sys_d.A;
B = sys_d.B;
C = sys_d.C;
D = sys_d.D;

co = ctrb(sys_d);
isControllable = [rank(A) == rank(co)]
Q = 1000*eye(size(A,1));
Q(1,1) = 10000000;
R = eye(size(B,2));
[K,S,E] = dlqr(A,B,Q,R)
abs(eig(A-B*K))

ob = obsv(sys_d);
isObservable = [rank(A) == rank(ob)]
QN = 1;
RN = eye(size(C,1));
[KEST,L,P,M,Z] = kalman(sys_d,QN,RN)
abs(eig(A - L*C))

time = 50;
plot_yaw = zeros(1, time);
plot_yawestimate = zeros(1, time);
plot_sideslip = zeros(1, time);
plot_sideslipestimate = zeros(1, time);

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

x = [1;2];
xhat = [-1;-2];
delta = steering_angle*(pi/180)*steering_ratio;  
u = -K*xhat;
% u =  delta;
for i=1:time        
    y = C*x + D*u;
    yhat = C*xhat + D*u;
    r = y - yhat;
    x = A*x + B*u;
    xhat = A*xhat + B*u + L*r;
    
    if pattern(i)==1
        u = -(K*xhat);
    end
    
    plot_sideslip(i) = x(1);
    plot_sideslipestimate(i) = xhat(1);
    plot_yaw(i) = x(2);
    plot_yawestimate(i) = xhat(2);
end

fontsize = 10;
linewidth = 1;

clf;
hold on;
plot(plot_yaw);
plot(plot_yawestimate);
% plot(plot_sideslip);
% plot(plot_sideslipestimate);
set(gca,'FontSize',fontsize)
xlabel('Time(x40x10^{-3})(s)','FontSize',fontsize);
ylabel('rad/s','Fontsize',fontsize);
legend({'yaw rate','estimated yaw '},'FontSize',fontsize);
grid on;
hold off;
