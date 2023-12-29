"""
Contains functions for managing a database to store information about subscribed servers.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.sqlite import insert

_engine = None

class Base(DeclarativeBase):
    pass

class Server(Base):
    __tablename__ = "Server"

    serverid: Mapped[int] = mapped_column(primary_key=True)
    channelid: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Server(serverid={self.serverid!r}, channelid={self.channelid!r})"

def init(conn_str: str) -> None:
    """
    Initializes the database connection. This must be called before any database operations occur.

    Args:
        conn_str: The connection string for the database.
    """
    global _engine
    _engine = create_engine(conn_str, echo=True)
    Base.metadata.create_all(_engine)

def register_loss_channel(server_id: int, channel_id: int):
    """
    Registers a server-channel pairing to send messages in.

    If a server has previously been registered, then the paired channel is instead updated.

    Args:
        server_id: The id of the server to register.
        channel_id: The id of the channel to register.
    """
    with Session(_engine) as session:
        stmt = insert(Server).values([
            {"serverid": server_id, "channelid": channel_id}
        ]).on_conflict_do_update(
            index_elements=[Server.serverid],
            set_=dict(channelid=channel_id)
        )
        session.execute(stmt)
        session.commit()

def get_all_channel_ids() -> list[int]:
    """
    Returns a list of all registered text channels.

    Returns:
        A list of all regsitered channel ids.
    """
    with Session(_engine) as session:
        result = session.query(Server.channelid).all()
        return [result[i][0] for i in range(len(result))]
