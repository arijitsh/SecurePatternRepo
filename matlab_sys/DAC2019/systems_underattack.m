clear;
clc;

%%%%%%%%%%%%%%%%%%%%%%%%%%% Power grid %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A=[-1 -3;3 -5];
% B=[2 -1;1 0];
% C=[0.8 2.4;1.6 0.8];
% D=zeros(size(C,1),size(B,2));
% 
% Ts = 1;
% pgrid = ss(A,B,C,D);
% pgrid_d=ss(A,B,C,zeros(size(B)),Ts);
% controllability_cc=[rank(pgrid_d.a)==rank(ctrb(pgrid_d))];
% p = 100;
% Q = p*eye(size(A));
% R = 0.1*eye(size(B,2),size(B,2));
% K = dlqr(A,B,Q,R)
% pgrid_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
% isstable(pgrid_cl)
% % pgrid_cl =ss(A-B*K,B,C,D,Ts);
% step(pgrid_cl)
% 
% QN =1;
% RN = eye(size(C,1));
% [KEST,L,PN] = kalman(pgrid_d,QN,RN)

% % for i=1:1000000
% %     L=(PN*C')/(C*PN*C'+RN);
% %     PN=(eye(size(C,1))-L*C)*PN;
% %     PN=(A*PN*A'+QN);
% % end
% 
% time = 10;
% plot_vectorx1 = ones(1,time);
% plot_vectorx2 = ones(1,time);
% plot_vectorz1 = ones(1,time);
% plot_vectorz2 = ones(1,time);
% 
% 
% x = zeros(size(A,1),1);
% z = 0.1*ones(size(A,1),1);
% u = zeros(size(B,2),1);


% for i=1:time
%     y = C*x
%     r = C*x - C*z;
%     x = A*x + B*u;
%     z = A*z + B*u + L*r;
%     u = -K*x;
%     
%     plot_vectorx1(i) = x(1);
%     plot_vectorz1(i) = z(1);
%     plot_vectorx2(i) = x(2);
%     plot_vectorz2(i) = z(2);
% end
% 
% fontsize = 10;
% linewidth = 1;
% 
% clf;
% subplot(1,2,1);
% hold on;
% plot(plot_vectorx1,'LineWidth',linewidth);
% plot(plot_vectorz1,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(1,2,2);
% hold on;
% plot(plot_vectorx2,'LineWidth',linewidth);
% plot(plot_vectorz2,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;


%%%%%%%%%%%%%%%%%%%%%%%%%%% Cruise Control %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A = [ 0       1       0;
%       0       0       1;
%   -6.0476  -5.2856  -0.238];  
% B = [0; 0; 2.4767];
% C = [1 0 0];
% D = 0;
% cruise_contrl=ss(A,B,C,D)
% Ts = .01;
% cruise_contrl_d = c2d(cruise_contrl,Ts,'zoh');
% controllability_cc=[rank(cruise_contrl_d.a)==rank(ctrb(cruise_contrl_d))]
% 
% A = cruise_contrl_d.a
% B = cruise_contrl_d.b
% C = cruise_contrl_d.c
% D = cruise_contrl_d.d
% 
% p = 100;
% Q = p*eye(3);
% R = 1;
% K = dlqr(A,B,Q,R)
% abs(eig(A - B*K))
% 
% QN = 1;
% RN = 1;
% [KEST,L,P] = kalman(cruise_contrl_d,QN,RN)
% % P = 1.0e-02 * [1    1   1;
% %                1    1   1;
% %                1    1   1];
% 
% for i=1:1000
%     L=P*C'*inv(C*P*C'+RN);
%     P=(eye(3)-L*C)*P;
%     P=(A*P*A'+QN);
% end
% 
% 
% cruise_contrl_cl = ss(A-B*K,zeros(size(B)),C,D,Ts);
% isstable(cruise_contrl_cl)
% 
% time = 1000;
% plot_vectorx1 = ones(1,time);
% plot_vectorx2 = ones(1,time);
% plot_vectorx3 = ones(1,time);
% plot_vectorxnorm = ones(1,time);
% plot_vectorz1 = ones(1,time);
% plot_vectorz2 = ones(1,time);
% plot_vectorz3 = ones(1,time);
% plot_vectorznorm = ones(1,time);
% 
% 
% x = zeros(size(A,1),1);
% z = 0.001*ones(size(A,1),1);
% u = zeros(size(B,2),1);
% 
% 
% for i=1:time
%     y = C*x;
%     r = C*x - C*z;
%     x = A*x + B*u;
%     z = A*z + B*u + L*r;
%     u = -K*x;
%     
%     plot_vectorx1(i) = x(1);
%     plot_vectorz1(i) = z(1);
%     plot_vectorx2(i) = x(2);
%     plot_vectorz2(i) = z(2);
%     plot_vectorx3(i) = x(3);
%     plot_vectorz3(i) = z(3);
%     plot_vectorxnorm(i) = norm(x,1);
%     plot_vectorznorm(i) = norm(z,1);
% end
% 
% fontsize = 10;
% linewidth = 1;
% 
% clf;
% subplot(2,2,1);
% hold on;
% plot(plot_vectorx1,'LineWidth',linewidth);
% plot(plot_vectorz1,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,2);
% hold on;
% plot(plot_vectorx2,'LineWidth',linewidth);
% plot(plot_vectorz2,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,3);
% hold on;
% plot(plot_vectorx3,'LineWidth',linewidth);
% plot(plot_vectorz3,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,4);
% hold on;
% plot(plot_vectorxnorm,'LineWidth',linewidth);
% plot(plot_vectorznorm,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;

%%%%%%%%%%%%%%%%%%%%%%%%%%%% water treatmnt %%%%%%%%%%%%%%%%%%%%%%%%%%%
% A=[-20 1;0 .1];
% B=[0;1];
% C=[1 0];
% D=[0];
% water_plant=ss(A,B,C,D);
% Ts=0.2;
% water_plant_d=c2d(water_plant,Ts)
% controllability_wp=[rank(water_plant_d.a)==rank(ctrb(water_plant_d))]
% 
% A = water_plant_d.a
% B = water_plant_d.b
% C = water_plant_d.c
% D = water_plant_d.d
% 
% p = 100;
% Q = p*eye(size(A));
% R = 0.1*eye(size(B,2),size(B,2));
% K = dlqr(A,B,Q,R)
% water_plant_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
% isstable(water_plant_cl)
% 
% QN = 0.00001;
% RN = 0.00001;
% [KEST,L,P] = kalman(water_plant_d,QN,RN)
% % P = 1.0e-02 * [1    1   1;
% %                1    1   1;
% %                1    1   1];
% 
% % for i=1:1000
% %     L=P*C'*inv(C*P*C'+RN);
% %     P=(eye(2)-L*C)*P;
% %     P=(A*P*A'+QN);
% % end
% 
% 
% time = 400;
% plot_vectorx1 = ones(1,time);
% plot_vectorx2 = ones(1,time);
% plot_vectorxnorm = ones(1,time);
% plot_vectorz1 = ones(1,time);
% plot_vectorz2 = ones(1,time);
% plot_vectorznorm = ones(1,time);
% 
% 
% x = zeros(size(A,1),1);
% z = ones(size(A,1),1);
% u = zeros(size(B,2),1);
% 
% 
% for i=1:time
%     y = C*x;
%     r = C*x - C*z;
%     x = A*x + B*u;
%     z = A*z + B*u + L*r;
%     u = -K*x;
%     
%     plot_vectorx1(i) = x(1);
%     plot_vectorz1(i) = z(1);
%     plot_vectorx2(i) = x(2);
%     plot_vectorz2(i) = z(2);
%     plot_vectorxnorm(i) = norm(x,1);
%     plot_vectorznorm(i) = norm(z,1);
% end
% 
% fontsize = 10;
% linewidth = 1;
% 
% clf;
% subplot(2,2,1);
% hold on;
% plot(plot_vectorx1,'LineWidth',linewidth);
% plot(plot_vectorz1,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,2);
% hold on;
% plot(plot_vectorx2,'LineWidth',linewidth);
% plot(plot_vectorz2,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,3);
% hold on;
% plot(plot_vectorxnorm,'LineWidth',linewidth);
% plot(plot_vectorznorm,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;

%%%%%%%%%%%%%%%%%%%%%%%%%%% temperature control %%%%%%%%%%%%%%%%%%%%%%%
% A=[-0.11 0.1;0 -50];
% B=[0;-50];
% C=[1 0];
% D=[0];
% tmp_cntrl=ss(A,B,C,D);
% Ts=0.5;
% tmp_cntrl_d=c2d(tmp_cntrl,Ts);
% controllability_tc=[rank(tmp_cntrl_d.a)==rank(ctrb(tmp_cntrl_d))]
% 
% A = tmp_cntrl_d.a
% B = tmp_cntrl_d.b
% C = tmp_cntrl_d.c
% D = tmp_cntrl_d.d
% 
% p = 100;
% Q = p*eye(size(A));
% R = 0.1*eye(size(B,2),size(B,2));
% K = dlqr(A,B,Q,R)
% tmp_cntrl_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
% isstable(tmp_cntrl_cl)
% 
% QN = 0.00001;
% RN = 0.00001;
% [KEST,L,P] = kalman(tmp_cntrl_d,QN,RN)
% 
% for i=1:1000
%     L=P*C'*inv(C*P*C'+RN);
%     P=(eye(size(A,1))-L*C)*P;
%     P=(A*P*A'+QN);
% end
% 
% 
% time = 5;
% plot_vectorx1 = ones(1,time);
% plot_vectorx2 = ones(1,time);
% plot_vectorxnorm = ones(1,time);
% plot_vectorz1 = ones(1,time);
% plot_vectorz2 = ones(1,time);
% plot_vectorznorm = ones(1,time);
% 
% ak1 = [-0.0500038552 0.0500047252];
% ak1 = [0];
% attackOnU = [ak1 zeros(1,time-size(ak1,2))];
% 
% ak2 = [-0.0000038552 -0.0023800349];
% ak2 = [0];
% attackOnY = [ak2 zeros(size(C,1),time-size(ak1,2))]
% 
% x = zeros(size(A,1),1)
% z = ones(size(A,1),1)
% u = zeros(size(B,2),1);
% u_attacked = zeros(size(B,2),1);
% r = zeros(size(C,1));
% 
% for i=1:time
%     i
%     
%     z = A*z + B*u + L*r
%     x = A*x + B*u_attacked    
%     attackOnU(i)
%     u = -K*x
%     u_attacked = u + attackOnU(i)
%     attackOnY(:,i)
%     y = C*x 
%     y_attacked = y + attackOnY(:,i)
%     r = y_attacked - C*z   
%     
%     
%     plot_vectorx1(i) = x(1);
%     plot_vectorz1(i) = z(1);
%     plot_vectorx2(i) = x(2);
%     plot_vectorz2(i) = z(2);
%     plot_vectorxnorm(i) = norm(x,1);
%     plot_vectorznorm(i) = norm(z,1);
% end
% 
% fontsize = 10;
% linewidth = 1;
% 
% clf;
% subplot(2,2,1);
% hold on;
% plot(plot_vectorx1,'LineWidth',linewidth);
% plot(plot_vectorz1,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,2);
% hold on;
% plot(plot_vectorx2,'LineWidth',linewidth);
% plot(plot_vectorz2,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;
% 
% subplot(2,2,3);
% hold on;
% plot(plot_vectorxnorm,'LineWidth',linewidth);
% plot(plot_vectorznorm,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% grid on;
% hold off;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Power system  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%  A = [0.66 0.53;
%        -0.53 0.13];
%  B = [0.34;    %B1=Bp1
%         0.53];
%  C = eye(2);
% %  L=[0.36 0.27;  -0.31 0.08];    
%  D = [0 ;
%         0];
%  K= [0.0556 0.3306];
%  Ts=1;
% pwr_plnt_d =ss(A,B,C,D,Ts);
% controllability_pp=[rank(pwr_plnt_d.a)==rank(ctrb(pwr_plnt_d))]
% pwr_plnt_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
% isstable(pwr_plnt_cl)
% A = pwr_plnt_d.a
% B = pwr_plnt_d.b
% C = pwr_plnt_d.c
% D = pwr_plnt_d.d

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Plant %%%%%%%%%%%%%%%%%%%

A=[1.38 -0.2077 6.715 -5.676;-0.5814 -4.29 0 0.675;
    1.067 4.273 -6.654 5.893;0.048 4.273 1.343 -2.104];
B=[0 0;5.679 0;1.136 -3.146;1.136 0];
C=[1 0 1 -1;0 1 0 0];
D=zeros(2,2);
plant= ss(A,B,C,D);
Ts=0.5
plant_d=c2d(plant,Ts);
controllability_p=[rank(plant_d.a)==rank(ctrb(plant_d))]

A = plant_d.a
B = plant_d.b
C = plant_d.c
D = plant_d.d

p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
plant_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(plant_cl)

QN = 10;
RN = 0.00001*eye(size(C,1));
[KEST,L,P] = kalman(plant_d,QN,RN)

% for i=1:1000
%     L=P*C'*inv(C*P*C'+RN);
%     P=(eye(size(A,1))-L*C)*P;
%     P=(A*P*A'+QN);
% end

time = 30;
plot_vectorx1 = ones(1,time);
plot_vectorx2 = ones(1,time);
plot_vectorx3 = ones(1,time);
plot_vectorx4 = ones(1,time);
plot_vectorxnorm = ones(1,time);
plot_vectorz1 = ones(1,time);
plot_vectorz2 = ones(1,time);
plot_vectorz3 = ones(1,time);
plot_vectorz4 = ones(1,time);
plot_vectorznorm = ones(1,time);


x = zeros(size(A,1),1);
z = 0.001*ones(size(A,1),1);
u = zeros(size(B,2),1);


for i=1:time
    y = C*x;
    r = C*x - C*z;
    x = A*x + B*u;
    z = A*z + B*u + L*r;
    u = -K*x;
    
    plot_vectorx1(i) = x(1);
    plot_vectorz1(i) = z(1);
    plot_vectorx2(i) = x(2);
    plot_vectorz2(i) = z(2);
    plot_vectorx3(i) = x(3);
    plot_vectorz3(i) = z(3);
    plot_vectorx4(i) = x(4);
    plot_vectorz4(i) = z(4);
    plot_vectorxnorm(i) = norm(x,1);
    plot_vectorznorm(i) = norm(z,1);
end

fontsize = 10;
linewidth = 1;

clf;
subplot(2,3,1);
hold on;
plot(plot_vectorx1,'LineWidth',linewidth);
plot(plot_vectorz1,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

subplot(2,3,2);
hold on;
plot(plot_vectorx2,'LineWidth',linewidth);
plot(plot_vectorz2,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

subplot(2,3,3);
hold on;
plot(plot_vectorx3,'LineWidth',linewidth);
plot(plot_vectorz3,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

subplot(2,3,4);
hold on;
plot(plot_vectorx4,'LineWidth',linewidth);
plot(plot_vectorz4,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;

subplot(2,3,5);
hold on;
plot(plot_vectorxnorm,'LineWidth',linewidth);
plot(plot_vectorznorm,'LineWidth',linewidth);
set(gca,'FontSize',fontsize)
grid on;
hold off;
