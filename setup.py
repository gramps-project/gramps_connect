try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
import sys


svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)


with open('gramps_connect/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(name='gramps_connect',
      version=version,
      description='Gramps webapp for genealogy',
      long_description=open('README.md', 'rb').read().decode('utf-8'),
      author='Doug Blank',
      author_email='doug.blank@gmail.org',
      url="https://github.com/gramps-connect/gramps_connect",
      install_requires=['gramps>=5.0', "tornado"],
      packages=['gramps_connect', 
                'gramps_connect.handlers'],
      include_data_files = True,
      include_package_data=True,
      data_files = [("./gramps_connect/templates", 
                     [
                         "gramps_connect/templates/login.html",
                     ])],
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
      ]
)
