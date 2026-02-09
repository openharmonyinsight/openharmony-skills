"""Setup script for arkweb-app-debug."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "1.0"

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="arkweb-app-debug",
    version=version,
    author="ArkWeb App Debug Team",
    description="Professional debugging tool for HarmonyOS ArkWeb applications with Chrome DevTools integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/arkweb-app-debug",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Zero dependencies! Uses only Python standard library
    ],
    entry_points={
        "console_scripts": [
            "arkweb-app-debug=arkweb_app_debug.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
