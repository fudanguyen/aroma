# How to organize your Python data science project

Having done a number of data projects over the years, and having seen a number of them up on GitHub, I've come to see that there's a wide range in terms of how "readable" a project is. I'd like to share some practices that I have come to adopt in my projects, which I hope will bring some organization to your projects.

**Disclaimer:** I'm hoping nobody takes this to be "the definitive guide" to organizing a data project; rather, I hope you, the reader, find useful tips that you can adapt to your own projects. 

**Disclaimer 2:** What I’m writing below is primarily geared towards Python language users. Some ideas may be transferable to other languages; others may not be so. Please feel free to remix whatever you see here!

**Disclaimer 3:** I found the [Cookiecutter Data Science page](http://drivendata.github.io/cookiecutter-data-science/) after finishing this blog post. Many ideas overlap here, though some directories are irrelevant in my work -- which is totally fine, as their Cookiecutter DS Project structure is intended to be flexible! Consistency is the thing that matters the most.

## `README.md`

Let’s start with the most front-facing file in your repository, the README file. It should contain information that will help your forgetful future self, newcomers, and collaborators figure out *why* this project exists, how things are organized, conventions used in the project, and where they can go to find more information.

Note here that the *why* portion is the most important. It gives the necessary context for the reader of your README file. Think of it as documentation that you leave behind, so you don’t have to sit down and explain over and over the high-level overview of the project. 

## Directory Structure

Here is the tl;dr overview: everything gets its own place, and all things related to the project should be placed under child directories one directory. 

	$ pwd
	/path/to/project/directory/
	
	$ ls
	|- notebooks/
	   |- 01-first-logical-notebook.ipynb
	   |- 02-second-logical-notebook.ipynb
	   |- prototype-notebook.ipynb
	   |- archive/
		  |- no-longer-useful.ipynb
	|- projectname/
	   |- projectname/
		  |- __init__.py
		  |- config.py
		  |- data.py
		  |- utils.py
	   |- setup.py
	|- README.md
	|- data/
	   |- raw/
	   |- processed/
	   |- cleaned/
	|- scripts/
	   |- script1.py
	   |- script2.py
	   |- archive/
	      |- no-longer-useful.py
	|- environment.yml

Let's go through each section in order.

### `notebooks/`

	/path/to/project/directory/
	|- notebooks/
	   |- 01-first-logical-notebook.ipynb
	   |- 02-second-logical-notebook.ipynb
	   |- prototype-notebook.ipynb
	   |- archive/
		  |- no-longer-useful.ipynb
	   |- figures/

Quite self-explanatory. We put our notebooks in this directory. As we develop the project, a narrative begins to develop, and we can start structuring our notebooks in "logical chunks" (`{something-logical}-notebook.ipynb`). They should also be ordered, which explains the numbering on the file names. We may use some notebooks for prototyping (`{something}-prototype.ipynb`). Additionally, we may find that some analyses are no longer useful, (`archive/no-longer-useful.ipynb`). Finally, we have a `figures/` directory, which can be optionally further organized, in which figures relevant to the project are placed.

### `projectname/`

	/path/to/project/directory/
	|- projectname/
	   |- projectname/
	      |- __init__.py
	      |- config.py
	      |- custom_funcs.py
	      |- test_config.py
	      |- test_custom_funcs.py
	   |- setup.py

If this looks intimidating, unnecessarily complicated, or something along those lines, humour me for a moment. I have a lesson learned from multiple months of working with other people that led me to this somewhat complicated, but hopefully ultimately useful directory structure.

Under this folder called `projectname/`, we put in a lightweight Python package called `projectname` that has all things that are refactored out of notebooks to keep them clean. It has an `__init__.py` underneath it so that we can import functions and variables into our notebooks and scripts:

	from projectname import something

#### `config.py`

In `projectname/projectname/config.py`, we place in special paths and variables that are used across the project. An example might be:

	# config.py
	
	from pathlib import Path  # pathlib is seriously awesome!
	
	data_dir = Path('/path/to/some/logical/parent/dir')
	data_path = data_dir / 'my_file.csv'  # use feather files if possible!!!
	
	customer_db_url = 'sql:///customer/db/url'
	purchases_db_url = 'sql:///purchases/db/url'

Then, in our notebooks, we can easily import these variables and not worry about custom strings littering our code.

	# notebook.ipynb
	from projectname.config import data_path
	import pandas as pd
	
	df = pd.read_csv(data_path)  # clean!

By using these `config.py` files, we get clean code in exchange for an investment of time naming variables logically.

#### `custom_funcs.py`

In `projectname/projectname/custom_funcs.py`, we can put in custom code that gets used across more than notebook. One example would be downstream data preprocessing that is only necessary for a subset of notebooks.

	# custom_funcs.py
	
	def custom_preprocessor(df):  # give the function a more informative name!!!
	    """
	    Processes the dataframe such that {insert intent here}. (Write better docstrings than this!!!!)
	
	    Intended to be used under this particular circumstance, with {that other function} called before it, and potentially {yet another function} called after it, but optional.
	
	    :param pd.DataFrame df: A pandas dataframe. Should contain the following columns:
	        - col1
	        - col2
	    :returns: A modified dataframe.
	    """
	    return (df.groupby('col1').count()['col2'])

Now, in our notebooks, we can do:

	# notebook.ipynb
	
	import pandas as pd
	from projectname.config import data_path
	from projectname.custom_funcs import custom_preprocessor
	
	df = pd.read_csv(data_path)
	processed = custom_preprocessor(df)

#### `test_{stuff}.py`

Finally, you may have noticed that there is a `test_config.py` and `test_custom_funcs.py` file. Those two modules, which I'll call "test modules", house tests for their respective Python modules (the `config.py` and `custom_funcs.py` files). 

Yes, I'm a big believer that data scientists should be writing tests for their code. Now, these tests don't have to be software-engineer-esque, production-ready tests. The bare minimum is just a single example that shows exactly what you're trying to accomplish with the function. If you accidentally break the function, the test will catch it for you. That's all a test is, and the single example is all that the "bare minimum test" has to cover.

#### `setup.py`

The final part of this is to create a `setup.py` file for the custom Python package (called `projectname`). Here is a simple boilerplate for how it has to look:

	from setuptools import setup, find_packages
	
	setup(name="projectname",
	      version="0.1")

Because this is a package that is intended to stay local and not be uploaded to PyPI, we only need to know its `name` and its `version`. Everything else, including its description, long description, author name, email address and more, are optional. You can include it, but it isn't mandatory.

### `data/`

	/path/to/project/directory/
	|- data/
	   |- raw/
	   |- processed/
	   |- cleaned/
	   |- README.md

Under `data/`, we keep separate directories for the `raw/` data, intermediate `processed/` data, and final `cleaned/` data. (These names, by the way, are completely arbitrary, you can name them in some other way if you desire, as long as they convey the same ideas.)

You'll note that there is also a `README.md` associated with this directory. This is intentional: it should contain the following details:

1. Where the data come from, 
2. What scripts under the `scripts/` directory transformed which files under `raw/` into which files under `processed/` and `cleaned/`, and
3. Why each file under `cleaned/` exists, with optional references to particular notebooks. (Optional, especially when things are still in flux.)

Here, I'm suggesting placing the data under the same project directory, but only under certain conditions. Firstly, only when you're the only person working on the project, and so there's only one authoritative source of data. Secondly, only when your data can fit on disk. 

If you're working with other people, you will want to make sure that all of you agree on what the "authoritative" data source is. If it is a URL (e.g. to an s3 bucket, or to a database), then that URL should be stored and documented in the custom Python package, with a concise variable name attached to it. If it is a path on an HPC cluster and it fits on disk, there should be a script that downloads it so that you have a local version. 

### `scripts/`

	/path/to/project/directory/
	|- scripts/
	   |- script1.py
	   |- script2.py
	   |- archive/
		  |- no-longer-useful.py

Like the `notebooks/` section, I think this is quite self-explanatory. Scripts, defined as logical units of computation that aren't part of the notebook narratives, but nonetheless important for, say, getting the data in shape, or stitching together figures generated by individual notebooks.

## But wait, it's complicated, no?

I proposed this project structure to colleagues, and was met with some degree of ambivalence. 

### Why not just put everything in notebooks?

After all, aren't notebooks supposed to be comprehensive, reproducible units? Yes, but that doesn't mean that they have to be littered with every last detail embedded inside them. Notebooks are great for a data project's narrative, but if they get cluttered up with chunks of code that are copied & pasted from cell to cell, then we not only have an unreadable notebook, we also legitimately have a coding practices problem on hand. This is where the practices of refactoring code come in really handy.

### Why not just `custom.py` under `notebooks/`?

Now, one may ask, "If we can import a `custom.py` from the same directory as the other notebooks, then why bother with the `setup.py` overhead?" My responses are as follows.

If the project truly is small in scale, and you're working on it alone, then yes, don't bother with the `setup.py`. It's too much overhead to worry about.

However, if the project grows big, and multiple people are working on the same project code base (e.g. a "data engineer" + a "data scientist"), then creating the `setup.py` has a few advantages.

Firstly, by creating a custom Python package for project-wide variables, functions, and classes, then they are available for not only notebooks, but also for, say, custom data engineering or report-generation scripts that may need to be run from time to time. This is especially relevant if installed into a project's data science environment (say, using `conda` environments), and I would consider this to be the biggest advantage to creating a custom Python package for the project.

Secondly, we gain a single reference point for custom code. Mentally, if anything, a single reference point for code makes things easier to manage. We can also perform proper code review on the functions without having to worry about digging through the unreadable JSON blobs that Jupyter notebooks are under-the-hood. (Thankfully, we also have [`nbdime`](https://github.com/jupyter/nbdime) to help us with this!)

## Conclusions

I have to admit that I went back-and-forth many, many times over the course over a few months before I finally coalesced on this project structure. It's taken repeated experimentation on new projects and modifying existing ones to reach this point. My hope is that this organizational structure provides some inspiration for your project. 

Perhaps you disagree with me, that this structure isn't the best. I'd love to hear your rationale for a different structure; there may well be inspiration that I could borrow!