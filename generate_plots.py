from database import db_session
from models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os.path, datetime

def get_plot(alert):

    """
    This function returns a filepath to a plot of the new posts on craigslist overtime.
    It also checks if a new plot is needed (if the plot is more than an hour old) and 
    generates a new one as required).
    """

    # Check the last modify time on the plot image to see if an update is necessary
    pname = "static/" + alert.user.name + str(alert.id) + ".png"
    update_req = True
    if os.path.isfile(pname):
        plot_m_time = datetime.datetime.fromtimestamp(os.path.getmtime(pname))
        if datetime.datetime.now() - plot_m_time < datetime.timedelta(hours=1):
            unpdate_req = False

    # If an update is necessary, generate a new plot
    if update_req == True:
        days = mdates.DayLocator()
        dayfmt = mdates.DateFormatter('%m-%d-%Y')

        scrapes = db_session.query(Scrape).filter_by(alert=alert).all()

        dts = []
        new_posts = []

        for scrape in scrapes:
            dts.append(scrape.dt)
            new_posts.append(scrape.new_posts)

        with plt.xkcd():
            fig, ax = plt.subplots()
            plt.xlabel('Date')
            plt.ylabel('New posts')
            plt.plot(dts, new_posts)
            ax.xaxis.set_major_locator(days)
            ax.xaxis.set_major_formatter(dayfmt)
            fig.savefig(pname)

    return pname
