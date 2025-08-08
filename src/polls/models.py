import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, func
from app_factory import db
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Poll(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    started_on: Mapped[datetime.datetime] = mapped_column(default=func.now())
    expires_on: Mapped[datetime.datetime] = mapped_column()
    force_expired: Mapped[bool] = mapped_column(default=False)
    hidden: Mapped[bool] = mapped_column(default=False)
    choices: Mapped[List['Choice']] = relationship(back_populates='poll')
    
    
class Choice(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    poll_id: Mapped[int] = mapped_column(ForeignKey('poll.id'))
    poll: Mapped['Poll'] = relationship(back_populates='choices')
    votes: Mapped[List['Vote']] = relationship(back_populates='choice')
    

class Vote(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    choice_id: Mapped[int] = mapped_column(ForeignKey('choice.id'))
    choice: Mapped['Choice'] = relationship(back_populates='votes')
    ip: Mapped[str] = mapped_column()
    cast_on: Mapped[datetime.datetime] = mapped_column(default=func.now())
    comment: Mapped[Optional[str]] = mapped_column()
