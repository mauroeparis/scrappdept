from typing import Optional, List

from sqlmodel import (
    create_engine,
    Field,
    select,
    Session,
    SQLModel,
)
from sqlmodel.sql.expression import Select, SelectOfScalar

# Avoiding a warning. More info at: 
# https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True


class Posting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sha: str = Field(index=True, sa_column_kwargs={'unique': True})
    url: str = Field(sa_column_kwargs={'unique': True})
    title: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    sent: bool = Field(default=False, index=True)

    def __key(self):
        return (self.id, self.sha)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Posting):
            return self.__key() == other.__key()
        return NotImplemented

engine = ''

def create_database(engine_name):
    global engine 
    engine = create_engine(f'sqlite:///{engine_name}.db')


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class PostingRepository:
    def create_posting(self, posting: Posting):
        with Session(engine) as session:
            session.add(posting)
            session.commit()

    def get_posting_by_sha(self, sha: str) -> Optional[Posting]:
        with Session(engine) as session:
            statement = select(Posting).where(Posting.sha == sha)
            posting = session.exec(statement).first()

            return posting
    
    def get_unsent_postings(self) -> List[Posting]:
        with Session(engine) as session:
            statement = select(Posting).where(Posting.sent == False)
            postings = [
                posting for posting
                in session.exec(statement)
            ]

            return postings

    def set_posting_as_sent(self, sha: str):
        with Session(engine) as session:
            statement = select(Posting).where(Posting.sha == sha)
            posting = session.exec(statement).first()
            posting.sent = True
            session.add(posting)
            session.commit()
