from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name='virtru-audit-client',
      version='1.0.0',
      packages=['virtru-audit-client'],
      description='client for exporting virtru audit data',
      long_description=readme,
      long_description_content_type='text/markdown')
