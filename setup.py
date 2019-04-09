from setuptools import setup

setup(
    name='postman2apiary',
    version='0.1.0',
    packages=['pmc2.0', 'pmc2.0.test', 'pmc2.1', 'pmc2.1.test'],
    url='https://github.com/jeffwhite-619/postman2apiary',
    license='LICENSE',
    author='Jeff White',
    author_email='thisguy@thejeffwhite.com',
    description='A fork of p8ul/postman2apiary, expanded to include support for Postman Collection version 2.1',
    long_description=open('README.txt').read()
)