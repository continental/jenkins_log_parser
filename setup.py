"""
Packages script for jenkins_log_parser
"""
import os
import re
from setuptools import (setup)
sphinx_imported = False
try:
    from sphinx.setup_command import BuildDoc
    sphinx_imported = True
except:
    pass
git_imported = False
try:
    import git
    git_imported = True
except ImportError:
    pass

PROJECT_NAME = "jenkins_log_parser"
DESCRIPTION = """
A small tool to generate human readable log files out of jenkins
build log data directory"""
URL = "https://github.com/continental/jenkins_log_parser"
AUTHOR = "Marcel M. Otte"
AUTHOR_EMAIL = "qwc@users.noreply.github.com"
LICENSE = "Apache License 2.0"
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Continuous Integration Services',
    'Intended Audience :: System Administrators',
    'License :: Apache License 2.0',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development',
    'Topic :: Software Development :: Continuous Integration',
]
CMDCLASS = {}
if sphinx_imported:
    CMDCLASS = {'build_sphinx': BuildDoc}


name = "jenkins_log_parser"

if git_imported and not os.environ.get("VERSION_TAG", None):
    repo = git.Repo()
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = tags[-1].__str__() if len(tags) > 0 else ""
    match_tag = re.fullmatch(
        r"^(releases?\/|v)?([0-9]+\.[0-9]+\.[0-9]+(-?[a-z]+[0-9]*)?)$",
        latest_tag
    )
    if match_tag:
        tag = match_tag.group(2)
        ext = match_tag.group(3)
        if ext is None:
            tag += "-next"
        os.environ["VERSION_TAG"] = tag

version = ("1.0.0"
           if not os.environ.get("VERSION_TAG", None)
           else os.environ["VERSION_TAG"])


setup(
    name=PROJECT_NAME,
    version=version,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    scripts=[
        os.path.join(
            "jenkins_log_parser",
            "jenkins_log_parser"
        )
    ],
    python_requires=">=3.5.2",
    dependency_links=[],
    setup_requires=[],
    tests_require=[],
    install_requires=[],
    extras_require={},
    packages=[
        "jenkins_log_parser",
    ],
    package_data={
    },
    cmdclass=CMDCLASS,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc')
        }
    } if sphinx_imported else {},
)  # noqa
