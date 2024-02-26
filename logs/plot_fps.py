import os
import json
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as mticker
import numpy as np
from scipy.signal import find_peaks

parser = argparse.ArgumentParser()
parser.add_argument('--prefix', help='Optional prefix for data file')
parser.add_argument('--container', help='From which container to parse the data')
args = parser.parse_args()

CONTAINER_ID = args.container if args.container is not None else 1

script_dir = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(script_dir, 'fps_data.txt')
gazebo_fps_file = f'../remrob-server/server/compose/local/temp/robosim-{CONTAINER_ID}/GAZEBO_FPS_out.txt'
rviz_fps_file = f'../remrob-server/server/compose/local/temp/robosim-{CONTAINER_ID}/FPS_out.txt'

fig, ax = plt.subplots()

def calculate_average_peak_value(data_file):

    with open(data_file, 'r') as f:
        fps_values = [json.loads(line)['fps'] if json.loads(line)['fps'] is not None else 0 for line in f]

    fps_values = np.array(fps_values)

    peaks, _ = find_peaks(fps_values)

    if len(peaks) == 0:
        return None, 0, 0

    largest_peak = max(peaks, key=lambda x: fps_values[x])

    threshold = 0.75 * fps_values[largest_peak]

    # Start and end of the peak
    start = np.where(fps_values[:largest_peak] < threshold)[0][-1]
    print("start:", fps_values[start])
    end = largest_peak + np.where(fps_values[largest_peak:] < threshold)[0][0]
    print("end:", fps_values[end])

    # Average of the peak
    average_peak_value = np.mean(fps_values[start:end])

    return average_peak_value, start, end

# Function to update the plot
def update(i):
    # Clear the previous plot
    ax.clear()

    ax_percentage = ax.twinx()
    # ax_gazebo = ax.twinx()

    # ax_gazebo.spines['left'].set_position(('outward', 80))
    # ax_gazebo.set_frame_on(True)
    # ax_gazebo.patch.set_visible(False)

    # Read the fps_values file
    with open(data_file, 'r') as f:
        avg_fps_values = []
        cpu_values = []
        ram_values = []
        gpu_values = []
        for line in f:
            data = json.loads(line)
            fps = data['fps']
            if fps is not None:  # Ignore null values
                avg_fps_values.append(float(fps))
            else:
                avg_fps_values.append(0)
            cpu_values.append(data['cpu_usage'])
            ram_values.append(data['ram_usage'])
            gpu_values.append(data['gpu_usage'])

    # Plot
    ax.plot(avg_fps_values, label='Framebuffer updates per second', linewidth=2, alpha=1)
    ax_percentage.plot(cpu_values, label='%CPU', color='m', linewidth=1, alpha=0.4)
    ax_percentage.plot(ram_values, label='%RAM', color='y', linewidth=1, alpha=0.4)
    ax_percentage.plot(gpu_values, label='%GPU', color='g', linewidth=1, alpha=0.4)
    # ax.plot(count_values, label='Total Framebuffer updates per second')

    # Title and labels
    ax.set_title('Framebuffer throughput', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('Framebuffer updates per second')

    ax_percentage.set_ylim(0, 100)
    ax_percentage.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:.0%}'.format(y / 100)))

    # Legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_percentage.get_legend_handles_labels()
    # ax.legend(lines, labels, loc=0)
    ax_percentage.legend(lines + lines2, labels + labels2, loc=0)

    # ax_percentage.annotate('CPU Usage', xy=(1, cpu_values[-1]), xytext=(10, 0), 
    #              xycoords=('axes fraction', 'data'), textcoords='offset points', color='gray')
    # ax_percentage.annotate('RAM Usage', xy=(1, ram_values[-1]), xytext=(10, 0), 
    #              xycoords=('axes fraction', 'data'), textcoords='offset points', color='y')
    # ax_percentage.annotate('GPU Usage', xy=(1, gpu_values[-1]), xytext=(10, 0), 
    #              xycoords=('axes fraction', 'data'), textcoords='offset points', color='g')

def load_fps_file(filename):
    with open(filename, 'r') as f:
        return [float(line.strip()) for line in f]

def get_gazebo_fps_avg():
    fps_values = load_fps_file(gazebo_fps_file)
    if len(fps_values) <= 1:
        return 0
    return sum(fps_values[1:]) / len(fps_values[1:])

def get_rviz_fps_avg():
    fps_values = load_fps_file(rviz_fps_file)
    if len(fps_values) <= 1:
        return 0
    return sum(fps_values[1:]) / len(fps_values[1:])

def get_performance_avg(start, end):
    with open(data_file, 'r') as f:
        cpu_values = []
        ram_values = []
        gpu_values = []
        for line in f:
            data = json.loads(line)
            cpu_values.append(data['cpu_usage'])
            ram_values.append(data['ram_usage'])
            gpu_values.append(data['gpu_usage'])
    return {
        'avg_cpu': np.mean(np.array(cpu_values)[start:end]),
        'avg_ram': np.mean(np.array(ram_values)[start:end]),
        'avg_gpu': np.mean(np.array(gpu_values)[start:end])
    }

average_peak_value, start, end = calculate_average_peak_value(data_file)
print(f"Average FB updates during the largest peak: {average_peak_value}")

average_gazebo_framerate = get_gazebo_fps_avg()
print(f"Average Gazebo framerate: {average_gazebo_framerate} FPS")

average_rviz_framerate = get_rviz_fps_avg()
print(f"Average RViz framerate: {average_rviz_framerate} FPS")

performance_avg = get_performance_avg(start, end)
print(f"Average CPU usage: {performance_avg['avg_cpu']}%"
      f"\nAverage RAM usage: {performance_avg['avg_ram']}%"
      f"\nAverage GPU usage: {performance_avg['avg_gpu']}%")

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
with open(os.path.join(script_dir, f'data/{args.prefix}avg_metrics_{timestamp}.json'), 'w') as f:
    f.write(json.dumps({
        'fps': average_peak_value,
        'gazebo_fps': average_gazebo_framerate,
        'rviz_fps': average_rviz_framerate,
        'cpu': performance_avg['avg_cpu'],
        'ram': performance_avg['avg_ram'],
        'gpu': performance_avg['avg_gpu']
    }))


# Create the animation
ani = animation.FuncAnimation(fig, update, interval=1000)  # Update every 1000 ms

# Show the plot
plt.show()