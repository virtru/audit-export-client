from setuptools import setup, find_packages

# Package meta-data.
NAME = 'auditexport'
DESCRIPTION = 'client for exporting virtru audit data.'
URL = 'https://github.com/virtru/audit-export-client'
REQUIRES_PYTHON = '>=3.5.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('VERSION') as version_file:
    version = version_file.read()

setup(name=NAME,
      version=version,
      packages=['auditexport'],
      license='MIT',
      description='',
      long_description=readme,
      long_description_content_type='text/markdown')
