""""""
from distutils.core import setup

setup(
    name="pygp",
    scripts=["pygp.py"],
    version="0.0.1",
    description="Pure Python PGP encryption",
    author="Barnaby",
    author_email="b@Zi.iS",
    install_requires={
        'pyaes': '~1.3',
        'rsa': '~3.1'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
    ]
)
