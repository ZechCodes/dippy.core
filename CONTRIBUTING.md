# Welcome
Welcome to the Dippy.cord project! Our goal is to make an easy to use API wrapper for the Discord API and websocket gateway. The hope is that it will be something others can use to build really cool Discord bot frameworks without having to worry about how to handle talking to the API, rate limits, caching, and re-establishing connections.
## Resources
- Currently we have some docs on the GitHub [Wiki](https://github.com/ZechCodes/dippy.core/wiki/)
- If you need quick answers you can join us on the [Beginner.Codes](https://discord.gg/u4UrgtECf3) Discord server. Someday if we have enough interest we may move to a dedicated Discord server.
## Testing
We’re using PyTest in the `/tests` folder. It’s a hardcore alpha right now so often nothing works, so tests should pass if you can get them to, otherwise if the code looks right and doesn’t throw syntax errors it should be fine.
## Setting Up
Dippy.core is built to run on Python 3.9 and uses [Poetry](https://python-poetry.org/) for dependency management. So you’ll want to install Poetry first thing
```sh
python -m pip install poetry
```
If your path is setup correctly that should allow you to install the project dependencies. From the root folder of the project run this
```sh
poetry install
```
That will create a virtual environment with all of the necessary packages.
## Bug Reports
As this is a hardcore alpha stage, bug reports should be limited to a quick “it didn’t work” on Discord or in an issue comment. If there’s something larger that is more than just things being broken in an alpha project, go ahead and create an issue and give it the “bug” label. Be sure to include some code that will cause the issue so we can replicate it.
## Code of Conduct
[CODE_OF_CONDUCT.md](https://github.com/ZechCodes/dippy.core/blob/34bceefec99d156d0746841a95c8bb89a0997d64/CODE_OF_CONDUCT.md)
## Contributor Recognition
We will be updating the readme with the GitHub profiles of anyone who contributes to the project unless otherwise requested.
## Getting Help
If you need any help for any reason you can reach out to [Zech](https://github.com/ZechCodes) on his [Twitter](https://twitter.com/ZechCodes), ask on an appropriate issue, or join us on the [Beginner.Codes](https://discord.gg/u4UrgtECf3) Discord server.
