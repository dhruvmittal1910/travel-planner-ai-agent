# using this file I willl be installing all the required packages in my current virtual env


from setuptools import setup,find_packages
from typing import List


def get_requirements()->List[str]:
    requirements_list:List[str]=[]
    
    try:
        # open the requiremnts.txt file and read
        with open("requirements.txt","r") as file:
            lines=file.readlines()
            for line in lines:
                req=line.strip()
                if req and req!='-e .':
                    requirements_list.append(req)
    except Exception as e:
        print("--- File not found --- \n",e)
    
    return requirements_list

print(get_requirements())

setup(
    name="AI_TRIP_PLANNER",
    version="0.0.1",
    author="Dhruv Mittal",
    author_email="dhruvmittal1910@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)