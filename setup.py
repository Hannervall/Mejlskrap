from setuptools import setup, find_packages

setup(
    name='mejlskrap',
    version='1.0.0',
    description='Skrapar mailadresser från angiven domän. Dessa med samma ändelse som är samma som domännamnet.',
    author='Alexander Hannervall',
    author_email='alexander@hannervall.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scrapy',
        'colorama',
        'pyfiglet'
    ],
    entry_points={
        'console_scripts': [
            'mejlskrap = mejlskrap.__main__:main'
        ]
    },
)