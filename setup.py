from setuptools import setup, find_packages

setup(
    name='GetTissue',
    version='0.1dev',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),

    packages=find_packages(exclude=['os', 're', 'time']),
    install_requires=[
        "numpy", 
        "gensim", 
        "flask", 
        "flask-restful",
        "scipy"
    ],
)