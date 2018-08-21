from setuptools import setup, find_packages

setup(
    name='microbase',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/ShagaleevAlexey/microbase',
    license='',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='This is microbase for microservices',
    install_requires=[
        'sanic',
        'sanic-envconfig',
        'python-rapidjson',
        'structlog'
    ]
)
