import setuptools
import os

README = open("README.md").read()

setuptools.setup(
  name = 'kogama.py',
  packages = ['kogama'],
  version = '0.1.4',
  license='MIT',
  description = 'An API wrapper for the online game KoGaMa written in Python',
  long_description = README,
  long_description_content_type="text/markdown",
  author = 'Ars3ne',
  author_email = 'ars3ne@protonmail.com',
  url = 'https://github.com/ars3ne/kogama.py',
  keywords = ['kogama', 'api'],
  python_requires=">=3.5.3",
  install_requires=[
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)