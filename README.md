cl-app
======

Monitors Craigslist for new posts that fit into specific criteria and then alerts the user via e-mail and/or text message.  The project uses BeautifulSoup for scraping, APScheduler for handling scheduled tasks, the Twilio API for text messages, SMPTLib for e-mail, Flask for the webframework, SQLAlchemy for the ORM, and SQLite for the database.

Installation
------------
After cloning the repo, setup a virtual environment with `virtualenv .` and enter the environment with `. bin/activate`.  Once inside the virtualenv use `pip install -r requirements.txt` to install the dependencies.  It should be noted that one of the dependeincies is matplotlib, which is a fairly large library (~50MB).  Matplotlib can be installed via pip, but some of it's dependencies cannot.  In order to install the dependencies, you will need to run `sudo apt-get build-dep python-matplotlib`.  

In order to create the SQLite database, you will need to do the following:
 - Create the db directory: `mkdir tmp`
 - Enter a python console: `python`
 - In the python console, import the init_db function from database.py: `from database import init_db`
 - In the python console, run the init_db function: `init_db()`

You should now see cl_app.db in the tmp directory.

Running
--------
To run the application you will need to start two programs. I use tmux sessions to manage running multiple programs on the same server, but there are other options.

In one tmux session, you will need run the scheduled_tasks.py program, which controls the scraping and alert sending tasks for the application.  In another tmux session, you will want to run the Flask application which will run the web server.

Additional Notes
----------------
I used matplotlib to graph the average number of new posts by hour in order to provide the user with some basic analytics on their search criteria.  I chose to use matplotlib because I was already using it for some data analysis projects and because I didn't want to deal with JavaScript.  In hindisght, considering how bad matplotlib works with virtualenv and pip, it probably would make sense to either re-write the feature using something like Flot, or to remove the feature.  I've largely abandoned this project however, so those changes probably won't be made anytime soon.

Demo
----
N/A - I had a live version of this site up and running on AWS, but pulled it down.  Craigslist blocked the servers IP to prevent scraping, and seeing as this project was mostly for educational/entertainment purposes, I decided to pull it down.  The links below have some screenshots of the site while it was still in action.

More Resources
---------------
Here are a few links to blog posts about the project:
 - http://www.blog.pyoung.net/2015/01/12/cl-app-postmortem/
 - http://www.blog.pyoung.net/2014/02/11/flask-and-matplotlib-xkcd-style/
 - http://www.blog.pyoung.net/2014/02/07/cl-alerts/


