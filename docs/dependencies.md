# BOOYAH

## Setup Environment

Isolating dependencies is important if your projects run on different versions for the same library.
This is where virtualenv comes to place.

You will need to install `pyenv` and `pyenv-virtualenv` to manage your python versions and virtual environments.

```sh
$ brew install pyenv pyenv-virtualenv
```

Add the following lines to your `.bashrc` or `.zshrc`:

```sh
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Restart your terminal and check if `pyenv` is installed:

```sh
$ pyenv --version
```

Install the python version used in this project:

```sh
$ pyenv install 3.11.4
```

Create a virtual environment for this project:

```sh
$ pyenv virtualenv 3.11.4 booyah
```

Activate the virtual environment:

```sh
$ pyenv activate booyah
```

After activating the virtual environment, you should see `(booyah)` in your terminal.

```sh
(booyah) $ python3 --version
```

If You want to deactivate the virtual environment:

```sh
(booyah) $ pyenv deactivate
```

## Install Dependencies

Remember to activate the virtual environment before installing the dependencies.

```sh
$ pyenv activate booyah
```

We are using pip to manage our dependencies. Make sure you have the latest version of pip installed:

```sh
(booyah) $ pip install --upgrade pip
```

Finally, install the dependencies:

```sh
(booyah) $ pip install -r requirements.txt
```
