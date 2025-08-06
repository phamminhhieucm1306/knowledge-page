from setuptools import setup, find_packages

setup(
    name="knowledge_page",
    version="0.1.0",
    description="A knowledge base management tool.",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)
