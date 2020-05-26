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


p = 500;
Q = p*(C'*C);
R = 0.1;
[K,S,E] = dlqr(A,B,Q,R);
K = [16.0302    5.6622];
abs(eig(A-B*K))

P = [0.1519    0.1073;
    0.1073    0.1465];
QN=0.01;
RN=0.0001;

[KEST,L,P] = kalman(sys_d,QN,RN)
% L = [1.8721;9.6532];
L = [0.9902;0.9892];
abs(eig(A-L*C))

x = [1;10];
y = C*x;
z = [0;0];
u = 0;

time=30;
plot_dist=zeros(1,time);
plot_vel=zeros(1,time);
plot_rnorm = zeros(1, time);

% dist_prev_1 = [0.1 0.000157937];
% vel_prev_1 = [0.998420629 0.998420629];
% r_prev_1 = [0 0.0003158741];

dist_prev_1 = [0.1 0.5];
vel_prev_1 = [0.998420629 2];
r_prev_1 = [0 0.05];

plot_th = 0.05*ones(1, time+size(dist_prev_1,2));
plot_safedist = 1*ones(1, time+size(dist_prev_1,2));
plot_safevel = 10*ones(1, time+size(dist_prev_1,2));

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

% x = [0.000157937;0.998420629];
% x = [0.5;2];
x = [12;15];
% xhat = [-0.0498;0.9984];
% xhat = [0.75;8];
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
    
    plot_dist(i) = abs(x(1));
    plot_vel(i) = abs(x(2));
    plot_rnorm(i) = r_norm;
   
end

fontsize = 10;
linewidth = 1;
markersize = 10;

dist_final_1 = [dist_prev_1 plot_dist];
vel_final_1 = [vel_prev_1 plot_vel];
r_final_1 = [r_prev_1 plot_rnorm];


subplot(1,2,1);
hold on;
plot(plot_safedist,'r','LineWidth',linewidth);
plot(dist_final_1,'r--','LineWidth',linewidth);
% plot(plot_safevel,'b','LineWidth',linewidth);
% plot(vel_final_1,'b--','LineWidth',linewidth);

set(gca,'FontSize',fontsize);
% axis([1 time+2 -0.2 2.2]);

xlabel('Time(x0.1)(s)','FontSize',fontsize);
ylabel('\beta (rad), \gamma (rad/s)','FontSize',fontsize);
% legend({'safe \beta','\beta','safe \gamma','\gamma'},'FontSize',fontsize);
grid on;
hold off;

subplot(1,2,2);
hold on;
plot(plot_th,'LineWidth',linewidth);
plot(r_final_1,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
xlabel('Time(x0.1)(s)','FontSize',fontsize);
ylabel('residue','FontSize',fontsize);
legend({'Th','|| r ||'},'FontSize',fontsize);
% axis([1 time -0.001 0.0035])
grid on;
hold off;
