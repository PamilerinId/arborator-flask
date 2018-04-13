from flask import Flask, render_template, request, make_response, session, redirect
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from flask_login import login_required, login_user, logout_user

from . import auth
from ..models import User
from auth_config import CONFIG
from instance.config import SECRET_KEY
#from run import app

authomatic = Authomatic(CONFIG, SECRET_KEY, report_errors=True)

@auth.route('/provider')
def choose_provider():
    """
    Login Page Handler
    """
    return render_template('auth/index.html')

@auth.route('/login/<provider_name>/', methods=['GET'])
def login(provider_name):
    """
    Login handler.
    """   
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    #####Sessions!! coming back
        # session=session,
        # session_saver=lambda: app.save_session(session, response))
    
    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.error:
            return "Error: {}".format(result.error.message)
        # Something really bad has happened.
        abort(500)
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            #save user id to session
            user = User.query.filter_by(email=result.user.email).first()
            # session['email'] = result.user.email
            if user is None:
                username = authomatic.result.user.email.split('@')[0]
                username = User.make_valid_nickname(username)
                username = User.make_unique_nickname(username)
                ##Save UserDetails To Db
                user, created = User.get_or_create(id = result.user.id,
                auth_provider = result.user.provider.id,
                username = username,
                email=result.user.email,
                first_name=result.user.first_name,
                family_name=result.user.last_name,
                picture_url=result.user.picture,
                access_level = 0
                created_date=datetime.utcnow(),
                last_seen=datetime.utcnow()))
                # ##Add Try/Catch and Logger Here
                # ##Check if user exists before 
                db.session.add(user)
                db.session.commit()

            login_user(user, remember=True)
            ##Check if Super(seperate func>>)
            if user.is_super:#(create list of preset super admin emails... .ini file  maybe)
                return redirect(url_for('home.admin_dash'))
            # elif user.is_admin:
            #     ##check project(s) in charge
            #     ##redirect to project page
             # The rest happens inside the template.
            return render_template('home/index.html', result=result)

    return response


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.choose_provider'))