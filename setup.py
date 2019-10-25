from setuptools import setup

setup(name='sciengdox',
      version='0.1',
      description='Science/engineering dynamic doc generation',
      long_description='Science and engineering dynamic documentation '
                       'pandoc filter and helpers',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='science engineering documentation scipy pandoc',
      url='http://github.com/gbingersoll/sciengdox',
      author='Greg Ingersoll',
      author_email='greg.ingersoll@convolutionresearch.com',
      license='MIT',
      packages=['sciengdox'],
      install_requires=[
          'markdown',
          'panflute',
          'pexpect'
      ],
      extras_require={
          'tests': ['pytest', 'pyyaml', 'pep8'],
          'examples': ['scipy', 'matplotlib']
      },
      entry_points={
          'console_scripts': [
              'pandoc-pythonexec=sciengdox.pandoc_pythonexec.filter:main']
      },
      include_package_data=True,
      zip_safe=False)
