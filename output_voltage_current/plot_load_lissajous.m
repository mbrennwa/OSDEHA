% plot tube curves with theoretical load "line" for a capacitive load to the tube anode(s)
%
% current I
% voltage U
% capacitor C
% time t
% frequency f
%
% capacitor: I = C x dU/dt
% applied voltage: U = U0 x sin(2pi f t) --> dU/dt = 2pi x f x U0 x cos(2pi f t)
% --> I = C x 2pi x f x U0 x cos(2pi f t)

tubecurves = '801A_1.dat';
tubename   = '801';

C  = 100e-12; % capacitance in Farads
% Ra = 66E3;    % AC resistance of anode resistor/CCS in Ohms
Ra = 10e6;    % AC resistance of anode resistor/CCS in Ohms
U0 = 650/2; % Voltage amplitude (Vpk)

% DC bias point:
Ubias = 500
Ibias = 20E-3

lw = 1.5;

% load tube curves:
x = str2num(fileread('801A_1.dat'));
Ug = unique(x(:,6)); Ug(Ug==0)=0;
for k = 1:length(Ug)
	l = find(x(:,6)==Ug(k));
	plot (x(l,1),1000*x(l,4),'k-', 'linewidth', lw);
	hold on
end


ff = [1E3,3e3,1e4,3e4,1e5];

for f=ff
	t  = linspace(0,1/f,300);
	U  = U0 * sin(2*pi*f*t);
	IC = C * 2*pi * f * U0 * cos(2*pi*f*t);
	IR = U / Ra;
	I  = IC + IR;
	plot(U+Ubias,1000*(-I+Ibias),'r-','linewidth',lw); hold on
end
r = axis(); r(1) = 0; r(3) = 0; axis(r) 
plot([r(1),Ubias],[Ibias,Ibias]*1000,'b-','linewidth',lw);
plot([Ubias,Ubias],[r(3),Ibias*1000],'b-','linewidth',lw);
plot(Ubias,Ibias*1000,'.','color','b','markersize',20);
hold off

xlabel('Anode-Cathode Voltage (V)')
ylabel('Anode Current (mA)')

% ,

title(sprintf("%s Tube Curves, Grid Voltages %g, %g,...,%g V\nLoad Lines: Anode Resistor (%g kOhm) + Estat Headphone (%g pF)\nSine Signals at %s kHz", tubename, Ug(end), Ug(end-1), Ug(1), Ra/1000,C*1E12, strrep(sprintf('%.0f,' , ff/1000)(1:end-1),',',', ')));
