from setuptools import setup, find_packages

setup(
    name="mode_0",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "twitchio>=2.6.0",
        "aiohttp>=3.8.4",
        "apscheduler>=3.10.1",
        "websockets>=11.0.3",
        "python-dotenv>=1.0.0",
        "colorlog>=6.7.0",
        "sqlalchemy>=2.0.0",
    ],
    python_requires=">=3.11",
)
