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
abs(eig(A-B*K))

P = [0.1519    0.1073;
    0.1073    0.1465];
QN=0.01;
RN=0.0001;

[KEST,L,P] = kalman(sys_d,QN,RN)
abs(eig(A-L*C))

x = [1;10];
y = C*x;
z = [0;0];
u = 0;

time=100;
plot_vector1=zeros(1,time);
plot_vector2=zeros(1,time);
plot_vector3=zeros(1,time);
plot_vector4=zeros(1,time);
plot_vector5=zeros(1,time);
plot_vector6=zeros(1,time);
plot_vector7=zeros(1,time);
plot_vector8=zeros(1,time);
plot_vector9=zeros(1,time);
plot_vector10=zeros(1,time);
plot_vector11=zeros(1,time);
time_axis=zeros(1,time);

pattern = ones(1,time);
subseq = [1 0];
repeat = ceil(size(pattern,2)/size(subseq,2));
offset = 0;
for i=1:repeat    
    for j=1:2
        if offset+j< size(pattern,2)
            pattern(offset+j) = subseq(j);
        end
    end
    offset = offset + size(subseq,2);
end
  
for i=1:time
    i;   
    
    y= C*x;
    y_hat= C*z;
    r= y - y_hat;
    z= A*z + B*u + L*r;
    x= A*x + B*u;
    
    if pattern(i)==1 
        u= -K*z;
    end 
    
    time_axis(i)=i;
    plot_vector1(i)=x(1);
    plot_vector2(i)=z(1);
    plot_vector3(i)=x(2);
    plot_vector4(i)=z(2);
    
   
end

fontsize = 10;
linewidth = 1;
markersize = 10;

clf
hold on;
plot(plot_vector1,'LineWidth',linewidth);
plot(plot_vector2,'LineWidth',linewidth);
% plot(plot_vector3,'LineWidth',linewidth);
% plot(plot_vector4,'LineWidth',linewidth);
% axis([1 time 0 0.1])
xlabel('Time(x10^{-1})(s)','FontSize',fontsize);
ylabel('residue','FontSize',fontsize);
grid on;
hold off;
