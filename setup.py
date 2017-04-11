from setuptools import setup

setup(
    name='App',
    packages=['App'],
    include_package_data=True,
    install_requires=[
        'flask', 'flask-session', 'flask-mysqldb',
    ],
)
