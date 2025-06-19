import serial
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.driving import count

cereal = serial.Serial(input("Enter the port: "), 115200)
cereal.close()

@count()
def update(x):

	cereal.open()
	leche = cereal.readline(10)
	leche = leche.decode("utf-8").strip()
	cereal.close()

	source.stream({'x': [x], 'y': [leche]}, rollover=100)

	print(f"mcu value: {leche}")


source = ColumnDataSource({'x': [], 'y': []})

p = figure(y_range=(-300, 4500), width=1280, height=720)

p.scatter(source=source)
p.line(source=source, color="red")

doc = curdoc()
doc.add_root(p)
doc.add_periodic_callback(update, 1)