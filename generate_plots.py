from database import db_session
from models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os.path, datetime
from pytz import timezone
import pytz

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
            update_req = False

    # If an update is necessary, generate a new plot
    if update_req == True:

        scrapes = db_session.query(Scrape).filter_by(alert=alert).all()
        mytz = timezone('US/Pacific')

        #########################
        # create an hourly plot #
        #########################

        hrs = range(24)

        # calculate average number of new posts by hour of day
        new_posts_by_hr = [0] * 24
        scrape_cnt = [0] * 24
        for scrape in scrapes:
            scrape_cnt[scrape.dt.hour] += 1
            new_posts_by_hr[scrape.dt.replace(tzinfo=pytz.utc).astimezone(mytz).hour] += scrape.new_posts

        avg_new_posts_by_hr = [float(new_posts_by_hr[i])/float(scrape_cnt[i])
                                for i in range(len(hrs))]     

        # get the last 24 posts
        last_24_new_posts_by_hr = [0] * 24
        for scrape in scrapes[len(scrapes)-24:]:
            last_24_new_posts_by_hr[scrape.dt.replace(tzinfo=pytz.utc).astimezone(mytz).hour] = scrape.new_posts

        # generate plot        
        with plt.xkcd():
            fig, ax = plt.subplots()
            plt.xlabel('Hour of Day')
            plt.ylabel('# of New Posts')
            plt.plot(hrs, avg_new_posts_by_hr, label='Overall Average')
            plt.plot(hrs, last_24_new_posts_by_hr, label='Last 24 Hrs')
            legen = plt.legend(loc='upper left', shadow = True)
            plt.xlim(0, 23)
            plt.ylim(0, max(max(avg_new_posts_by_hr), max(last_24_new_posts_by_hr))*1.1)
            fig.savefig(pname)

            
    """
        #days = mdates.DayLocator()
        dayfmt = mdates.DateFormatter('%m-%d-%Y')

        dts = []
        new_posts = []

        for scrape in scrapes:
            dts.append(scrape.dt)
            new_posts.append(scrape.new_posts)

        mpl_dts = mdates.date2num(dts)

        with plt.xkcd():
            fig, ax = plt.subplots()
            plt.xlabel('Date')
            plt.ylabel('New posts')
            plt.plot_date(mpl_dts, new_posts, linestyle='-')
            #ax.xaxis.set_major_locator(days)
            ax.xaxis.set_major_formatter(dayfmt)
            fig.autofmt_xdate(bottom=0.18)
            fig.savefig(pname)
    """

    return pname

if __name__ == "__main__":
    alerts = db_session.query(Alert).all()
    if alerts:
        get_plot(alerts[2])
    else:
        print "No alerts in database, cannot run plot function"
