from setuptools import setup, find_packages

setup(
    name='visual_cryptography',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for (3,3) visual cryptography',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/visual_cryptography',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.21.0',
        'Pillow>=8.3.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'visual-cryptography=src.cryptography.visual_cryptography:main',
        ],
    },
)
