# My Digital Drone Twin
### Skeleton-Tracking for Sports using LiDAR Depth Camera
:walking:   :helicopter:   :running:

![kth logo](https://www.findaphd.com/common/institutions/logos/Institutions/PID208.gif)

# How SkeletonTrackingApp works?
Are you curious to find out how `SkeletonTrackingApp` works? (*the below video should be replaced with better one)

Watch a video [here.](https://drive.google.com/file/d/1t-GgERY4j2ppLnEbO_lELs6ntI9Gp5FQ/view?usp=sharing)
# Prep
- The project has been built with `python=3.7.9` version on `Windows 10 OS`.
- You must have `python3` and the version to be `< 3.8` due to Cubemos restrictions.
- You need an Intel RealSense camera `L515` if you intend to use the functionaly `Recording`. `D400` serie should work as well.

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
# Run the app via command
Use the below command to run the app. `-W ignore` flag ignores useless warnings which are popped up. 
`cd app`
`python -W ignore run.py`
# Run unittests
Use the command `python run_tests.py` to run the `unittests`.
