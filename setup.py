from setuptools import setup
  
setup(
    name='hearing-exam',
    version='0.1.0',
    description='This python script will simulate a hearing exam, with distinct frequencies and volume',
    author='Domenico Raimondi',
    author_email='draimondi@gmail.com',
    packages=['exam'],
    install_requires=[
        'numpy',
        'pyaudio',
        'PySimpleGUI'
    ],
)