# imports - standard imports
import os, shutil
from distutils.command.clean import clean as Clean

from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
import re, ast

# get version from __version__ variable in frappe/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('frappe/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")

class CleanCommand(Clean):
    def run(self):
        Clean.run(self)

        basedir = os.path.abspath(os.path.dirname(__file__))

        for relpath in ['build', '.cache', '.coverage', 'dist', 'frappe.egg-info']:
            abspath = os.path.join(basedir, relpath)
            if os.path.exists(abspath):
                if os.path.isfile(abspath):
                    os.remove(abspath)
                else:
                    shutil.rmtree(abspath)

        for dirpath, dirnames, filenames in os.walk(basedir):
            for filename in filenames:
                _, extension = os.path.splitext(filename)
                if extension in ['.pyc']:
                    abspath = os.path.join(dirpath, filename)
                    os.remove(abspath)
            for dirname in dirnames:
                if dirname in ['__pycache__']:
                    abspath = os.path.join(dirpath,  dirname)
                    shutil.rmtree(abspath)

setup(
	name='frappe',
	version=version,
	description='Metadata driven, full-stack web framework',
	author='Frappe Technologies',
	author_email='info@frappe.io',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link],
	cmdclass = \
	{
		'clean': CleanCommand
	}
)
