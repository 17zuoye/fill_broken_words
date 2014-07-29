from setuptools import setup

setup(
    name='fill_broken_words',
    version='0.0.2',
    url='http://github.com/mvj3/fill_broken_words/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='Fill broken words',
    long_description="Consider there's a sentence, which has a half part of one word outside of it, e.g. ['How many s                 of pizza do you want?', ['lices']], so we need to fix it correctly.",
    packages=['fill_broken_words', 'fill_broken_words/patterns_vs_word',],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'etl_utils',
        'pyenchant',
        'split_block',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
