from setuptools import setup, find_packages

setup(
    name="snowflake_notebook",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "snowflake-connector-python>=2.8.0",
        "pandas>=1.0.0",
        "ipython>=7.0.0",
        "python-dotenv>=0.19.0",
    ],
    author="David Gilles",
    author_email="davidgilles69@gmail.com",
    description="Ein Paket für die einfache Integration von Snowflake mit Jupyter Notebooks",
    keywords="snowflake, jupyter, notebook, sql, magic",
    python_requires=">=3.6",
)
