import os
import csv
from datetime import datetime
from potentiostat import Potentiostat
import matplotlib.pyplot as plt

def run_beaker_test():
    port = '/dev/tty.usbmodem1101'       # Serial port for potentiostat device
    datafile = 'data.txt'       # Output file for time, curr, volt data

    test_name = 'cyclic'        # The name of the test to run
    curr_range = '10000uA'        # The name of the current range [-100uA, +100uA]
    sample_rate = 100.0         # The number of samples/second to collect

    volt_min = -1.2             # The minimum voltage in the waveform (V)
    volt_max =  -0.4             # The maximum voltage in the waveform (V)
    #volt_per_sec = 0.050        # The rate at which to transition from volt_min to volt_max (V/s)
    volt_per_sec = 1.00         # The rate at which to transition from volt_min to volt_max (V/s)
    num_cycles = 1              # The number of cycle in the waveform

    # Convert parameters to amplitude, offset, period, phase shift for triangle waveform
    amplitude = (volt_max - volt_min)/2.0            # Waveform peak amplitude (V) 
    offset = (volt_max + volt_min)/2.0               # Waveform offset (V) 
    period_ms = int(1000*4*amplitude/volt_per_sec)   # Waveform period in (ms)
    shift = 0.5                                      # Waveform phase shift - expressed as [0,1] number
                                                     # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.

    # Create dictionary of waveform parameters for cyclic voltammetry test
    test_param = {
            'quietValue' : 0.0,
            'quietTime'  : 0,
            'amplitude'  : amplitude,
            'offset'     : offset,
            'period'     : period_ms,
            'numCycles'  : num_cycles,
            'shift'      : shift,
            }

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(os.path.dirname(__file__), "../../output")
    os.makedirs(output_dir, exist_ok=True)

    data_filename = os.path.join(output_dir, f"cv_data_{timestamp}.txt")
    plot1_filename = os.path.join(output_dir, f"cv_time_plot_{timestamp}.png")
    plot2_filename = os.path.join(output_dir, f"cv_iv_plot_{timestamp}.png")

    # Create potentiostat object and set current range, sample rate and test parameters
    dev = Potentiostat(port)     
    dev.set_curr_range(curr_range)   
    dev.set_sample_rate(sample_rate)
    dev.set_param(test_name,test_param)

    # Run cyclic voltammetry test
    t, volt, curr = dev.run_test(test_name, display='data', filename=None)

    # Save data to file
    with open(data_filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Time (s)', 'Voltage (V)', 'Current (uA)'])
        writer.writerows(zip(t, volt, curr))

    # plot results using matplotlib
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t,volt)
    plt.ylabel('potential (V)')
    plt.grid('on')
    plt.subplot(212)
    plt.plot(t,curr)
    plt.ylabel('current (uA)')
    plt.xlabel('time (sec)')
    plt.grid('on')
    plt.tight_layout()
    plt.savefig(plot1_filename)  # after first plot block

    plt.figure(2)
    plt.plot(volt,curr)
    plt.xlabel('potential (V)')
    plt.ylabel('current (uA)')
    plt.grid('on')
    plt.tight_layout()
    plt.savefig(plot2_filename)  # after second plot block


    print(f"Saved data to: {data_filename}")
    print(f"Saved plot (time) to: {plot1_filename}")
    print(f"Saved plot (IV) to: {plot2_filename}")