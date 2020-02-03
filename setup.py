from setuptools import setup
import re


requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('asyncjw/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


if not version:
    raise RuntimeError('version is not set')

if version[-1] in ["a", "b"]:
    import subprocess
    commit = (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()[:6]
        .decode()
    )
    version += f"+{commit}"



setup(
    name="asyncjw",
    version=version,
    author="Suhail6inkling",
    packages=["asyncjw"],
    python_requires='>=3.5.3',
    install_requires=requirements
)