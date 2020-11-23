import os
import re
from pathlib import Path

from setuptools import find_packages, setup

NAME = "ptools_bin"
PACKAGES = find_packages()
META_PATH = Path("ptools_bin", "__init__.py")
PROJECT_URLS = {
    "Source Code": "https://github.com/ENCODE-DCC/ptools_bin",
    "Issue Tracker": "https://github.com/ENCODE-DCC/ptools_bin/issues",
}
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
]
INSTALL_REQUIRES = ["numpy>=1.19.2", "biopython>=1.78", "pandas>=1.1.3"]

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with Path(HERE, *parts).open(encoding="utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")
URL = find_meta("url")
LONG = read("README.md")
DESCRIPTION = find_meta("description")
LICENSE = find_meta("license")
AUTHOR = find_meta("author")
EMAIL = find_meta("email")
SCRIPTS = [
    "bin/makepBAM_genome.sh",
    "bin/makepBAM_transcriptome.sh",
    "bin/makeBAM.sh",
    "bin/makeDiff.sh",
    "bin/makeFastq.sh",
]
ENTRY_POINTS = {
    "console_scripts": [
        "getSeq_genome_wN=ptools_bin.getSeq_genome_wN:main",
        "getSeq_genome_woN=ptools_bin.getSeq_genome_woN:main",
        "pbam_mapped_transcriptome=ptools_bin.pbam_mapped_transcriptome:main",
        "make_unique=ptools_bin.make_unique:main",
        "print_unique=ptools_bin.print_unique:main",
        "10x_bam2fastq=ptools_bin.10xbam2fastq:main",
        "createDiff=ptools_bin.createDiff:main",
        "compress=ptools_bin.compress:main",
        "pbam2bam=ptools_bin.pbam2bam:main",
    ]
}
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls=PROJECT_URLS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.5",
    scripts=SCRIPTS,
    entry_points=ENTRY_POINTS,
)
