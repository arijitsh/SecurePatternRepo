A=[-1 -3;3 -5];
B=[2 -1;1 0];
C=[0.8 2.4;1.6 0.8];
K=[2];
pgrid=ss(A-B*K,B,C,zeros(size(B)),3);
step(pgrid)