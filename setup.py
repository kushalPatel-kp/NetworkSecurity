from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    requirement_list:List[str]=[]
    try:
        with open('requirement.txt', 'r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("Not found")

    return requirement_list

setup(
    name="networksecurity",
    version="0.0.1",
    author="Kushal Patel",
    author_email="kushalpatel043@gmail.com",
    packages=find_packages(),
    install_rquires=get_requirements()
)