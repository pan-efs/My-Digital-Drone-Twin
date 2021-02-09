# My Digital Drone Twin
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

Add `.vscode` folder and create a `settings.json` file. Import the below code block:

```
{

    "python.pythonPath": "C:\\Users\\user\\miniconda3\\envs\\thesis\\python.exe",
    "python.linting.pylintArgs": ["--generate-members"],

}
```

`python.pythonPath` may not be the same. Look your directory.

# Run unittests
Use the command `coverage run -m unittest discover && coverage report -m` to run the `unittests`.
