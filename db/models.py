from datetime import datetime
from sqlalchemy.sql import func

from sqlalchemy import Enum, ForeignKey, BIGINT, SMALLINT, TEXT, DateTime, Integer, Column, VARCHAR, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, declared_attr, Session

from db.utils import DB
from enums.main import LangEnum, VolEnum, MoneyTypeEnum, StatusEnum

session = Session(DB.engine)


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


class AbstractTime(Base):
    __abstract__ = True
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())


class Contact(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bot_link : Mapped[str] = mapped_column(VARCHAR)
    phone_number : Mapped[str] = mapped_column(VARCHAR(13))
    description : Mapped[str] = mapped_column(Text)


class User(AbstractTime):
    chat_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=0)
    lang: Mapped[str] = mapped_column(Enum(LangEnum,values_callable = lambda x : [i.value for i in x]), default=LangEnum.EN)
    categories: Mapped[list['Category']] = relationship("Category", back_populates="owner")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="user")


class Category(AbstractTime):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column("owner_id", BIGINT, ForeignKey("users.chat_id", ondelete="SET NULL"),
                                          nullable=True)
    owner: Mapped['User'] = relationship("User", back_populates="categories")
    books: Mapped[list['Book']] = relationship("Book", back_populates="category")


class Book(AbstractTime):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=True)
    page: Mapped[str] = mapped_column(__type_pos=SMALLINT, nullable=True)
    vol: Mapped[bool] = mapped_column(Enum(VolEnum,values_callable = lambda x : [i.value for i in x]), server_default=VolEnum.SOFT.value)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    amount: Mapped[str] = mapped_column(__type_pos=SMALLINT)
    photo: Mapped[str] = mapped_column(default="https://telegra.ph/file/7d61841cf87d8ebfb276c.png")
    money_type: Mapped[str] = mapped_column(Enum(MoneyTypeEnum,values_callable = lambda x : [i.value for i in x]),
                                            default=MoneyTypeEnum.UZS)
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped['Category'] = relationship("Category", back_populates="books")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates='book')


class Order(AbstractTime):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(Enum(StatusEnum),
                                        server_default=StatusEnum.PENDING.value)
    payment_status: Mapped[str] = mapped_column(Enum(StatusEnum,values_callable = lambda x : [i.value for i in x]),
                                                server_default=StatusEnum.PENDING.value)
    user_id: Mapped[int] = mapped_column('user_id', BIGINT, ForeignKey("users.chat_id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship("User", back_populates="orders")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates='order')


class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    count: Mapped[str] = mapped_column(server_default="False")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    order: Mapped['Order'] = relationship("Order", back_populates='order_items')
    book: Mapped['Book'] = relationship("Book", back_populates='order_items')


class DeleteUser(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT)
    deleted_at: Mapped[int] = mapped_column(DateTime(), server_default=func.now())


class Network(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    link: Mapped[str]

# 10.10.2.186:8000/
