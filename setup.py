from setuptools import find_packages
from setuptools import setup

from version import VERSION

setup(
    name="vkr_project",
    version=VERSION,
    # packages=find_packages(exclude=['*_notebooks', '*playground*']),
    author="Iaroslav Sukhorukov",  # repository maintainer
    author_email="Iarosla-0v@yandex.ru",  # repository maintainer
    install_requires=[

    ],
    package_data={
        'vkr_project': ['py.typed'],
        'vkr_project_docs': ['source/vkr_project_docs/*']
    },
)
