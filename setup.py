import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyncentral',
    version="0.0.0.2",
    license='GPL-3.0 License',
    author='Renier Moorcroft',
    author_email='RenierM26@users.github.com',
    description='Python api to access Solarwinds NCentral SOAP API',
    long_description="This package allows access to Solarwinds NCentral API. Please view readme on github",
    url='https://github.com/RenierM26/pyncentral',
    packages=setuptools.find_packages(),
    setup_requires=[
        'requests',
        'setuptools'
    ],
    install_requires=[
        'zeep',
        'pandas'
    ],
    entry_points={
    'console_scripts': ['pyncentral = pyncentral.__main__:main']
    },
    python_requires = '>=3.6'
)
