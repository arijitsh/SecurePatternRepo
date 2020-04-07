%%%%%%%%%%%%%%%%%%%%%%% Power plant:motivating eg %%%%%%%%%%%%%%%%%%%%%%%
 A = [0.66 0.53;
       -0.53 0.13];
 B = [0.34;    %B1=Bp1
        0.53];
 C = eye(2);
%  L=[0.36 0.27;  -0.31 0.08];    
 D = [0 ;
        0];
 K= [0.0556 0.3306];
 Ts=1;
pwr_plnt_d =ss(A,B,C,D,Ts);
controllability_pp=[rank(pwr_plnt_d.a)==rank(ctrb(pwr_plnt_d))]
pwr_plnt_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(pwr_plnt_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%%% Power grid %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
A=[-1 -3;3 -5];
B=[2 -1;1 0];
C=[0.8 2.4;1.6 0.8];
D=zeros(size(C,1),size(B,2));
K=[2];
pgrid_d=ss(A,B,C,zeros(size(B)),3);
controllability_cc=[rank(pgrid_d.a)==rank(ctrb(pgrid_d))];
p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
pgrid_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(pgrid_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%%%% cruise control %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
A = [ 0       1       0;
      0       0       1;
  -6.0476  -5.2856  -0.238];  
B = [0; 0; 2.4767];
C = [1 0 0];
D = 0;
cruise_contrl=ss(A,B,C,D)
Ts = .01;
cruise_contrl_d = c2d(cruise_contrl,Ts,'zoh');
controllability_cc=[rank(cruise_contrl_d.a)==rank(ctrb(cruise_contrl_d))]
p = 100;
Q = p*eye(3);
R = 1;
K = dlqr(A,B,Q,R)

QN = 1;
RN = 1;

P = 1.0e-02 * [1    1   1;
               1    1   1;
               1    1   1];
for i=1:1000
    L=P*C'*inv(C*P*C'+RN);
    P=(eye(3)-L*C)*P;
    P=(A*P*A'+QN);
end
L
cruise_contrl_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(cruise_contrl_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%%%% water treatmnt %%%%%%%%%%%%%%%%%%%%%%%%%%%
A=[-20 1;0 .1];
B=[0;1];
C=[1 0];
D=[0];
water_plant=ss(A,B,C,D);
Ts=0.2;
water_plant_d=c2d(water_plant,Ts)
controllability_wp=[rank(water_plant_d.a)==rank(ctrb(water_plant_d))]

p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
water_plant_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(water_plant_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%%% temperature control %%%%%%%%%%%%%%%%%%%%%%%
A=[-0.11 0.1;0 -50];
B=[0;-50];
C=[1 0];
D=[0];
tmp_cntrl=ss(A,B,C,D);
Ts=0.5;
tmp_cntrl_d=c2d(tmp_cntrl,Ts);
controllability_tc=[rank(tmp_cntrl_d.a)==rank(ctrb(tmp_cntrl_d))]

p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
tmp_cntrl_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(tmp_cntrl_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%% plant %%%%%%%%%%%%%%%%%%%%%%%%%%
A=[1.38 -0.2077 6.715 -5.676;-0.5814 -4.29 0 0.675;
    1.067 4.273 -6.654 5.893;0.048 4.273 1.343 -2.104];
B=[0 0;5.679 0;1.136 -3.146;1.136 0];
C=[1 0 1 -1;0 1 0 0];
D=zeros(2,2);
plant= ss(A,B,C,D);
Ts=0.5
plant_d=c2d(plant,Ts);
controllability_p=[rank(plant_d.a)==rank(ctrb(plant_d))]

p = 100;
Q = p*eye(size(A));
R = 0.1*eye(size(B,2),size(B,2));
K = dlqr(A,B,Q,R)
plant_cl =ss(A-B*K,zeros(size(B)),C,D,Ts);
isstable(plant_cl)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%table=dropStats(length,decay,sys,T,gain)
sys=tmp_cntrl_d
l=50;
d=0.36
T=sys.Ts;
g=[];
dropStats(l,d,sys,T,g);