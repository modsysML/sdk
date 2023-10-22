# sdk

### Setting up dev env
At this point you should've setup your virtual env

**Installation**

```
pip install -r requirements.txt
```

After installing system dependencies be sure to install pre-commit

```
pip install pre-commit

pre-commit install
```

**Contribution guidelines**

We use commit messages for automated generation of project changelog. For every pull request we request contributors to be compliant with the following commit message notation.

```
<type>: <summary>

<body>
```

Accepted <type> values:

- new = newly implemented user-facing features
- chg = changes in existing user-facing features
- fix = user-facing bugfixes
- oth = other changes which users should know about
- dev = any developer-facing changes, regardless of new/chg/fix status

Summary (The first line)
The first line should not be longer than 75 characters, the second line is always blank and other lines should be wrapped at 80 characters.
