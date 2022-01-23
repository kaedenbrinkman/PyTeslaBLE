from setuptools import setup, find_packages

setup(
    name='pyteslable',
    version='0.1.0',
    description='Python interface for connecting to Tesla vehicles directly using the BLE API',
    url='https://github.com/kaedenbrinkman/PyTeslaBLE',
    author='Kaeden Brinkman',
    author_email='kaeden@kaedenb.org',
    license='BSD 2-clause',
    packages=find_packages(exclude=['test']),
    install_requires=['simplepyble', 'cryptography', 'protobuf'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
