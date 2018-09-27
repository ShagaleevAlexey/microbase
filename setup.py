from setuptools import setup, find_packages

setup(
    name='microbase',
    version='0.1.7',
    packages=find_packages(),
    url='https://github.com/ShagaleevAlexey/microbase',
    license='',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='This is microbase for microservices',
    install_requires=[
        'sanic==0.7.0',
        'sanic-envconfig==1.0.1',
        'python-rapidjson==0.6.3',
        'structlog==18.1.0'
    ]
)
