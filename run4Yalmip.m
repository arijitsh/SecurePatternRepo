addpath(genpath('C:\Program Files\MATLAB\R2018a\toolbox\sdpt3-master\'));
install_sdpt3;
addpath(genpath('C:\Program Files\MATLAB\R2018a\toolbox\YALMIP-master\'));
yalmiptest;
sdpsettings('verbose',0,'solver','sdpt3');
clc;