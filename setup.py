from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    """
    function to get the required files
    """
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

        return requirements

#  setup details  
setup(
    name = "dsproject",
    version = "1.0",
    author= "Pranav Dhadwal",
    author_email= "dhadwal.pranav01@gmail.com",
    install_requires=get_requirements('requirements.txt')
)