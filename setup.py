# coding=utf-8
from setuptools import setup, find_packages


exclude = ['sentinelladocker']

install_requires = ['trollius==2.0', 'docker']

setup(
    name='sentinella-docker',
    description='Some description',
    version='0.1',
    packages=find_packages(exclude=exclude),
    zip_safe=False,
    namespace_packages=['sentinella'],
    install_requires=install_requires,
    author='Julio Acuña',
    author_email='urkonn@gmail.com',
    url='https://github.com/urkonn/sentinella-docker',
    license='ASF',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Monitoring',
    ],
    keywords='monitoring Docker Containers',
)
