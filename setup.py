import os
from typing import List
from dotenv import load_dotenv, find_dotenv
from setuptools import find_packages, setup

load_dotenv(find_dotenv())

HYPEN_E_DOT = '-e .'
AUTHOR = os.environ.get('AUTHOR')
AUTHOR_EMAIL = os.environ.get('AUTHOR_EMAIL')

def get_requirements(file_path: str) -> List[str]:
    '''
    This function retrieves the requirements from a file and returns them as a list.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name='component_scrapers',
    version='0.0.1',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
