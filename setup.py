from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()
with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

setup(name='virtru-audit-client',
      version='1.0.0',
      packages=['virtru-audit-client'],
      description='client for exporting virtru audit data',
      long_description=readme)
