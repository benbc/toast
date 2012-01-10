from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    ]

setup(name='toast',
      version='0.0',
      description='toast',
      long_description='toast',
      classifiers=[],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="toast",
      entry_points = """\
      [paste.app_factory]
      main = toast:main
      """,
      )
