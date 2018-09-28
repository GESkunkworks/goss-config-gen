from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='goss-config-gen',
    description='Generate Gossamer config files and AWS aliases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='gossamer config aws',
    url='https://github.com/GESkunkworks/goss-config-gen',
    use_scm_version=True,
    author='Michael Palmer',
    author_email='github@michaeldpalmer.com',
    packages=find_packages(),
    setup_requires=[],
    install_requires=[
        'setuptools_scm~=3.1.0',
        'six~=1.11.0'
    ],
    entry_points={
        'console_scripts': [
            'goss-config-gen = goss_config_gen.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ]
)
