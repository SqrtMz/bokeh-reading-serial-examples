import serial
import serial.tools.list_ports
import time

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource

# Load data
# data = pd.read_csv('test/datasets/scopegen_data3.csv')
# x = np.array(data[data.columns[0]])
# y = np.array(data[data.columns[1]])

# Bokeh setup
source = ColumnDataSource(data=dict(x=[], y1=[]))
p = figure(title="Signal", height=400, width=800,
            x_axis_label='Time (s)', y_axis_label='Amplitude',
            y_range=(0, 200))
p.line('x', 'y1', source=source, line_color='red')


# State variable for current frame
i = {'index': 0}

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for port in ports:
    portList.append(str(port))
    print(port)

val = input('Select port: ')

for j in range(len(portList)):
    if portList[j].startswith("/dev/ttyUSB" + str(val)):
        portSelected = ("/dev/ttyUSB" + str(val))
        print('Port selected: ' + str(port))
        break

serialInst.baudrate = 115200
serialInst.port = portSelected
serialInst.open()
global time_step
time_step = 0
global time_passed
time_passed = []

def update():
    global time_step, time_passed
    if serialInst.in_waiting > 0:
        serialRecieving = serialInst.readline()
        print(serialRecieving.decode('utf-8').rstrip('\n'))
        time_passed.append(time_step)
        time.sleep(0.01)
        time_step += 0.01

        # Process the received data
        # Assuming the data is in the format "x,y"
        
        try:
            data_serial = serialRecieving.decode('utf-8').rstrip('\n').split(',')
            y1_data = float(data_serial[0])
            y2_data = float(data_serial[1])
        except:
            y1_data = 0
            y2_data = 0
            print("Error in data conversion")


    new_data = dict(x=[time_step], y1=[y2_data])
    source.stream(new_data)
    i['index'] += 1
    

# Register plot and animation callback
curdoc().add_root(p)
curdoc().add_periodic_callback(update, 10)  # milliseconds