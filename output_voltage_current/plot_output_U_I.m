x   = load("volt_current_out.txt");
Upk = 208*1.414*2; % measurement was done with 208 Vrms at ONE tube/anode; convert to peak voltage for symmetric output from two tubes working in opposite polarity
f   = x(:,1); % frequency (Hz) 
Ipk = x(:,2)/1000*1.414; % convert RMS voltage drop across 1kOhm resistor to peak current

% convert to assumed 500 Vpk output voltage:
Ipk = 500/Upk * Ipk;
Upk = 500/Upk * Upk;

% modelled current through capacitor:
C = 100e-12; % 100 pF
ff   = logspace(1,5,5);
IIpk = Upk .* (2*pi*ff*C);

% plot stuff:
loglog(f,1000*Ipk,'r.','markersize',15 , ff,1000*IIpk,'b-','linewidth',2)
axis([30 100000, 1e-2,1e2])
xlabel('Frequency (Hz)')
ylabel('Peak current (mA)')
title('Estat Headphone Current at 500 Vpk')
legend('Measured', sprintf('%g pF load',C*1e12),'location','northwest')
