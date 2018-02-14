"""A setuptools based setup module.
Based on the setup.py template at https://github.com/pypa/sampleproject

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
import os.path as op

here = op.abspath(op.dirname(__file__))

# Get the long description from the README file
with open(op.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='lovelyrita',  # Required
    version='0.1',  # Required
    description='Understanding parking enforcement data',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/openoakland/lovely-rita',  # Optional
    author='OpenOakland',  # Optional
    author_email='',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # keywords='sample setuptools development',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # install_requires=[''],  # Optional
    # package_data={},
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'lovelyrita = lovelyrita.__main__:main',
        ],
    },
)
