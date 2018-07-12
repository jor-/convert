# Copyright (C) 2018 Joscha Reimer jor@informatik.uni-kiel.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""A setuptools based setup module.
https://packaging.python.org/en/latest/distributing.html
"""

import setuptools
import os.path

import versioneer_extended

# get the long description from the README file
readme_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst')
with open(readme_file, mode='r', encoding='utf-8') as f:
    long_description = f.read()

# setup
setuptools.setup(
    # general informations
    name='convert',
    description='This library allows to convert files into other formats.',
    long_description=long_description,
    keywords='file format numpy scipy',

    url='https://github.com/jor-/convert',
    author='Joscha Reimer',
    author_email='jor@informatik.uni-kiel.de',
    license='AGPLv3+',

    classifiers=[
        # Development Status
        'Development Status :: 3 - Alpha',
        # Intended Audience, Topic
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Filesystems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        # Licence (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        # Supported Python versions
        'Programming Language :: Python',
    ],

    # version
    version=versioneer_extended.get_version(),
    cmdclass=versioneer_extended.get_cmdclass(),

    # packages to install
    packages=setuptools.find_packages(),

    # dependencies
    setup_requires=[
        'setuptools>=0.8',
        'pip>=1.4',
    ],
    install_requires=[
    ],
    extras_require={
        'numpy': ['numpy>=1.7'],
        'scipy': ['scipy>=0.10'],
    },
    # scripts
    entry_points={
        'console_scripts': [
            'convert_numpy = convert.numpy:_main',
        ],
    }
)
