from setuptools import setup
from setuptools import find_packages

version = '0.0.0'

classifiers = """
Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
Operating System :: OS Independent
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Topic :: Software Development :: Libraries
Topic :: Utilities
""".strip().splitlines()

setup(
    name='dnsinq',
    version=version,
    description="dnsmasq config helper",
    long_description=(
        open('README.rst').read() + "\n" +
        open('CHANGES.rst').read()
    ),
    classifiers=classifiers,
    keywords='',
    author='Tommy Yu',
    author_email='y@metatoaster.com',
    url='https://github.com/metatoaster/dnsinq',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'requests',
    ],
    include_package_data=True,
    python_requires='>=3.3',
    entry_points={
        'console_scripts': [
            'dnsinq = dnsinq.cli:main',
        ]
    },
    test_suite="dnsinq.tests.make_suite",
)
