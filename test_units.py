import unittest
import db
import classes


class TestUnit(unittest.TestCase):
    # Alara Hergün
    def test_get_user(self):
        tst_usr = classes.User('Memur', 10020, 'Merve Ece Altınok', 1, 0, 10019, 'mervecealtinok@gmail.com')
        func_usr = db.get_user('10020')

        self.assertIsInstance(func_usr, classes.User)  # Getirilen objenin istenilen sınıfın objesi olup olmadığı

        self.assertEqual(int(func_usr.user_id), tst_usr.user_id)
        self.assertEqual(func_usr.name_surname, tst_usr.name_surname)
        self.assertEqual(int(func_usr.card_id), tst_usr.card_id)
        self.assertEqual(func_usr.email, tst_usr.email)
        self.assertEqual(func_usr.category, tst_usr.category)
        self.assertEqual(func_usr.owned_item, tst_usr.owned_item)
        self.assertEqual(func_usr.reserved_item,
                         tst_usr.reserved_item)  # Getirilien objenin istenilen obje ile aynı özelliklere sahip olup olmadığı

    def test_get_user_card(self):
        tst_card = classes.Card(10019, 10020, 10020, 0)
        func_card = db.get_user_card('10020')

        self.assertIsInstance(func_card, classes.Card)  # Getirilen objenin istenilen sınıfın objesi olup olmadığı

        self.assertEqual(int(func_card.card_id), tst_card.card_id)
        self.assertEqual(int(func_card.balance), tst_card.balance)
        self.assertEqual(int(func_card.password), tst_card.password)
        self.assertEqual(int(func_card.owner_id),
                         tst_card.owner_id)  # Getirilen objenin istenilen obje ile aynı özelliklere sahip olup olmadığı

    # Metin Binbir
    def test_control_get_book(self):
        tst_usr1 = classes.User('Memur', 1, 'User1', 0, 0, 1, '1@1.com')
        tst_usr2 = classes.User('Öğretim Görevlisi', 2, 'User2', 0, 0, 2, '2@2.com')
        tst_usr3 = classes.User('Öğrenci', 3, 'User3', 0, 0, 3, '3@3.com')

        tst_item1 = classes.Stock('Kitap', 'Ders', 'Kitap İsmi', 'Sercan Aksoy', 1, '2020-10-10', 'BCDA', True)
        tst_item2 = classes.Stock('Kitap', 'Bilim', 'Kitap İsmi2', 'Sercan Aksoy', 1, '2020-10-10', 'BCDA', True)

        self.assertFalse(db.control_get_book(tst_usr1, tst_item1))  # Öğretim Görevlisi dışında biri Ders Kitabı alamaz
        self.assertTrue(db.control_get_book(tst_usr2, tst_item1))  # Öğretim Görevlisi Ders Kitabı alabilir
        self.assertTrue(db.control_get_book(tst_usr3,
                                            tst_item2))  # Öğretim Görevlisi dışında biri Ders Kitabı harici kitap alabilir

    def test_is_balance_enough(self):
        balance = 25  # Mukayese edilmesi beklenen değer
        card_id = 10016  # Test aşamasında bakiyesi balance'a yeterli olabilecek bir kart id'si seçilmiştir
        card_id2 = 10015  # Test aşamasında bakiyesi balance'a yetmeyecek bir kart id'si seçilmiştir
        self.assertTrue(db.is_balance_enough(card_id, balance))
        self.assertFalse(db.is_balance_enough(card_id2, balance))

    # Sercan Aksoy
    def test_control_get_operation(self):
        tst_usr1 = classes.User('Memur', 1, 'User1', 3, 0, 1, '1@1.com')
        tst_usr2 = classes.User('Öğretim Görevlisi', 2, 'User2', 6, 0, 2, '2@2.com')
        tst_usr3 = classes.User('Öğrenci', 3, 'User3', 0, 0, 3, '3@3.com')

        self.assertFalse(db.control_get_operation(tst_usr1))  # Memur maksimum 3 kitap alabilir fazlasını alamaz
        self.assertFalse(
            db.control_get_operation(tst_usr2))  # Öğretim Görevlisi maksimum 6 kitap alabilir fazlasını alamaz
        self.assertTrue(db.control_get_operation(tst_usr3))  # Öğrenci maksimum 3 kitap alabilir şuan kitap alabilir

    def test_is_item_reserved(self):
        item_id1 = 10020  # Rezerve edilmiş item seçilmiştir
        item_id2 = 10006  # Rezerve edilmemiş item seçilmiştir

        self.assertTrue(db.is_item_reserved(item_id1))
        self.assertFalse(db.is_item_reserved(item_id2))

    # Yağmur Atak
    def test_have_expired_item(self):
        tst_usr1 = classes.User('Memur', 10013, 'User1', 3, 0, 1, '1@1.com')  # Borca girmiş bir kişi seçilmiştir
        tst_usr2 = classes.User('Öğretim Görevlisi', 10018, 'User2', 6, 0, 2,
                                '2@2.com')  # Borcu olmayan bir kişi seçilmiştir

        self.assertTrue(db.have_expired_item(tst_usr1))
        self.assertFalse(db.have_expired_item(tst_usr2))

    def test_can_borrow_item(self):
        tst_item1 = classes.Stock('Kitap', 'Ders', 'Kitap İsmi', 'Sercan Aksoy', 10009, '2020-10-10', 'BCDA',
                                  True)  # Kütüphanede bulunan item seçildi
        tst_item2 = classes.Stock('Kitap', 'Ders', 'Kitap İsmi', 'Sercan Aksoy', 10001, '2020-10-10', 'BCDA',
                                  False)  # Ödünç ama rezerve olmayan item seçildi
        tst_item3 = classes.Stock('Kitap', 'Ders', 'Kitap İsmi', 'Sercan Aksoy', 10020, '2020-10-10', 'BCDA',
                                  False)  # Rezerve edilmiş item seçildi

        self.assertEqual(db.can_borrow_item(tst_item1), 'available')
        self.assertEqual(db.can_borrow_item(tst_item3), 'false')
        self.assertEqual(db.can_borrow_item(tst_item2), 'reserve')


if __name__ == '__main__':
    unittest.main()
