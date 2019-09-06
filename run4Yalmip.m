
addpath(genpath('/media/sunandan/DATA/Games n Apps/sdpt3-master/'));
install_sdpt3;
addpath(genpath('/media/sunandan/DATA/Games n Apps/YALMIP-master/'));
yalmiptest;
sdpsettings('verbose',0,'solver','sdpt3');
clc;