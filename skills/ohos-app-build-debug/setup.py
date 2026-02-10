#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Setup Configuration
HarmonyOS/OpenHarmony 应用构建工具安装配置
"""

from setuptools import setup, find_packages
import os

# 读取 README.md 作为长描述
def read_file(filename):
    """读取文件内容"""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="ohos-app-build-debug",
    version="2.1.0",
    author="handyohos",
    author_email="noreply@anthropic.com",
    description="HarmonyOS/OpenHarmony 应用构建工具",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://gitcode.com/openharmonyinsight/openharmony-skills",
    packages=find_packages(exclude=['tests', 'tests.*', '*.egg-info', '__pycache__']),
    python_requires='>=3.7',
    install_requires=[
        # 如果需要额外的依赖，在这里添加
        # 例如：'requests>=2.25.0',
    ],
    entry_points={
        'console_scripts': [
            'ohos-app-build-debug=ohos_app_build_debug:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="harmonyos openharmony ohos devtools build debug hdc",
    project_urls={
        "Bug Reports": "https://gitcode.com/openharmonyinsight/openharmony-skills/issues",
        "Source": "https://gitcode.com/openharmonyinsight/openharmony-skills",
    },
    include_package_data=True,
    zip_safe=False,
)
