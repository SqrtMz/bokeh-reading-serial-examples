import serial.tools.list_ports
from bokeh.models import ColumnDataSource, Button
from bokeh.plotting import figure, curdoc
from bokeh.driving import count
from bokeh.layouts import column


ports = serial.tools.list_ports.comports()
portList = []

for port in ports:
    portList.append(str(port))
    print(str(port))

val = input("Select port:")
#val = input("Select port: COM") -wintard
#val = "COM" + str(val)
print("You selected: ", val) 
# print("You selected: COM", val) - wintard

data = serial.Serial()
data.baudrate = 115200
data.port = val
data.close()

@count()
def update(x):
    data.open()
    packet = data.readline()
    packet = packet.decode('utf-8').rstrip()
    data.close()

    values = packet.split(",")
    signal1= float(values[0])
    signal2= float(values[1])


    source1.stream({'x': [x], 'y': [signal1]}, rollover=10000)
    source2.stream({'x': [x], 'y': [signal2]}, rollover=10000)
    print(f"Voltage1: {signal1}", f"Voltage2: {signal2}")
    

source1 = ColumnDataSource({ 'x': [], 'y': []})
source2 = ColumnDataSource({ 'x': [], 'y': []})

p = figure(y_range=(-500,4500), width=1280, height=750, title="Serial Data", x_axis_label='Time',
           y_axis_label='Voltage')
p.scatter(source=source1, size=5, color="navy", alpha=0.5)
p.scatter(source=source2, size=5, color="darkgreen", alpha=0.5)
p.xaxis.fixed_location = 0 
p.yaxis.fixed_location = 0

doc = curdoc()
callback = doc.add_periodic_callback(update, 10)

button = Button(label="Stop", button_type="success")
def stop():
    if callback.is_running():
        callback.stop()
        button.label = "Start"
    else:
        callback.start()
        button.label = "Stop"

button.on_click(stop)

doc.add_root(column(button, p))