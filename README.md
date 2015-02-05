cl-app
======

Monitors Craigslist for new posts that fit into specific criteria and then alerts the user via e-mail and/or text message.  The project uses BeautifulSoup for scraping, APScheduler for handling scheduled tasks, the Twilio API for text messages, SMPTLib for e-mail, Flask for the webframework, SQLAlchemy for the ORM, and SQLite for the database.

Installation
------------
After cloning the repo, setup a virtual environment with `virtualenv .` and enter the environment with `. bi/activate`.  Once inside the virtualenv use `pip install -r requirements.txt` to install the dependencies.  It should be noted that one of the dependeincies is matplotlib, which is a fairly large library (~50MB).  Additionally, I have occasionlay run into complications with the matplotlib installation via pip, although my latest test seemed to work.

Add Database creation instructions here

Running
-------
To run the application you will need to start two programs. I use tmux sessions to manage running multiple programs on the same server, but there are other options.

Add Running Instructions here
