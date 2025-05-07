from setuptools import setup, find_packages

setup(
    name='beatrica',
    version='2025.5.71632',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description="Beatrica is a tool for code review automation using large language models.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/beatrica',
    packages=find_packages(),
    install_requires=[
        "rich==13.7.1",
        "beatrica-git==0.1.1",
        "beatrica-embedding==0.1.1",
        "langchain-openai==0.1.2",
        "langchain-mistralai==0.1.1",
        "chromadb==0.3.29",
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'coverage',
            'flake8',
            'black',
            'isort',
            'mypy',
            'pre-commit',
            'twine',
            'wheel',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'beatrica=beatrica.beatrica:main',
        ],
    },
)
