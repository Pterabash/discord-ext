from setuptools import find_packages, setup

setup(
        name='Descord',
        packages=find_packages(include=['descord', 'descord.ext']),
        version='1.0'
        description='Discord.py related library.',
        author='thisgary',
        license='MIT',
        install_requires=['discord.py'],
        setup_requires=['pytest_runner'],
        test_require=['pytest'],
        test_suite='tests',)

