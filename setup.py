from setuptools import setup, find_packages

setup(
    name='banking',
    version='0.1',
    py_modules=['banking'],
    long_description=open('README.md').read(),
    entry_points='''
        [console_scripts]
        banking=banking.__main__:cli
    '''
)
