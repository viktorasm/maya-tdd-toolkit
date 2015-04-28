# Maya TDD setup

I'm trying to publish some code in relation to my [TDD in Maya article](http://viktorasm.github.io/tdd/maya/2015/01/01/automated-testing-maya-plugin-development.html). Before it's been a seamless part of the rest of [ngSkinTools](http://www.ngskintools.com) project, but as I'm finding that I need to repeat this setup in other Maya-related projects, this is my attempt to make it a reusable library.

## Installation

* Create your virtual environment
	
	virtualenv venv
	source venv/bin/activate

* Install *dccautomation*: 

    pip install git+https://github.com/rgalanakis/dccautomation.git
    
* Install this package:

	pip install git+https://github.com/viktorasm/maya-tdd-toolkit.git

## Sample project

Checkout [maya-tdd-toolkit-sampleproject](https://github.com/viktorasm/maya-tdd-toolkit-sampleproject) for an example.