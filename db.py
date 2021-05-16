import psycopg2
from psycopg2 import sql

from classes.Card import Card
from datetime import datetime
from classes.Stock import Stock
from classes.User import User

""""select distinct e.kategori, e.tur, e.isim, e.olusturucu, e.id, " \
            "e.geldigi_tarih, e.hangi_raf, e.kutuphanede_mi, o.reserve_mi from " \
            "envanter e, odunc o where o.reserve_mi=false and e.kutuphanede_mi=true" \
            "and e.id={id}".format(id=item_id_)"""

try:
    connection = psycopg2.connect(user="postgres",
                                  password="dbyagmur99",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="kutuphane")
    cursor = connection.cursor()


except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)


def get_all_stock():
    query = "select * from envanter"
    cursor.execute(query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    records = cursor.fetchall()
    stock_list = []
    for row in records:
        s = Stock(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        stock_list.append(s)
    return stock_list


def get_user(user_id):
    query = "select * from kullanicilar where id::int={barcode_no}".format(barcode_no=user_id)
    cursor.execute(query)
    user = cursor.fetchone()
    return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7])


def get_user_card(user_id):
    query = "select * from kart where sahip_id::int={barcode_no}".format(barcode_no=user_id)
    cursor.execute(query)
    card = cursor.fetchone()
    return Card(card[0], card[1], card[2], card[3])


def control_get_operation(user):
    role = user.category
    query = "select tasima_hakki from sinirlar where kategori={user_role}".format(user_role=repr(role))
    cursor.execute(query)
    limit = cursor.fetchone()
    if (role == 'Öğrenci' or role == 'Memur') and user.owned_item == limit:
        return False
    elif (role == 'Öğretim Görevlisi') and user.owned_item == limit:
        return False
    else:
        return True


def control_get_book(user, item):
    role = user.category
    book_cat = item.category
    book_type = item.kind
    if role != 'Öğretim Görevlisi' and book_cat == 'Kitap' and book_type == 'Ders':
        return False
    else:
        return True


def can_borrow_item(item):
    item_id_ = item.item_id + "  "
    query = "select * from " \
            "envanter where kutuphanede_mi=TRUE " \
            "and id::int={id}".format(id=item_id_)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        return True, "available"
    else:
        query = "select * from odunc where reserve_mi=FALSE " \
                "and obje_id::int={id}".format(id=item_id_)
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            return True, "reserve"
    return False


def borrow_item(user, item):
    item_id_ = item.item_id + "  "
    user_id = user.user_id
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    print(type(formatted_date))
    print(type(now))
    print(formatted_date)
    cursor.execute(sql.SQL("INSERT INTO {} VALUES (%s, %s, %s);").format(sql.Identifier('odunc')), [
        user_id,
        item_id_,
        formatted_date
    ])
    connection.commit()


def reserve_item(user, item):
    item_id_ = item.item_id + "  "
    user_id = user.user_id
    reserve_user = find_owner_reserve(item)
    query = "insert into rezerve values ({item_id}, {owner_id}, {goes_to})".format(item_id=item_id_,
                                                                                   owner_id=reserve_user.user_id,
                                                                                   goes_to=user_id)
    cursor.execute(query)
    connection.commit()


def find_owner_reserve(item):
    item_id_ = item.item_id + "  "
    query = "select alan_id from odunc where obje_id::int={id}".format(id=item_id_)
    cursor.execute(query)
    result = cursor.fetchone()
    reserve_user = get_user(result[0])
    return reserve_user


# odunc tablosuna ekleme yap
def set_item_to_user(user, item):
    query = "update table envanter"


"""finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")"""
