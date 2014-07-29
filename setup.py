from setuptools import setup

setup(
    name='fill_broken_words',
    version='0.0.1',
    url='http://github.com/mvj3/fill_broken_words/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='split block',
    long_description="Consider there's a sentence, which has a half part of one word outside of it, e.g. ['How many s                 of pizza do you want?', ['lices']], so we need to fix it correctly.",
    packages=['split_block'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'etl_utils',
        'pyenchant',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
