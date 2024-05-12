from setuptools import setup, find_packages

setup(
    name="ttsvid",
    version="1.0",
    packages=["ttsvid"],
    scripts=["scripts/ttsvid"],
    install_requires=[
        "numpy",
        "scipy",
        "argparse",
        "TTS"
    ],
    package_data={
        '' : ['presenter.mp3'],
    },
    include_package_data=True,    
)
