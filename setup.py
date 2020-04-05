from setuptools import find_packages, setup


setup(
    name='tilekiln',
    version='0.0.2',
    author="Paul Norman",
    author_email="osm@paulnorman.ca",
    url="https://github.com/pnorman/tilekiln",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Click',
        'fs',
        'pyyaml',
        'jinja2',
        'psycopg2'
    ],
    entry_points={
        'console_scripts': ['tilekiln-generate=tilekiln.scripts.generate:cli',
                            'tilekiln-tilejson=tilekiln.scripts.tilejson:cli']
    },
    setup_requires=[
        'pytest-runner',
        'flake8'
    ],
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    python_requires="~=3.6"
)
