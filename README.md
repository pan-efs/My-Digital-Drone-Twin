# My Digital Drone Twin
### Skeleton-Tracking for Sports using LiDAR Depth Camera
:walking:   :helicopter:   :running:

![kth logo](https://www.findaphd.com/common/institutions/logos/Institutions/PID208.gif)

# Prep
The project is mainly built with `python=3.7` version on Windows 10 OS.

# Miniconda installation
To install `miniconda` you can follow [the instructions of official website](https://docs.conda.io/en/latest/miniconda.html).

# Conda environment
You need to create a new `conda` environment with all the essential `python` packages installed. You can create this environment from the provided `environment.yml` file in this repository in the following way:
- `conda env create -f environment.yml`

# Cubemos
You can follow the install instructions related to `Cubemos Skeleton Tracking` from [getting started guide](https://download-skeleton-tracking-sdk.s3.eu-central-1.amazonaws.com/GettingStartedGuide.pdf) or [realsense installation guide](https://dev.intelrealsense.com/docs/skeleton-tracking-sdk-installation-guide).

# VS Code
`VS Code` is recommended but it's not necessary.

Add `.vscode` folder and create a `settings.json` file. Import the below code block, modify `user` accordingly.

```
{

    "python.pythonPath": "C:\\Users\\<user name>\\miniconda3\\envs\\thesis\\python.exe",
    "python.linting.pylintArgs": ["--generate-members"],

}
```

`python.pythonPath` may not be the same. Look your directory.

# Configurations
From your local project's path:

`cd app`

`python configuration.py --a <main path> --b <realsense_viewer path> --c <offline_analysis path>`

- Parser is not required. That means that you can define your paths manually from [here](https://github.com/pan-efs/My-Digital-Drone-Twin/blob/main/app/configuration.py).
- Main path is your local project's path.
- RealSense Viewer is your local path of Intel's viewer app.
- Offline analysis path is the .bag file that you want to be converted.

### Run converter after 'configuration' step
From your local project's path:

`cd cubemos_converter`

`python convert_bagfile_skel.py`
# Run biomechanical analysis examples
### Run cadence
From your local project's path:

`cd datatypes`

`python cadence_example.py --path <text file>`

#### Plotting
![cadence plot](/samples/imgs/cadence.png)

### Run hammer throw
From your local project's path:

`cd datatypes`

`python hammer_example.py --path <text file>`

- Try to parse your text path using `\\` instead of `\`. 
- Turning phase should be defined manually. Otherwise, delete the range limit from lists, e.g. line 102 in `hammer_example.py`.
- If you do not have a text file, you can choose one among `<project path>\\samples\\data` or from [here](https://github.com/pan-efs/My-Digital-Drone-Twin/tree/main/samples/data).

#### Plotting
![hammer throw plot](/samples/imgs/error_bar_hammer_fast.png)
# Run unittests
Use the command `coverage run -m unittest discover && coverage report -m` to run the `unittests`.
