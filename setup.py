try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'LabSense',
    'description': 'LabSense is a project that retrieves different types of data about a lab.',
    'author': 'Jason Tsao',
    'url': 'https://github.com/jtsao22/LabSense',
    'download_url': 'https://github.com/jtsao22/LabSense/archive/master.zip',
    'author_email': 'jtsao22@gmail.com',
    'version': '0.1',
    'install_requires': [''],
    'packages': ['NAME'],
    'scripts': []
}

setup(**config)
