from setuptools import setup

setup(
    name="my_digital_drone_twin",
    version="0.0.1",
    description="Skeletal tracking for sports using LiDAR depth camera. Desktop App version.",
    url="https://github.com/pan-efs/My-Digital-Drone-Twin",
    author="Panagiotis Efstratiou",
    author_email="",
    license="Creative Commons Zero v1.0 Universal",
    packages=[
        "biomechanics",
        "cubemos_converter",
        "filters",
        "cubemos",
        "exceptions",
        "datatypes",
        "app",      
    ],
    install_requires=[
        "pandas", 
        "numpy",
        "pyqt5",
        "pyrealsense2",
        "filterpy",],
    zip_safe=False,
)
