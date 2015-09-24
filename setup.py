from setuptools import setup, find_packages

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='pike',
    version='0.0.3',
    description=('Lightweight plugin management system for Python'),
    long_description=desc,
    url='https://github.com/pyarmory/pike',
    author='John Vrbanac',
    author_email='john.vrbanac@linux.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='plugin management modules',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=['six'],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [],
    },
)
