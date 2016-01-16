""" Copyright (C) 2016  Chris Christodoulou <chris.christodoulou@gmail.com>
                        Orestis Ioannou <orestis@oioannou.com>

This file is part of bookpit. bookpit is free software: you can
redistribute it and/or modify it under the terms of the GNU  Affero General
Public License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version. For more information
see the COPYING file at the top-level directory """
#  -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def _get_engine_session(url, verbose=True):
    """ Create a sqlalchemy engine and session using `url`"""
    engine = create_engine(url, echo=verbose)
    session = scoped_session(sessionmaker(bind=engine))
    return engine, session


def _close_session(session):
    """ Close the session """
    session.remove()
