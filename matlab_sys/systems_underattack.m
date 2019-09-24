clear;
clc;

%%%%%%%%%%%%%%%%%%%%%%%%%%% Power grid %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
A=[-1 -3;3 -5];
B=[2 -1;1 0];
C=[0.8 2.4;1.6 0.8];
D=zeros(size(C,1),size(B,2));
K=[2];

Ts = 1;
pgrid = ss(A,B,C,D);
pgrid_d=ss(A,B,C,zeros(size(B)),Ts);
controllability_cc=[rank(pgrid_d.a)==rank(ctrb(pgrid_d))];
p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
pgrid_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(pgrid_cl)
% pgrid_cl =ss(A-B*K,B,C,D,Ts);
step(pgrid_cl)

QN =1;
RN = eye(size(C,1));
[KEST,L,PN] = kalman(pgrid_d,QN,RN)

% for i=1:1000000
%     L=(PN*C')/(C*PN*C'+RN);
%     PN=(eye(size(C,1))-L*C)*PN;
%     PN=(A*PN*A'+QN);
% end

time = 10;
plot_vectorx1 = ones(1,time);
plot_vectorx2 = ones(1,time);
plot_vectorz1 = ones(1,time);
plot_vectorz2 = ones(1,time);


x = zeros(size(A,1),1);
z = 0.1*ones(size(A,1),1);
u = zeros(size(A,1),1);


for i=1:time
    y = C*x
    r = C*x - C*z;
    x = A*x + B*u;
    z = A*z + B*u + L*r;
    u = -K*x;
    
    plot_vectorx1(i) = x(1);
    plot_vectorz1(i) = z(1);
    plot_vectorx2(i) = x(2);
    plot_vectorz2(i) = z(2);
end

fontsize = 10;
linewidth = 1;

clf;
subplot(1,2,1);
hold on;
plot(plot_vectorx1,'LineWidth',linewidth);
plot(plot_vectorz1,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

subplot(1,2,2);
hold on;
plot(plot_vectorx2,'LineWidth',linewidth);
plot(plot_vectorz2,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

