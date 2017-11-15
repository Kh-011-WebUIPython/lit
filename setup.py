import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


NAME = 'LIT'
DESCRIPTION = ''
URL = 'https://github.com/Kh-011-WebUIPython/lit/'
EMAIL = 'maxkrivich@gmail.com'
AUTHOR = 'Maxim Krivich'


with codecs.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name=NAME,
    version='',
    packages=find_packages(),
    url=URL,
    license='MIT',
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    install_requires=REQUIREMENTS,
    # entry_points={
    #     'console_scripts': [],
    # },
)
