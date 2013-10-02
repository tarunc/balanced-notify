from setuptools import Command, setup

setup(
    name='balanced-notify',
    version='0.0.1',
    url='http://github.com/tarunc/balanced-notify/',
    license='MIT',
    author='Tarun',
    author_email='tarunc92@gmail.com',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'simplejson>=3.3',
        'Flask_Restless>=0.12',
        'Flask_SQLAlchemy>=1.0'
    ]
)