% % ESP with periodic
% 
% % sideslip = [0.0000032461 0.0000013812 1.1000013812 4.661828327 0.0000013812 0.0000013812 0.0000024746]
% % yawrate = [0.0000013812 0.0000048081 91.214143341 39.1669726902 0.0000006906 0.0000624281 0.0000101917]
% % r = [0.0 0.0029986187 0.0000013812 0.0000013812 0.0001141655 0.0000411334 0.0000172389]
% 
% % sideslip = [0.0 0 0.0301488806 0.1277715436 2.72e-08 0 0]
% % yawrate = [0 0 2.4999999999 1.0734908963 2.291e-07 0 0]
% % r = [0 0.0029999999 0.0007281573 0 0 0 0]
% 
% 
% safe_sideslip = 1*ones(1,7)
% safe_yawrate = 2*ones(1,7)
% th = 0.003*ones(1,7)
% 
% 
% fontsize = 40
% linewidth = 2
% 
% clf;
% subplot(1,2,1);
% hold on;
% % plot(safe_sideslip,'b','LineWidth',linewidth);
% % plot(sideslip,'r','LineWidth',linewidth);
% plot(safe_yawrate,'b','LineWidth',linewidth);
% plot(yawrate,'r','LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% % xlabel('Time(x 0.1)(s)','FontSize',fontsize);
% % ylabel('rad/s','Fontsize',fontsize);
% legend({'safe \beta','\beta under attack','safe \gamma','\gamma under attack'},'FontSize',fontsize);
% axis([1 7 -0.5 3])
% grid on;
% hold off;
% 
% subplot(1,2,2);
% hold on;
% plot(th,'LineWidth',linewidth);
% plot(r,'LineWidth',linewidth);
% set(gca,'FontSize',fontsize)
% % xlabel('Time(x 0.1)(s)','FontSize',fontsize);
% % ylabel('rad/s','Fontsize',fontsize);
% legend({'Th','|| r ||'},'FontSize',fontsize);
% axis([1 time -0.01 0.06]);
% grid on;
% hold off;


% trajectory tracking

dist = [0.1 0.000157937 1.1003158741 1.1304823248 0.0003158741]
vel = [0.998420629 0.998420629 23.0015793709 22.3982503569]
r = [0 0.0003158741 0.0279617361]
