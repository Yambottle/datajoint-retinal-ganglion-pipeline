import os
from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py as build_py_orig

package_name = r"rg_pipeline"
here = os.path.dirname(os.path.abspath(__file__))

# requirements.txt -> install_requires
req_path = os.path.join(here , "requirements.txt")
if os.path.exists(req_path):
    with open('requirements.txt') as f:
        install_requires = f.read().strip().split('\n')
else:
    install_requires = []

# package list
packages = find_packages(where='.', exclude=(), include=('*',))

setup(
    name=package_name,
    version="1.0",
    description='Datajoint schemas for retinal ganglion experiments',
    author='Drew Yang',
    author_email='drew.yang.dev@gmail.com',
    zip_safe = False,
    packages=packages,
    scripts=[f'bin/{package_name}'],
    # could cause dependency conflict while integrating with other modules in the same env
    install_requires=install_requires, 
    # # ENABLE package_data
    # include_package_data=True,
    # # ('PACKAGE_NAME', 'DIR_WITHIN_PACKAGE')
    # package_data = {
    #     'pipeline':['/pipeline/data/*', '/pipeline/data_source_manifest.json', '/pipeline/config.ini'],
    #     'visualization':['/visualization/config.ini'] 
    # }
 )