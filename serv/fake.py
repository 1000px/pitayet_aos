from random import randint
from sqlalchemy.exc import IntegrityError
from serv import db
from serv.models import Order, Dish, Shop, Desk, Category, User
from faker import Faker

# 生成Shop数据
def shop():
  shop = Shop('测试店铺')
  db.session.add(shop)
  try:
    db.session.commit()
  except IntegrityError:
    db.session.rollback()

def order(count=5):
  shop = Shop.query.first()
  fk = Faker(locale='zh_CN')
  i = 0
  while i < count:
    order = Order(
      order_price = fk.pyfloat(left_digits=2, right_digits=2, positive=True),
      shop_id = shop.id,
      desk_id = i
    )
    db.session.add(order)
    print(i)
    i = i + 1
    try:
      db.session.commit()
    except IntegrityError:
      db.session.rollback()

def desk(count=12):
  shop = Shop.query.first()
  fk = Faker(locale='zh_CN')
  i = 1
  while i <= count:
    desk = Desk(
      desk_num=i,
      shop_id=shop.id
    )
    db.session.add(desk)
    i = i + 1
    try:
      db.session.commit()
    except IntegrityError:
      db.session.rollback()

def dish(count=30):
  shop = Shop.query.first()
  fk = Faker(locale='zh_CN')
  i = 0
  while i < count:
    dish = Dish(
      dish_name=fk.word(),
      shop_id=shop.id,
      dish_price=fk.pyfloat(left_digits=2, right_digits=2, positive=True)
    )
    db.session.add(dish)
    i = i + 1
    try:
      db.session.commit()
    except IntegrityError:
      db.session.rollback()

def category(count=5):
  shop = Shop.query.first()
  fk = Faker(locale='zh_CN')
  i = 0
  while i < count:
    category = Category(
      category_name=fk.word()
    )
    db.session.add(category)
    i = i + 1
    try:
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
