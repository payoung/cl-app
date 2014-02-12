from credentials import SECRET_KEY
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, login_user, login_required, logout_user, session, current_user
from database import db_session
from models import *
import datetime
from forms import EditProfileForm, EditAlertForm
from sqlalchemy import desc
from json import loads
from generate_plots import get_plot


app = Flask(__name__)
login_manager = LoginManager()
app.secret_key = SECRET_KEY
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return db_session.query(User).get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    page = 'login'
    if request.method == 'POST':
        user = db_session.query(User).filter_by(name=request.form['username']).first()
        if user == None or request.form['password'] != user.password:
            error = 'Invalid login information'
        else:
            session['logged_in'] = True
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('user_home_page'))
    return render_template('login.html', error=error, page=page)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    page = 'signup'
    if request.method == 'POST':
        user_check = db_session.query(User).filter_by(name=request.form['username']).first()
        if user_check != None:
            error = 'User name already taken, please choose another one'
        else:
            session['logged_in'] = True
            user = User(name=request.form['username'], password=request.form['password'], 
                    email=request.form['email'], phone=request.form['phone'])
            db_session.add(user)
            db_session.commit()
            login_user(user)
            flash('Thanks for signing up, you are now logged in')
            return redirect(url_for('user_home_page'))
    return render_template('signup.html', error=error, page=page)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/", methods=["GET", "POST"])
@login_required
def user_home_page():
    message1 = "Welcome back, " + current_user.name
    alerts = db_session.query(Alert).filter_by(user=current_user).all()
    return render_template("user_home_page.html", message1=message1, alerts=alerts)


@app.route("/newalert", methods=["GET", "POST"])
@login_required
def newalert():
    error = None
    return render_template("newalert.html", error=error)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_alert():
    email = False; textmessage = False
    notifications_list = request.form.getlist('notifications')
    if 'email' in notifications_list:
        email = True
    if 'textmessage' in notifications_list:
        textmessage = True
    alert = Alert(name=request.form['name'], link=request.form['link'],
                interval=request.form['interval'], email=email,
                text=textmessage, status=1, last_24=0, post_cnt=0,
                last_update=datetime.date.today(), user=current_user)
    db_session.add(alert)
    db_session.commit()
    flash('New alert was created')
    return redirect(url_for('user_home_page'))


@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm(current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db_session.add(current_user)
        db_session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('editprofile'))
    elif request.method != "POST":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template('editprofile.html', form=form)


@app.route('/alertstatus/<alertname>', methods=['GET', 'POST'])
@login_required
def alertstatus(alertname):
    alert = db_session.query(Alert).filter_by(user=current_user, name=alertname).first()
    if alert.email:
        email="Yes"
    else:
        email="No"
    if alert.text:
        text="Yes"
    else:
        text="No"
    if alert.status:
        active="Active"
    else:
        active="Inactive"

    # Load the last 10 posts and display on status page
    last_scrape = db_session.query(Scrape).filter_by(alert=alert).order_by(desc('dt')).first()
    pairs = []
    if last_scrape:
        descs = loads(last_scrape.descs)
        sub_links = loads(last_scrape.links)
        root_link = alert.link.split("org")[0] + "org"
        links = []
        for sub_link in sub_links:
            links.append(root_link + sub_link)
        if len(links) > 10:
            links = links[:10]
            descs = descs[:10]
        for i in range(len(descs)):
            pairs.append((descs[i], links[i]))

    # Get the filepath for the new posts plot
    pname = "/" + get_plot(alert)

    return render_template('alertstatus.html', alert=alert, email=email, 
                            text=text, active=active, pairs=pairs, pname=pname)


@app.route('/editalert/<alertname>', methods=['GET', 'POST'])
@login_required
def editalert(alertname):
    form = EditAlertForm()
    alert = db_session.query(Alert).filter_by(user=current_user, name=alertname).first()
    if form.validate_on_submit():
        alert.name = form.name.data
        alert.link = form.link.data
        alert.interval = form.interval.data
        alert.email = form.email.data
        alert.text = form.text.data
        alert.status = form.status.data
        db_session.add(alert)
        db_session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('editalert', alertname=alert.name))
    elif request.method != "POST":
        form.name.data = alert.name
        form.link.data = alert.link
        form.interval.data = alert.interval
        form.email.data = alert.email
        form.text.data = alert.text
        form.status.data = alert.status
    return render_template('editalert.html', form=form)


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('login'))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.debug = True
    app.run()
