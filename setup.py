from setuptools import setup, find_packages

# Package meta-data.
NAME = 'virtruaudit'
DESCRIPTION = 'client for exporting virtru audit data.'
URL = 'https://github.com/virtru/audit-export-client'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = 'v1.0.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name=NAME,
      version=VERSION,
      package_dir={'': 'src'},
      packages=find_packages('src', exclude='test'),
      license='MIT',
      description='',
      long_description=readme,
      long_description_content_type='text/markdown')
