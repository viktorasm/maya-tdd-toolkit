# Maya TDD setup

I'm trying to publish some code in relation to my [TDD in Maya article](http://viktorasm.github.io/tdd/maya/2015/01/01/automated-testing-maya-plugin-development.html). Before it's been a seamless part of the rest of [ngSkinTools](http://www.ngskintools.com) project, but as I'm finding that I need to repeat this setup in other Maya-related projects, this is my attempt to make it a reusable library.

## Installation (venv)

* Create your virtual environment

	```bash	
	virtualenv venv
	source venv/bin/activate
	```

* Install this package:

	```bash
	pip install git+https://github.com/viktorasm/maya-tdd-toolkit.git
	```
	
## Installation (pipenv)

Specify in your `Pipfile`:

```toml
[dev-packages]
pytest = "*"
mayatdd = {git = "https://github.com/viktorasm/maya-tdd-toolkit.git", ref = "master"}
```

## Sample project

Checkout [maya-tdd-toolkit-sampleproject](https://github.com/viktorasm/maya-tdd-toolkit-sampleproject) for an example.
