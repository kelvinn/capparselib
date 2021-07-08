from invoke import task


@task
def clean(c, docs=False, bytecode=True, dist=True, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if dist:
        patterns.append('dist/*')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def build(c, docs=False):
    c.run("python setup.py build")
    if docs:
        c.run("sphinx-build docs docs/_build")


@task
def package(c):
    c.run("python setup.py sdist bdist_wheel")


@task
def install(c):
    c.run("python setup.py install")


@task
def unit(c):
    c.run("pip install -r src/requirements-test.txt")  # convert this to inside setup.py, somehow.
    c.run("coverage run setup.py test")


@task
def flake8(c):
    c.run("flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics")
    c.run("flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics")


@task
def upload_test(c):
    c.run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    # c.run("pip install -t /tmp --isolated -i https://test.pypi.org/simple/ capparselib")


@task
def upload(c):
    c.run("twine upload dist/*")
