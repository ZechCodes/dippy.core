# Dippy.Core

This is a bare-bones Discord gateway client that can be used to build Python bot frameworks for Discord. 

# ☢️ THIS IS ALPHA SOFTWARE ☢️

There will be bugs and not all features are implemented. It should be fine to use it but if it goes crazy and gets your bot token reset, well, you've been warned. (Fwiw I've not had issues during development so far)

**PLEASE** report any bugs or issues here. __If you would like to contribute feel free!__

## Contributing

[CONTRIBUTING.md](https://github.com/ZechCodes/dippy.core/blob/v1-alpha/CONTRIBUTING.md)
[CODE_OF_CONDUCT.md](https://github.com/ZechCodes/dippy.core/blob/v1-alpha/CODE_OF_CONDUCT.md)

[Issues](https://github.com/ZechCodes/dippy.core/issues)
[Wiki](https://github.com/ZechCodes/dippy.core/wike)

## Testing

We’re using PyTest in the `/tests` folder. It’s a hardcore alpha right now so often nothing works, so tests should pass if you can get them to, otherwise if the code looks right and doesn’t throw syntax errors it should be fine.

## Setting Up

Dippy.core is built to run on Python 3.9 and uses Poetry for dependency management. So you’ll want to install Poetry first thing
```shell
python -m pip install poetry
```
If your path is setup correctly that should allow you to install the project dependencies. From the root folder of the project run this
```shell
poetry install
```
That will create a virtual environment with all of the necessary packages.

## Bug Reports

As this is a hardcore alpha stage, bug reports should be limited to a quick “it didn’t work” on Discord or in an issue comment. If there’s something larger that is more than just things being broken in an alpha project, go ahead and create an issue and give it the “bug” label. Be sure to include some code that will cause the issue so we can replicate it.

## Contributors

[Zech (Owner)](https://github.com/ZechCodes)
[aryan-debug](https://github.com/aryan-debug)
[wake-code](https://github.com/wake-code)
