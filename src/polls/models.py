import datetime
import pandas
from typing import List, Optional
from flask_login import UserMixin
from sqlalchemy import ForeignKey, func
from app_factory import db
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Poll(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    started_on: Mapped[datetime.datetime] = mapped_column(default=func.now())
    expires_on: Mapped[datetime.datetime] = mapped_column()
    force_expired: Mapped[bool] = mapped_column(default=False)
    hidden: Mapped[bool] = mapped_column(default=False)
    choices: Mapped[List['Choice']] = relationship(back_populates='poll')

    @property
    def total_votes(self):
        total = 0

        for choice in self.choices:
            total += choice.total_votes

        return total
    
    @property
    def failed_votes_count(self):
        total = 0

        for choice in self.choices:
            total += choice.failed_votes_count

        return total
    
    @property
    def current_winner(self):
        sorted_choices = sorted(self.choices, key=lambda choice: choice.total_votes)
        return sorted_choices[0] if sorted_choices else None

    @staticmethod
    def get_active_poll() -> 'Poll':
        return (Poll.query
                .filter(Poll.expires_on > datetime.datetime.now(),
                        Poll.force_expired == False,
                        Poll.hidden == False)
                .order_by(Poll.expires_on.asc(),
                          Poll.started_on.asc()).first())

    def votes_over_time(self, frequency='D'):
        dfs = [choice.votes_over_time(frequency) for choice in self.choices]

        try:
            result = pandas.concat(dfs, axis=1)
        except ValueError:
            return None

        return result


class Choice(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    poll_id: Mapped[int] = mapped_column(ForeignKey('poll.id'))
    poll: Mapped['Poll'] = relationship(back_populates='choices')
    votes: Mapped[List['Vote']] = relationship(back_populates='choice')

    @property
    def total_votes(self):
        result = db.session.query(func.count(Vote.id)).filter(
            Vote.choice == self,
            Vote.failed == False
        ).scalar()

        return result
    
    @property
    def failed_votes_count(self):
        result = db.session.query(func.count(Vote.id)).filter(
            Vote.choice == self,
            Vote.failed == True
        ).scalar()
        
        return result
    
    @property
    def current_percent(self):
        try:
            return (self.total_votes / self.poll.total_votes) * 100
        except ZeroDivisionError:
            return 0

    def votes_over_time(self, frequency='D'):
        df = pandas.DataFrame([{
            'timestamp': vote.cast_on,
            self.text: True,
        } for vote in self.votes if not vote.failed])
        
        if df.empty:
            return None
        
        df['timestamp'] = pandas.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        groups = df.resample(frequency).count()
        
        return groups


class Vote(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    choice_id: Mapped[Optional[int]] = mapped_column(ForeignKey('choice.id'), nullable=True)
    choice: Mapped['Choice'] = relationship(back_populates='votes')
    cast_on: Mapped[datetime.datetime] = mapped_column(default=func.now())
    comment: Mapped[Optional[str]] = mapped_column()
    ip_hash: Mapped[str] = mapped_column()
    fingerprint: Mapped[str] = mapped_column()
    user_id: Mapped[str] = mapped_column()
    failed: Mapped[bool] = mapped_column(default=False)


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(default=False)