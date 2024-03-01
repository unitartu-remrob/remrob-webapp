# Running tests

Video illustration of a performance test run: https://www.youtube.com/watch?v=ScvikH2_Jkg 

The performance test scripts are on `performance-metrics` branch in [remrob-docker repository](https://github.com/unitartu-remrob/remrob-docker). The Dockerfile includes custom-built Gazebo and Rviz that have been modified to extract FPS measures from the simulations. The extracted data is saved in `$HOME/.ros`.

The modified template generation scripts are in `remrob-server` repository `performance-metrics` branch. The image name in the template should be the same as the one built from the `performance-metrics` branch. The FPS data files are mapped to the host from `$HOME/.ros` directory in the containers.

The automated Gazebo image test does the following:
1) Starts a Gazebo simulation with a [Robotont robot in a maze](https://github.com/robotont/robotont_gazebo)
2) Runs a teleop node in a new window
3) Spins the robot to simulate graphical load for 15 seconds
4) Closes the Gazebo window


The automated RViz image test does the following:
1) Starts an RViz with a ["fake" Robotont robot](https://github.com/robotont/robotont_driver?tab=readme-ov-file#fake-driver)
2) Runs a teleop node in a new window
3) Spins the robot to simulate graphical load for 15 seconds
4) Closes the RViz window

The data is sent by the client automatically every second to the /fps endpoint of the flask application. The fps collected is a 100n window moving average. The data is in the format:
```json
{
	"fps": 0,
	"source": "{container_id}",
}
```

At every snapshot of this fps, the server records the corresponding CPU, GPU, RAM, and application (Gazebo | RViz) FPS metrics to logs/fps_data.txt

To calculate the average FPS from the logged data, run the following command:

```bash
npm run metrics -- --prefix {output_file_prefix} --container {container_id}
```

The average is calculated from the 0.75p peak of the framebuffer update rate.

Clear the log:
```bash
npm run clear-log
```

Change the appropriate output file prefix and container ID in the script as necessary.

The json data can be transformed to CSV with `dump_data_to_csv.py`.


