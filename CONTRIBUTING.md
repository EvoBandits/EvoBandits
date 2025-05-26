# Overview

Thanks for taking the time to contribute! We appreciate all contributions, from reporting bugs to
implementing new features. If you're unclear on how to proceed after reading this guide, please
open a [new discussion](https://github.com/EvoBandits/EvoBandits/discussions/new/choose).

## Reporting bugs

We use [GitHub issues](https://github.com/EvoBandits/EvoBandits/issues) to track bugs.
You can report a bug by opening a [new issue](https://github.com/EvoBandits/EvoBandits/issues/new/choose).

Before creating a bug report, please check that your bug has not already been reported, and that
your bug exists on the latest version of EvoBandits. If you find a closed issue that seems to report the
same bug you're experiencing, open a new issue and include a link to the original issue in your
issue description.

Please include as many details as possible in your bug report. The information helps the maintainers
resolve the issue faster.

## Suggesting enhancements

We use [GitHub Discussions](https://github.com/EvoBandits/EvoBandits/discussions) to track suggested
enhancements. You can suggest an enhancement by opening a
[new feature request](https://github.com/EvoBandits/EvoBandits/discussions/new/choose).
Before creating an enhancement suggestion, please check that a similar issue does not already exist.

Please describe the behavior you want and why, and provide examples of how evobandits would be used if
your feature were added.

## Contributing to the codebase

### Picking an issue

Pick an issue by going through the [issue tracker](https://github.com/EvoBandits/EvoBandits/issues) and
finding an issue you would like to work on.

If you would like to take on an issue, please comment on the issue to let others know. You may use
the issue to discuss possible solutions.

### Setting up your local environment

The EvoBandits development flow relies on both Rust and Python, which means setting up your local
development environment is not trivial. If you run into problems, please open a
[new discussion](https://github.com/EvoBandits/EvoBandits/discussions/new/choose)

#### Configuring Git

For contributing to EvoBandits you need a free [GitHub account](https://github.com) and have
[git](https://git-scm.com) installed on your machine. Start by
[forking](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the EvoBandits repository, then
clone your forked repository using `git`:

```bash
git clone https://github.com/<username>/EvoBandits.git
cd EvoBandits
```

Optionally set the `upstream` remote to be able to sync your fork with the EvoBandits repository in the
future:

```bash
git remote add upstream https://github.com/EvoBandits/EvoBandits.git
git fetch upstream
```

#### Installing dependencies

In order to work on EvoBandits effectively, you will need [Rust](https://www.rust-lang.org/) and
[Python](https://www.python.org/).

First, install Rust using [rustup](https://www.rust-lang.org/tools/install).

Next, install Python, for example using [uv](https://docs.astral.sh/uv/getting-started/installation/).

You can now check that everything works correctly by going into the `py-evobandits` directory and
running the test suite (warning: this may be slow the first time you run it):

```bash
cd py-evobandits
uv tool install maturin
maturin develop
uv run pytest
```

This will do a number of things:

- Use Python to create a virtual environment in the `.venv` folder.
- Use [uv](https://github.com/astral-sh/uv) to install all Python
  dependencies for development, linting, and building documentation.
- Use Rust to compile and install EvoBandits in your virtual environment.
- Use [pytest](https://docs.pytest.org/) to run the Python unittests in your virtual environment

Check if linting also works correctly by running:

```bash
pre-commit
```

If this all runs correctly, you're ready to start contributing to the EvoBandits codebase!

#### Updating the development environment

Dependencies are updated regularly. If you do not keep your environment
up-to-date, you may notice tests or CI checks failing, or you may not be able to build EvoBandits at
all.

To update your environment, first make sure your fork is in sync with the EvoBandits repository:

```bash
git checkout main
git fetch upstream
git rebase upstream/main
git push origin main
```

Update all Python dependencies to their current versions in origin/main by running:

```bash
uv sync
```

If the Rust toolchain version has been updated, you should update your Rust toolchain. Follow it up
by running `cargo clean` to make sure your Cargo folder does not grow too large:

```bash
rustup update
cargo clean
```

### Working on your issue

Create a new git branch from the `main` branch in your local repository, and start coding!

The Rust code is located in the `evobandits` directory, while the Python codebase is located in the
`py-evobandits` directory.

Two other things to keep in mind:

- If you add code that should be tested, add tests.
- If you change the public API, update the documentation.

### Pull requests

When you have resolved your issue,
[open a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
in the EvoBandits repository. Please adhere to the following guidelines:

- Title:
    - Start your pull request title with a [conventional commit](https://www.conventionalcommits.org/) tag.
      This helps us add your contribution to the right section of the changelog.
      We use the [Angular convention](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#type).
      Scope can be `rust` and/or `python`, depending on your contribution: this tag determines which changelog(s) will include your change.
      Omit the scope if your change affects both Rust and Python.
    - Use a descriptive title starting with an uppercase letter.
      This text will end up in the [changelog](https://github.com/EvoBandits/EvoBandits/releases), so make sure the text is meaningful to the user.
      Use single backticks to annotate code snippets.
      Use active language and do not end your title with punctuation.
    - Example: ``fix(python): Fix `DataFrame.top_k` not handling nulls correctly``
- Description:
    - In the pull request description, [link](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) to the issue you were working on.
    - Add any relevant information to the description that you think may help the maintainers review your code.
- Make sure your branch is [rebased](https://docs.github.com/en/get-started/using-git/about-git-rebase) against the latest version of the `main` branch.
- Make sure all GitHub Actions checks pass.


After you have opened your pull request, a maintainer will review it and possibly leave some
comments. Once all issues are resolved, the maintainer will merge your pull request, and your work
will be part of the next EvoBandits release!

Keep in mind that your work does not have to be perfect right away! If you are stuck or unsure about
your solution, feel free to open a draft pull request and ask for help.

## Contributing to documentation

The most important components of EvoBandits documentation are the
[user guide](https://evobandits.github.io/EvoBandits/), the
[API references](https://evobandits.github.io/EvoBandits/references/study/).

### User guide

The user guide is maintained in the `docs/source` folder. Before creating a PR first
raise an issue to discuss what you feel is missing or could be improved.

#### Building and serving the user guide

The user guide is built using [MkDocs](https://www.mkdocs.org/).

Activate the virtual environment and run `mkdocs serve` to build and serve the user guide, so you
can view it locally and see updates as you make changes.

#### Creating a new user guide page

Each user guide page is based on a `.md` markdown file. This file must be listed in `mkdocs.yml`.

#### Linting

Before committing, install `pre-commit install` (see above)

### API reference

EvoBandits has an API reference which is directly generated
from the codebase, so in order to contribute, you will have to follow the steps outlined in
[this section](#contributing-to-the-codebase) above.

For the Python API reference, we always welcome good docstring examples. This is a great way to start contributing to EvoBandits!

## Release flow

_This section is intended for EvoBandits maintainers._

EvoBandits releases Rust crates to [crates.io](https://crates.io/crates/evobandits) and Python packages to
[PyPI](https://pypi.org/project/evobandits/).

New releases are marked by an official [GitHub release](https://github.com/EvoBandits/EvoBandits/releases)
and an associated git tag.

### Steps

The steps for releasing a new Rust or Python version are similar. The release process is mostly
automated through GitHub Actions, but some manual steps are required. Follow the steps below to
release a new version.

Start by bumping the version number in the source code:

1. Check the [releases page](https://github.com/EvoBandits/EvoBandits/releases) on GitHub and find the
   appropriate draft release. Note the version number associated with this release.
2. Bump the version number.

- _Rust:_ Update the version number in all `Cargo.toml` files in the `evobandits` directory and
  subdirectories.
- _Python:_ Update the version number in
  [`py-evobandits/Cargo.toml`](https://github.com/EvoBandits/EvoBandits/blob/main/py-evobandits/Cargo.toml#L17) to
  match the version of the draft release.

4. From the `py-evobandits` directory, run `cargo build` to generate a new `Cargo.lock` file.
5. Create a new commit with all files added.
6. Push your branch and open a new pull request to the `main` branch of the main EvoBandits repository.
7. Wait for the GitHub Actions checks to pass, then squash and merge your pull request.

Directly after merging your pull request, release the new version:

8. Go to the release page and draft a release or publish an existing draft.
9. Wait for the workflow to finish, then check
   [crates.io](https://crates.io/crates/evobandits)/[PyPI](https://pypi.org/project/evobandits/)/[GitHub](https://github.com/EvoBandits/EvoBandits/releases)
   to verify that the new EvoBandits release is now available.

### Troubleshooting

It may happen that one or multiple release jobs fail. If so, you should first try to simply re-run
the failed jobs from the GitHub Actions UI.

If that doesn't help, you will have to figure out what's wrong and commit a fix. Once your fix has
made it to the `main` branch, simply re-trigger the release workflow.
