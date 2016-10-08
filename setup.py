from setuptools import setup, find_packages
import glob
import subprocess
import os


# Build the JS so vcs.js is ready for packaging
os.chdir("js")
subprocess.check_call("npm run build", shell=True)
os.chdir("..")


setup(
    name="vcs_live",
    version="0.1",
    packages=find_packages(),
    scripts=glob.glob("scripts/*"),
    package_data={"vcs_live": ["js/vcs.js", "html/sample.html"]}
)
