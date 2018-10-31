from setuptools import setup, find_packages

# Package meta-data.
NAME = 'auditexport'
DESCRIPTION = 'client for exporting virtru audit data.'
URL = 'https://github.com/virtru/audit-export-client'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '1.0.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name=NAME,
      version=VERSION,
      packages=['auditexport'],
      license='MIT',
      description='',
      long_description=readme,
      long_description_content_type='text/markdown')
