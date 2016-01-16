# Developer Guide

This is the Developer's Guide to the Galaxy.

## Flask config

Make sure the Python interpreter can find bookpit's Python modules:

    $ export PYTHONPATH=`pwd`/bookpit:"$PYTHONPATH"
    $ python -c 'import bookpit'  # if this fails, double-check $PYTHONPATH

Using this you can import the bookpit files from anywhere. If bin/run.py
fails because of the import, then you haven't set the Python path correctly.

## Git conventions

**IMPORTANT:** Before your first commit, make sure that you have defined your
name and email properly. When inside the control panel repo directory, use the
following commands to set a per repository email address:

    $ git config user.name "name"
    $ git config user.email "name@email.review"

After your commit and *before* pushing upstream make sure that everything is
fine by inspecting the 'git log' output.

### Branches

  - Develop _one_ feature per branch. The name of the branch should have a
  "feature-" prefix.
  - Solve _one_ bug per branch. The name of the branch should have a "bug-"
  prefix.
  - Add documentation to a doc branch. Name a branch with a "docs-" prefix.
  - Ask someone else to review and merge your branch when it's over. Proper
  merging is done by:

        $ git checkout master
        $ git merge --no-ff <branch_name>

  - Delete a remote branch after merging. In order to do so, first remove the
  remote branch and then the local branch (or vice versa):

        $ git push origin :<branch_name>
        $ git branch -D <branch_name>

    Use `git fetch -p` to update the local branch references afterwards.

  - Use `git pull --rebase` before pushing something to a branch in order to
  avoid unnecessary cycles. You may want to save that in your local config by:

        $ git config branch.autosetuprebase always

### Commit messages

  - The first line should always be 50 characters or less. This is not a full
  sentence (thus don't use a fullstop '.'); think this a short summary of the
  change. Start your phrase with a capital letter and use present tense, e.g.
  "Add support for cookies".
  - The second line should *always* be blank.
  - The third line (or next lines) could have arbitrary text but the lines
  should have at most 72 characters.

(Linus said
[everything](https://github.com/torvalds/linux/pull/17#issuecomment-5659933)!)


Dependencies
------------

* Python >= 3.3
* psycopg2
* python3-dev
* virtualenv

HowTo run for the first time
----------------------------

- virtualenv -p `which python3` virt/
- source ./virt/bin/activate
- pip install -r requirements.txt
- export PYTHONPATH=/path/to/bookpit:$PYTHONPATH
- python ./bin/run.py


## Setting-up a development environment

In Python we tend to work inside a sandbox'ed environment in order to avoid the
dependency hell that might come of! There are various tutorials on how to setup
the best/coolest/you-name-it virtualenv. The quick-and-dirty way is:

    # apt-get install python-setuptools postgresql-9.5 python-psycopg2 python-nose python-nose2-cov
    # easy_install virtualenv
    $ mkdir ~/virt_env
    $ virtualenv -p `which python3` ~/virt_env/bookpit

Activating the virtualenv:

    $ source ~/virt_env/bookpit/bin/activate
    (bookpit) $

Install requirementsin the virtual environment (using Python 3), e.g.

    $ pip install -r requirements.txt

  *WARNING:* If you have problems with that, you might also need to install
  python3-dev.

Checking the installed packages:

    $ pip freeze

If you want to deactivate the current environment:

    (bookpit) $ deactivate
    $

## Creating the databases

In order to be able to use the bookpit app you have to setup a Postgres
database.

1. Install postgres and create an account:

        $ su - postgres 
        $ psql
        psql> CREATE USER [username] WITH ENCRYPTED PASSWORD '[password]';
        psql> CREATE DATABASE [database] ENCODING 'UTF8' OWNER [username] TEMPLATE template0;

3. Create and populate databases:
   - TODO


## TODO

You should probably have a look at the TODO list on trello: 
https://trello.com/b/Y3iVslSU/vivlia-omorfa

## Translations

Package used for internationalization is `flask-babel`. In templates you mark
text for translation using `{{_('text')}}`. In a .py file you have to use
`gettext()` or `lazy_gettext()` to mark certain strings as translatable.

To extract all the translations you need to run:

    pybabel extract -F babel.cfg -o messages.pot bookpit

If there are any `lazy_gettext()`s then you need:

    pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot bookpit

This command creates a messages.pot in the root directory that has all the
strings needed for translation. *Do NOT write inside this file!*

To add a new language:

    pybabel init -i messages.pot -d bookpit/translations -l el

Modify 'el' according to the language code you want to add. Normally, this is
done *once* for each language. Then, you just use `babel update` as described
below.

To update translations, possibly after some strings changed:

    pybabel update -i messages.pot -d bookpit/translations

Finally, once you finished translating generate the results by:

    pybabel compile -f -d bookpit/translations

Afterwards some strings might be marked as *fuzzy* (where it tried to figure out
if a translation matched a changed key). If you have fuzzy entries, make sure to
check them by hand and remove the fuzzy flag before compiling again.
