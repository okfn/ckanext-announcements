[![Tests](https://github.com/okfn/ckanext-announcements/workflows/Tests/badge.svg?branch=main)](https://github.com/okfn/ckanext-announcements/actions)

# ckanext-announcements

Allow users to define scheduled announcements

![Screen shot](/docs/imgs/screen.png)

## Requirements

Compatibility with core CKAN versions:

`ckanext-announcements` only works with Python 3

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8             | no            |
| 2.9 (py2)       | no            |
| 2.9 (py3)       | yes           |


## Installation

To install ckanext-announcements:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/okfn/ckanext-announcements.git
    cd ckanext-announcements
    pip install -e .
	pip install -r requirements.txt

3. Add `announcements` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Update DB to add the announcements table

     `ckan db upgrade -p announcements`

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

`ckanext.announcements.limit_announcements` (default: 50)
> Limit for the announcement list

## Developer installation

To install ckanext-announcements for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/okfn/ckanext-announcements.git
    cd ckanext-announcements
    python setup.py develop
    pip install -r dev-requirements.txt

### Activate pre-commits

There are github actions to check code with `flake8` and `black` so
it will be usefull to activate pre-commits

```
pip install pre-commit
pre-commit install
```

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-announcements

If ckanext-announcements should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
