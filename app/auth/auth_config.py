# -*- coding: utf-8 -*-
# authomatic providers config.py

import authomatic
from authomatic.providers import oauth1, oauth2

CONFIG = { 
    'twitter': {  # Your internal provider name
        # Provider class
        'class_': oauth1.Twitter,
        'consumer_key': 'Sd6hNLuOnTWM428Q2tObxIeyD',
        'consumer_secret': 'VBk11n5sdMNkUNs49SEcenSUdr86jCXoYplF8nqqwPCXCg398q',
        'id': authomatic.provider_id()
    },

    # 'yahoo': {
    #     'class_': oauth1.Yahoo,
    #     'consumer_key': '##########--',
    #     'consumer_secret': '##########',
    #     'id': authomatic.provider_id()
    # },

    'facebook': {

        'class_': oauth2.Facebook,
        'consumer_key': '586660258357828',
        'consumer_secret': 'ccd636977a6ccc08468950a04a2af812',
        'id': authomatic.provider_id(),
        'scope': oauth2.Facebook.user_info_scope
    },

    'google': {
        'class_': oauth2.Google,
        'consumer_key': '806212413325-r4ga91mim3lnqcu58jgm2uufd52avk20.apps.googleusercontent.com',
        'consumer_secret': 'pL31ijCzorI4XRGJ_rkkWmLn',
        'id': authomatic.provider_id(),
        'scope': oauth2.Google.user_info_scope
    },

    'github': {

        'class_': oauth2.GitHub,
        'consumer_key': '031490de23f3d79f6ad1',
        'consumer_secret': '3c272d0218300e42e319d9a61091873cd6e7b02d',
        'id': authomatic.provider_id(),
        'scope': oauth2.GitHub.user_info_scope
    },

    'linkedin': {
        'class_': oauth2.LinkedIn,
        'consumer_key': '86z1ib5ntkq6io',
        'consumer_secret': '0kLc3ZYeEo4RxiLl',
        'id': authomatic.provider_id(),
        'scope': oauth2.LinkedIn.user_info_scope,
        '_name': 'LinkedIn',
    },
}
