from setuptools import setup

setup(
    name="human_pose_estimation",
    version="0.0.1",
    description="3D Human pose estimation and extract biomechanics info",
    url="",
    author="Panagiotis Efstratiou",
    author_email="pefstrat@gmail.com",
    license="Creative Commons Zero v1.0 Universal",
    packages=[
        "pose_estimation/convert-bagfile-skel",
        "biomechanics/biomechanics2D",
        "biomechanics/biomechanics3D",
    ],
    install_requires=["pandas", "numpy", "math",],
    zip_safe=False,
)
