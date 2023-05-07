import psutil
import matplotlib.pyplot as plt

# set up the data
xdata, ydata = [], []

# record CPU usage for 10 seconds
for i in range(1000):
    # get the CPU usage
    cpu_percent = psutil.cpu_percent(interval=0.01)

    # append data
    xdata.append(i*0.01)
    ydata.append(cpu_percent)

# create the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_ylabel('CPU Usage (%)')
ax.set_ylim(0, 100)
ax.plot(xdata, ydata, color='b')

# show the plot
plt.savefig("cpu.png")
