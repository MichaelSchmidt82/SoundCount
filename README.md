<center><img src="https://i.imgur.com/iLqILvT.png" height=100 width=100></img></center>

# Measuring-Speech
MTSU Software Engineering CSCI-4700/5700 project with <a href="http://research.vuse.vanderbilt.edu/rasl/pase-cane-homepage/">Vanderbilt</a>

### Main goals
sound-count attempts to answer:

1.  Measure how many words are in an audio stream/file.
2.  Description of speaker - Adult or child, male or female.
3.  Content of the sentence. Is it a sentence, is it a question?
4.  Part of speech information.

### Other goals
1.  Quantify when and whether a child likes or dislikes aspects.

### Limitations
1.  Windows is not supported, install Ubuntu in VirtualBox instead.

# Installing dependences
### Install the Python package manager PIP

  - Prerequisite:  [Python 3.6.8](https://www.python.org/downloads/release/python-368/)

__Note: Some systems use Python 2.7 as the default python interpreter.__ Be sure to check which python you're using with ```python --version``` if you are unsure of your system's default python interpreter.

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

then install the python package manager pip using
```bash
python<3> get-pip.py
```
You more than likely need to use ```python3```.  Alternatively, ```sudo easy_install pip```, may also work.

`pip` might be available via brew for macOS via ```brew install pip3```.  ```sudo apt install python3-pip``` should work in most Debian/apt-based linux distributions systems.  You may also use ```pip<3> --version``` to display which pip is in use.

### Install virutalenv

install virtualenv using pip:  

```bash
pip<3> install virtualenv
```

### Virtualenv

Virtualenv is used to create and manage environments for different python projects.  A virtualenv is **strongly** recommended.  Use virtualenv to create a virtual environment by using:

```bash
virtualenv env --python=$(which python3.6)
```

__NOTE:__ If you are in a virtual environment do not use ```sudo```, as this will install outside the virtual environment. In a virtual environment, the packages are installed in (this case) to the folder ```env```

### Switching environments
Use ```source env/bin/activate``` to load your environment.  ```env``` is a placeholder for your environment name.  

Use ```deactivate``` to exit out of your environment.  

To verify which environment you're in, use ```which pip```.  if you see that the pip location is in your environment folder (env), then you are in your virtual environment.  Also notice that in virtualenv, python3 is now the default interpreter which makes life much easier.  Check using ```python --version``` and notice the __lack__ of 3 at the end.

### Additional Requirements:

`swig` is a dependance for some python packages.  Use

```bash
apt install swig
```

or

```bash
brew install swig
```

Then install python packages by:  
```bash
pip<3> install -r requirements.txt
```  

Be sure to download the NLTK dataset: use `python<3> to bring up an interpreter:  
```python
>>> import nltk; nltk.download()
```

### Misc.
  - Recommended: [Postman](https://www.getpostman.com/)
