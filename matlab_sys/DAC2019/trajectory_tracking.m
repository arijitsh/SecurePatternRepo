A = [1 0.01;0 1];
B = [0.0001;0.01];
C = eye(2);
D = [0;0];

sys =ss(A,B,C,D);
p = 1;
Q = p*(C'*C);
R = 1;
[K,S,E] = dlqr(A,B,Q,R);
K= [16.0302    5.6622];
abs(eig(A-B*K))


L = [0.6180 0.0011; 0.0011 0.6180];


x = [1;1];
y = C*x;
z = [0;0];
u = 0;

time=1000;
plot_dist=zeros(1,time);
plot_vel=zeros(1,time);

for i=1:time
   x = A*x + B*u; 
   r = C*x - C*z;
   z = A*z + B*u + L*r;
   u = -K*z;
   
   plot_dist(i) = x(1);
   plot_vel(i) = x(2);
   
end


hold on;
plot(plot_dist);
plot(plot_vel);
hold off;