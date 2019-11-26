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
Ts = 0.1;
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

time = 3;
pattern = ones(1,time);
% subseq = [1 0];
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

plot_yaw = zeros(1, time);
plot_yawestimate = zeros(1, time);
plot_sideslip = zeros(1, time);
plot_sideslipestimate = zeros(1, time);
plot_rnorm = zeros(1, time);


sideslip_prev_1 = [0.0000032461 0.8];
yawrate_prev_1 = [0.0000013812 1.8];
r_prev_1 = [0.0 0.0029986187];

plot_th = 0.003*ones(1, time+size(sideslip_prev_1,2));
plot_safesideslip = 1*ones(1, time+size(sideslip_prev_1,2));
plot_safeyawrate = 2*ones(1, time+size(sideslip_prev_1,2));

ak1 = 0;
ak2 = 0;

au = [ak1 zeros(1, time-size(ak1,2))];
ay = [ak2 zeros(1, time-size(ak2,2))];

% x = [0.0000013812;0.0000048081]
x = [0.001;0.00018];
xhat = [0;0]
u = 0.0
u_attacked = 0
y = C*x
yhat = C*xhat
delta = steering_angle*(pi/180)*steering_ratio;  

for i=1:time  
    i
    r = y - yhat
    r_norm = abs(r)
    xhat = A*xhat + B*u + L*r
    x = A*x + B*u_attacked    
    
    if pattern(i)==1
        u = -(K*xhat)
        u_attacked = u + au(i)
    else
        u = u
        u_attacked = u_attacked
    end
    
    y = C*x + ay(i)
    yhat = C*xhat
    
    
    plot_sideslip(i) = x(1);
    plot_sideslipestimate(i) = xhat(1);
    plot_yaw(i) = x(2);
    plot_yawestimate(i) = xhat(2);
    plot_rnorm(i) = r_norm;
end

sideslip_final_1 = [sideslip_prev_1 plot_sideslip];
yawrate_final_1 = [yawrate_prev_1 plot_yaw];
r_final_1 = [r_prev_1 plot_rnorm];



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
time = 3;
plot_yaw_10 = zeros(1, time);
plot_yawestimate_10 = zeros(1, time);
plot_sideslip_10 = zeros(1, time);
plot_sideslipestimate_10 = zeros(1, time);
plot_rnorm_10 = zeros(1, time);


sideslip_prev_10 = [2.658e-07 1.945e-07 0.1 0.2 0.7];
yawrate_prev_10 = [1.6652e-06 3.891e-07 0.9 1.32789752204 1.7];
r_prev_10 = [0.0 0.0000003891 0.0000003891 0.0029996108 0.0029996108];

plot_th = 0.003*ones(1, time+size(sideslip_prev_10,2));
plot_safesideslip = 1*ones(1, time+size(sideslip_prev_10,2));
plot_safeyawrate = 2*ones(1, time+size(sideslip_prev_10,2));

ak1 = 0;
ak2 = 0;

au = [ak1 zeros(1, time-size(ak1,2))];
ay = [ak2 zeros(1, time-size(ak2,2))];

x = [0.7;1.7];
xhat = [0.699995;1.699995];
u = 0.0;
u_attacked = 0;
y = C*x;
yhat = C*xhat;
delta = steering_angle*(pi/180)*steering_ratio;  

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
    
    
    plot_sideslip_10(i) = x(1);
    plot_sideslipestimate_10(i) = xhat(1);
    plot_yaw_10(i) = x(2);
    plot_yawestimate_10(i) = xhat(2);
    plot_rnorm_10(i) = r_norm;
end

fontsize = 10;
linewidth = 1;

sideslip_final_10 = [sideslip_prev_10 plot_sideslip_10];
yawrate_final_10 = [yawrate_prev_10 plot_yaw_10];
r_final_10 = [r_prev_10 plot_rnorm_10];









%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subplot(1,2,1);
hold on;
plot(plot_safesideslip,'r','LineWidth',linewidth);
plot(sideslip_final_10,'r--','LineWidth',linewidth);
plot(plot_safeyawrate,'b','LineWidth',linewidth);
plot(yawrate_final_10,'b--','LineWidth',linewidth);

set(gca,'FontSize',fontsize)
axis([1 time+size(sideslip_prev_10,2) -0.2 2.2])

xlabel('Time(x0.1)(s)','FontSize',fontsize);
ylabel('\beta (rad), \gamma (rad/s)','FontSize',fontsize);
legend({'safe \beta','\beta','safe \gamma','\gamma'},'FontSize',fontsize);
grid on;
hold off;

subplot(1,2,2);
hold on;
plot(plot_th,'LineWidth',linewidth);
plot(r_final_10,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
xlabel('Time(x0.1)(s)','FontSize',fontsize);
ylabel('residue','FontSize',fontsize);
legend({'Th','|| r ||'},'FontSize',fontsize);
% axis([1 time+size(sideslip_prev_10,2) -0.001 0.0035])
grid on;
hold off;
