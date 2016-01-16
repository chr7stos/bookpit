""" Copyright (C) 2016  Chris Christodoulou <chris.christodoulou@gmail.com>
                        Orestis Ioannou <orestis@oioannou.com>

This file is part of bookpit. bookpit is free software: you can
redistribute it and/or modify it under the terms of the GNU  Affero General
Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version. For more information
see the COPYING file at the top-level directory """

from flask.ext.testing import TestCase
from app import app_wrapper

app = app_wrapper.app
db = app_wrapper.db

TEST_SQLALCHEMY_DATABASE_URI = app.config['TEST_DB']


class MyTest(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        # fill DB

    def tearDown(self):
        db.session.remove()
        db.drop_all()
