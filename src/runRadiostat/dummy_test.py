import matplotlib.pyplot as plt
from potentiostat import Potentiostat

def run_dummy_test():
    # Adjust this if your device shows up under a different port
    port = '/dev/tty.usbmodem1101'
    pot = Potentiostat(port)

    # Define the built-in test type (linear sweep)
    test_name = 'linearSweep'

    # Set the parameters for the linear sweep
    pot.set_param(test_name, {
        'Vstart': -1.0,
        'Vstop': 1.0,
        'Scanrate': 0.05,
        'SampleRate': 100,
        'NumScans': 1
    })

    pot.set_curr_range('100uA')  # Adjust if necessary

    print("Running dummy test...")
    data = pot.run_test(test_name, display='pbar')

    # Extract columns from data
    time_vals = [row[0] for row in data]
    curr_vals = [row[1] for row in data]
    volt_vals = [row[2] for row in data]

    # Plot current vs voltage
    plt.plot(volt_vals, curr_vals)
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title('Dummy Cell Linear Sweep')
    plt.grid(True)
    plt.tight_layout()
    plt.show()