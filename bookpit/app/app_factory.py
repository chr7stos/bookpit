# Copyright (C) 2016  Chris Christodoulou <chris.christodoulou@gmail.com>
#                        Orestis Ioannou <orestis@oioannou.com>
#
# This file is part of bookpit. bookpit is free software: you can
# redistribute it and/or modify it under the terms of the GNU  Affero General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version. For more information
# see the COPYING file at the top-level directory
#  -*- coding: utf-8 -*-
"""Application factory containing the config and apps."""
import configparser
import os

from flask import Flask
from flask_mail import Mail
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from .session import _get_engine_session


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROBABLE_CONF_FILES = [
    '/etc/bookpit/config.ini',
    '/srv/bookpit/config/config.local.ini',
    '/srv/bookpit/config/config.ini',
    os.path.join(ROOT_DIR, '..', 'config', 'config.local.ini'),
    os.path.join(ROOT_DIR, '..', 'config', 'config.ini'),
]


class AppWrapper(object):
    """Wrapper for apps and session."""

    def __init__(self, session=None):
        """Create a Flask application and sets up its configuration.

        If config and/or session are provided, they will overload the
        default behavior.
        """
        self.session = session
        self.app = Flask(__name__)

    def set_db(self):
        """Read config and set up session and engine."""
        config = configparser.ConfigParser()
        conf_file = guess_conffile()
        config.read(conf_file)
        self.conf = config
        self.app.config['secret_key'] = self.conf["DEFAULT"]['secret']
        # setup sqlalchemy
        if self.session is None:
            self.setup_sqlalchemy()

    def go(self):
        """Set up the necessary apps and run app.

        Set up SQLAlchemy, logging, and imports all the views.
        After creating an AppWrapper and calling this method, the app is ready.
        """
        # read conf
        config = configparser.ConfigParser()
        conf_file = guess_conffile()
        config.read(conf_file)
        self.conf = config
        self.app.config['secret_key'] = self.conf["DEFAULT"]['secret']
        # setup sqlalchemy
        # if self.session is None:
        #    self.setup_sqlalchemy()
        # setup flask-login
        self.lm = LoginManager()
        self.lm.init_app(self.app)
        self.lm.login_view = "login"
        self.lm.login_message = 'Please log in to access this page.'
        # setup flask-mail
        self.setup_mail()
        self.mail = Mail(self.app)
        # setup blueprints
        self.setup_blueprints()
        self.db = SQLAlchemy(self.app)

    def setup_sqlalchemy(self):
        """Create an engine and a session for SQLAlchemy."""
        self.app.config['SQLALCHEMY_DB_URI'] = self.conf["DEFAULT"]['db_uri']
        db_uri = self.app.config['SQLALCHEMY_DB_URI']
        eng, ses = _get_engine_session(db_uri, verbose=False)
        self.engine, self.session = eng, ses

    def setup_mail(self):
        """Set up flask-mail configuration based on the config file."""
        self.app.config["MAIL_SERVER"] = self.conf['MAIL']['smtp']
        self.app.config["MAIL_PORT"] = self.conf['MAIL']['port']
        self.app.config["MAIL_USE_TLS"] = self.conf['MAIL']['tls']
        self.app.config["MAIL_USERNAME"] = self.conf['MAIL']['user']
        self.app.config["MAIL_PASSWORD"] = self.conf['MAIL']['password']

    def setup_blueprints(self):
        """Set up admin and events blueprints."""
        self.admin = Admin(self.app)


def guess_conffile():
    """Find the conffile."""
    for conffile in PROBABLE_CONF_FILES:
        if os.path.exists(conffile):
            if os.stat(conffile).st_size:  # file is not empty
                return conffile

    raise Exception('No configuration file found in %s'
                    % str(PROBABLE_CONF_FILES))
