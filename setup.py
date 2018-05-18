from setuptools import setup
import os

if os.environ.get('USER','') == 'vagrant':
    del os.link

setup(
    name='PlayStoreReviewsDownloader',
    version='0.1',
    description='Package to scrape google play store reviews',
    author='Ademola Oyewale',
    author_email='saopayne@gmail.com',
    url='https://github.com/saopayne/PlayStoreReviewsDownloader',
    keywords=['google play store reviews', 'reviews', 'play store', 'app reviews'],
    classifiers=[],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ]

)
