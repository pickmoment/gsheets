from setuptools import setup, find_packages
 
setup(
    name='gsheets',
    version='0.1.0',
    url='https://github.com/pickmoment/gsheets',
    license='MIT',
    author='pickmoment', 
    author_email='pickmoment@gmail.com',
    description='Google Sheets API',
    packages=find_packages(),
    long_description=open('README.md').read(),
    zip_safe=False,
    setup_requires=[
        'google-api-python-client>=1.7.11',
        'google-auth-httplib2>=0.0.3',
        'google-auth-oauthlib>=0.4.1'
    ]
)