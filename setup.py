from setuptools import setup, find_packages
from os import path

# Read the contents of the README file
cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sciengdox',
      version='0.7.0',
      description='Science/engineering dynamic doc generation',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='science engineering documentation scipy pandoc',
      url='http://github.com/gbingersoll/sciengdox',
      author='Greg Ingersoll',
      author_email='greg.ingersoll@convolutionresearch.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'beautifulsoup4',
          'colorama',
          'numpy',
          'panflute',
          'pint',
          'pysvglib',
          'scipy'
      ],
      extras_require={
          'dev': ['pytest', 'pyyaml', 'pycodestyle', 'mock',
                  'pytest_mock', 'setuptools', 'wheel', 'twine'],
          'examples': ['kaleido', 'matplotlib', 'plotly']
      },
      entry_points={
          'console_scripts': [
              'compiledoc=sciengdox.compiledoc:main',
              'pandoc-pythonexec=sciengdox.pandoc_pythonexec.filter:main']
      },
      include_package_data=True,
      zip_safe=False)
