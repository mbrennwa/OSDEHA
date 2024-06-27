
% B+ voltage (VDC)
U0 = 440;

% Safety resistor value (Ohm):
Rs = 5100;


% body resistance (in kOhm) as a function of voltage (VAC) (https://de.wikipedia.org/wiki/K%C3%B6rperwiderstand
Rb = [
	25 	67.3
	50 	44.9
	75 	24.8
	100 	10.9
	125 	8
	150 	5.2
	175 	4.3
	200 	3.8
];
Rb(:,2) = Rb(:,2)*1000; % convert to Ohm
p=polyfit(Rb(:,1),1./Rb(:,2),1); Rb=1/polyval(p,U0); % extrapolate to U0

% min body resistance found from Googling (Ohm):
Rb_min = 100;

% max body resistance found from Googling (Ohm):
Rb_max = 1E6;

% Voltage divider between Rs and body resistance:
Ux = Rb / (Rb+Rs) * U0;
Ux_max = Rb_max / (Rb_max+Rs) * U0;
Ux_min = Rb_min / (Rb_min+Rs) * U0;
Ix = (U0-Ux)/Rs;
Ix_min = (U0-Ux_max)/Rs;
Ix_max = (U0-Ux_min)/Rs;

