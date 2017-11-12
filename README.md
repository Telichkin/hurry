# Hurry!
[![Build Status](https://travis-ci.org/Telichkin/hurry.svg?branch=master)](https://travis-ci.org/Telichkin/hurry)
[![codecov](https://codecov.io/gh/Telichkin/hurry/branch/master/graph/badge.svg)](https://codecov.io/gh/Telichkin/hurry)
[![Python versions](https://img.shields.io/badge/python-3.4%2B-blue.svg)](https://pypi.python.org/pypi/hurry)

**Hurry!** helps you run your routine commands and scripts faster. It transforms commands like 
```docker-compose -f docker-compose.dev.yml up --build -d``` into ```hurry up```.

## Supported Python versions
Current version works with Python 3.4+ only.

## Install 
```pip3 install hurry```

## Usage
In the folder, where you want to use **Hurry!**, create *hurry.json* file with shortcuts:
```bash
$ cat ./hurry.json
{ "hello": "echo Hello, World!" }
```

Now you can use created shortcuts: 
```bash
$ hurry --help
Usage:
    hurry hello

$ hurry hello
Execute: echo Hello, World!
Hello, World!
```

### Templating

**Hurry!** supports simple templating inside shortcuts with `<template>` syntax:
```bash
$ cat ./hurry.json
{ "hello <name>": "echo Hello, <name>!" }

$ hurry --help
Usage:
    hurry hello <name>
```

Quotes are unnecessarily, when you use one-word argument:
```bash
$ hurry hello OneWord
Execute: echo Hello, OneWord!
Hello, OneWord!
```

Quotes are mandatory, when you use many-words argument or argument that starts with dash(-es):
```bash
$ hurry hello "Many Words"
Execute: echo Hello, Many Words!
Hello, Many Words!

$ hurry hello "-words-starts-with-dash"
Execute: echo Hello, -words-starts-with-dash!
Hello, -words-starts-with-dash!
```

### Hurry inside Hurry

It's possible to use already created commands inside **Hurry!**:
```bash
$ cat ./hurry.json
{
    "up": "docker-compose -f path/to/docker-compose.yml up -d",
    "down": "docker-compose -f path/to/docker-compose.yml down",
    "restart": "hurry down && hurry up"
}
```
