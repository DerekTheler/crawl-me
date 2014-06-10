PROJECT_METADATA = "project.json"

import json, os
here = os.path.abspath(os.path.dirname(__file__))
proj_conf = json.loads(open(os.path.join(here, PROJECT_METADATA)).read())

from setuptools import setup, find_packages

setup(
    name = proj_conf["name"],
    version = proj_conf["version"],

    packages = find_packages(),
    install_requires = ['pyquery>=1.2.8'],

    author = proj_conf["author"],
    author_email = proj_conf["author_email"],
    url = proj_conf["url"],
    license = proj_conf["license"],

    description = proj_conf["description"],
    keywords = proj_conf["keywords"],

    entry_points = {
        'console_scripts': proj_conf["console_scripts"]
    }
)