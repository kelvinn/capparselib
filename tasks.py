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
def upload_test(c):
    c.run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")


@task
def upload(c):
    c.run("twine upload dist/*")
