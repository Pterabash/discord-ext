import setuptools

setuptools.setup(
        name='Dscord',
        version='1.1.17',
        author='thisgary',
        author_email='gary.github@gmail.com',
        description='Discord API wrapper\'s wrapper.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT Lisence',
            'Operating System :: OS Independent',
        ],
        license='MIT',
        python_requires='>=3.7',
        install_requires=['discord.py', 'flask'],
        setup_requires=['pytest_runner'],
        tests_require=['pytest'],
        test_suite='tests',
)

