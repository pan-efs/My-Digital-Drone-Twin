from setuptools import setup

setup(
    name="my_digital_drone_twin",
    version="0.0.1",
    description="3D Human pose estimation and extract biomechanics info using a depth camera attached on drone",
    url="https://github.com/pan-efs/My-Digital-Drone-Twin",
    author="Panagiotis Efstratiou",
    author_email="",
    license="Creative Commons Zero v1.0 Universal",
    packages=[
        "biomechanics",
        "cubemos_converter",
        "filters",
        "cubemos",
        "networking",
        "stats",
        "animations",
        "configs",      
    ],
    install_requires=[
        "pandas", 
        "numpy",
        "matplotlib",
        "pyrealsense2",
        "filterpy",],
    zip_safe=False,
)
