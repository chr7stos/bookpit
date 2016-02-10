# Copyright (C) 2016  Chris Christodoulou <chris.christodoulou@gmail.com>
#                        Orestis Ioannou <orestis@oioannou.com>
#
# This file is part of bookpit. bookpit is free software: you can
# redistribute it and/or modify it under the terms of the GNU  Affero General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version. For more information
# see the COPYING file at the top-level directory
#  -*- coding: utf-8 -*-
"""Models used in bookpit."""

from __future__ import absolute_import
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy.ext.declarative import declarative_base
from consts import GENRES

Base = declarative_base()


class Book(Base):
    """Table containing book entries."""

    __tablename__ = "Book"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(Enum(*GENRES, name="genres"), nullable=False)

    def __init__(self, name, year, genre):
        self.name = name
        self.year = year
        self.genre = genre


class Author(Base):
    """Table containing authors of books."""

    __tablename__ = "Author"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Review(Base):
    """Table containing pending and approved reviews."""

    __tablename__ = "Review"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id', ondelete="CASCADE"),
                     nullable=False)
    timestamp = Column(DateTime(timezone=False), index=True, nullable=False)
    approved = Column(Boolean, nullable=False, default=False)

    def __init__(self, content, book_id, timestamp):
        self.content = content
        self.book_id = book_id
        self.timestamp = timestamp


class Vote(Base):
    """Table containing upvotes and downvotes of reviews."""

    __tablename__ = "Vote"
    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('review.id', ondelete="CASCADE"),
                       nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    vote = Column(Integer, nullable=False)

    def __init__(self, review_id, user_id, vote):
        self.review_id = review_id
        self.user_id = user_id
        self.vote = vote


class Comment(Base):
    """Table containing comments on specific reviews."""

    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    review_id = Column(Integer, ForeignKey('review.id', ondelete="CASCADE"),
                       nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"),
                     nullable=False)
    timestamp = Column(DateTime(timezone=False),
                       index=True, nullable=False)

    def __init__(self, content, review_id, user_id, timestamp):
        self.content = content
        self.review_id = review_id
        self.timestamp = timestamp
        self.user_id = user_id


class BooksAuthors(Base):
    """Relationship between authors and books."""

    __tablename__ = "BooksAuthors"
    book_id = Column(Integer, ForeignKey('book.id', ondelete="CASCADE"),
                     nullable=False)
    author_id = Column(Integer, ForeignKey('author.id', ondelete="CASCADE"),
                       nullable=False)

    def __init__(self, book, author):
        self.book_id = book
        self.author_id = author


class User(Base):
    """Flask-login Users."""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(254), unique=True, nullable=False)
    password = Column(String(254), nullable=False)
    enabled = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        """Output a user."""
        return self.username

    def to_dict(self):
        return dict(id=self.id, username=self.username,
                    enabled=self.enabled, admin=self.admin)

    ''' Flask-login methods '''

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.enabled

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
