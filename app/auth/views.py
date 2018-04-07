from flask import Flask, render_template, request, make_response, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from . import auth
from ..models import User
from auth_config import CONFIG
from instance.config import SECRET_KEY
#from run import app

authomatic = Authomatic(CONFIG, SECRET_KEY, report_errors=True)

@auth.route('/sign-in')
def sign_in():
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
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            ##Save UserDetails To Db
            user = User(id = result.user.id,
                        username = result.user.username,
                        email=result.user.email,
                        first_name=result.user.first_name,
                        family_name=result.user.last_name,
                        picture_url=result.user.picture)

            db.session.add(user)
            db.session.commit()
            ##Add Try/Catch and Logger Here
        
        # The rest happens inside the template.
        return render_template('auth/login.html', result=result)
    
    # Don't forget to return the response.
    return response
