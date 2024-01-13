% theoretical load "line" for a capacitive load to the tube anode(s)
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

ff = [1E3,3e3,1e4,3e4,1e5];
C  = 100e-12;
U0 = 500; % Voltage amplitude (Vpk)

% DC bias point:
Ubias = 400;
Ibias = 20E-3;

for f=ff
	t  = linspace(0,1/f,300);
	U  = U0 * sin(2*pi*f*t);
	I  = C * 2*pi * f * U0 * cos(2*pi*f*t);
	plot(U+Ubias,1000*(I+Ibias),'r-','linewidth',1); hold on
end
r = axis();
plot([r(1),Ubias],[Ibias,Ibias]*1000,'b-','linewidth',2);
plot([Ubias,Ubias],[r(3),Ibias*1000],'b-','linewidth',2);
plot(Ubias,Ibias*1000,'.','color','b','markersize',20);
hold off

xlabel('Voltage (V)')
ylabel('Current (mA)')
title(sprintf('Capacitive I-V Load Curves, Sine Signals at f = %s kHz',strrep(sprintf('%.0f,' , ff/1000)(1:end-1),',',', ')));
