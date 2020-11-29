
setup(
    name='gecko.py',
    version='0.1',
    py_modules=['gecko.py'],
    install_requires=[
    'requests',
    'Click',
    'pyfiglet'
    ],
    entry_points='''
        [console_scripts]
        yourscript=gecko.py:cli
    ''',
)
