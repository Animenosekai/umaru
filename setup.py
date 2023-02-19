from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()

setup(
    name="procon",
    packages=["procon"],
    version="1.0",
    license="MIT",
    description="A Pro Controller driver to control your computer as if it was a console",
    author="Anime no Sekai",
    author_email="niichannomail@gmail.com",
    url="https://github.com/Animenosekai/procon",
    # download_url="https://github.com/Animenosekai/procon/archive/v1.0.tar.gz",
    keywords=['python', 'pro-controller', 'games', 'controller', 'driver'],
    install_requires=[
        "pynput==1.7.6",
        "hidapi==0.13.1",
        # "dataclasses==0.8",
        "notify-py"
    ],
    entry_points={
        'console_scripts': [
            'procon = procon.__main__:main'
        ]
    },
    classifiers=['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License'],
    long_description=readme_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires='>=3.7, <4',
    package_data={
        'procon': ['LICENSE'],
    },
)
