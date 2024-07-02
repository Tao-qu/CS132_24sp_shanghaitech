import unittest
from test_functions import *

class TestBankingSystem(unittest.TestCase):
    def test_create_account(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.ATM_current_account = 0
        
        length_original = len(DataBase.account_password)
        create_account("123456")
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original+1)
        self.assertIn("123456", DataBase.account_password.values())
        self.assertEqual(DataBase.ATM_current_account, int(get_key(DataBase.account_password, "123456")))
        
        length_original = len(DataBase.account_password)
        create_account("456789")
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertNotIn("456789", DataBase.account_password.values())
        
        return_card()
        length_original = len(DataBase.account_password)
        create_account("abc123")
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertNotIn("abc123", DataBase.account_password.values())
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        length_original = len(DataBase.account_password)
        create_account("123")
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertNotIn("123", DataBase.account_password.values())
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        length_original = len(DataBase.account_password)
        create_account("1234567890123")
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertNotIn("1234567890123", DataBase.account_password.values())
        self.assertEqual(DataBase.ATM_current_account, 0)
        
    def test_close_account(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.account_balance={'2023123456':'0','22222':'500','11111':'500'}
        DataBase.ATM_current_account = 0
        
        length_original = len(DataBase.account_password)
        insert_card("2023123456", "111111")
        close_account()
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original-1)
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        length_original = len(DataBase.account_password)
        insert_card("11111", "11111")
        close_account()
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertEqual(DataBase.ATM_current_account, 11111)
        
        length_original = len(DataBase.account_password)
        transfer_money("22222", "500")
        close_account()
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original-1)
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        length_original = len(DataBase.account_password)
        insert_card("22222", "22222")
        close_account()
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original)
        self.assertEqual(DataBase.ATM_current_account, 22222)
        
        length_original = len(DataBase.account_password)
        withdraw("1000")
        close_account()
        length_new = len(DataBase.account_password)
        self.assertEqual(length_new, length_original-1)
        self.assertEqual(DataBase.ATM_current_account, 0)
        
    def test_insert_card(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        self.assertEqual(DataBase.ATM_current_account, 2023123456)
        
        insert_card("22222", "22222")
        self.assertEqual(DataBase.ATM_current_account, 2023123456)
        
        return_card()
        insert_card("33333", "33333")
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        insert_card("22222", "11111")
        self.assertEqual(DataBase.ATM_current_account, 0)
        
        insert_card("22222", "22222")
        self.assertEqual(DataBase.ATM_current_account, 22222)
        
    def test_return_card(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        self.assertEqual(DataBase.ATM_current_account, 2023123456)
        return_card()
        self.assertEqual(DataBase.ATM_current_account, 0)
        
    def test_deposit(self):
        DataBase.account_password={'2023123456' : '111111', '22222' : '22222', '11111' : '11111'}
        DataBase.account_balance={'2023123456':'0','22222':'500','11111':'500'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        deposit("200")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        deposit("-100")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        deposit("abc")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        return_card()
        deposit("100")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
    def test_withdraw(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.account_balance={'2023123456':'500','22222':'500','11111':'500'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        withdraw("300")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        withdraw("300")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        withdraw("-100")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        withdraw("abc")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
        return_card()
        withdraw("100")
        self.assertEqual(DataBase.account_balance["2023123456"], "200")
        
    def test_log_in(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        
        log_in("2023123456", "111111")
        self.assertEqual(DataBase.app_count, 1)
        self.assertIn("2023123456", DataBase.app_instances.values())
        
        log_in("22222", "11111")
        self.assertEqual(DataBase.app_count, 1)
        self.assertNotIn("22222", DataBase.app_instances.values())
        
        log_in("22222", "22222")
        self.assertEqual(DataBase.app_count, 2)
        self.assertIn("22222", DataBase.app_instances.values())
        
        log_in("33333", "33333")
        self.assertEqual(DataBase.app_count, 2)
        self.assertNotIn("33333", DataBase.app_instances.values())
        
    def test_log_out(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        
        log_in("2023123456", "111111")
        log_in("22222", "22222")
        log_in("11111", "11111")
        log_out(0)
        self.assertEqual(DataBase.app_count, 2)
        self.assertNotIn("2023123456", DataBase.app_instances.values())
        
        log_out(2)
        self.assertEqual(DataBase.app_count, 2)
        
        log_out(1)
        self.assertEqual(DataBase.app_count, 1)
        self.assertNotIn("11111", DataBase.app_instances.values())
        
    def test_close_app(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        
        log_in("2023123456", "111111")
        log_in("22222", "22222")
        log_in("11111", "11111")
        close_app(2)
        self.assertEqual(DataBase.app_count, 2)
        self.assertNotIn("11111", DataBase.app_instances.values())
        
        close_app(2)
        self.assertEqual(DataBase.app_count, 2)
        
        close_app(1)
        self.assertEqual(DataBase.app_count, 1)
        self.assertNotIn("22222", DataBase.app_instances.values())
        
    def test_change_password(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        change_password("123456")
        self.assertEqual(DataBase.account_password["2023123456"], "123456")
        
        log_in("2023123456", "123456")
        log_in("22222", "22222")
        change_password("654321", 1)
        self.assertEqual(DataBase.account_password["22222"], "654321")
        
        change_password("567890", 2)
        self.assertEqual(DataBase.account_password["2023123456"], "123456")
        self.assertEqual(DataBase.account_password["22222"], "654321")
        
        change_password("abcd123")
        self.assertEqual(DataBase.account_password["2023123456"], "123456")
        change_password("123")
        self.assertEqual(DataBase.account_password["2023123456"], "123456")
        change_password("1234567890123")
        self.assertEqual(DataBase.account_password["2023123456"], "123456")
        
    def test_transfer_money(self):
        DataBase.account_password={'2023123456':'111111','22222':'22222','11111':'11111'}
        DataBase.account_balance={'2023123456':'500','22222':'500','11111':'500'}
        DataBase.ATM_current_account = 0
        
        insert_card("2023123456", "111111")
        transfer_money("22222", "100")
        self.assertEqual(DataBase.account_balance["2023123456"], "400")
        self.assertEqual(DataBase.account_balance["22222"], "600")
        
        transfer_money("22222", "600")
        self.assertEqual(DataBase.account_balance["2023123456"], "400")
        self.assertEqual(DataBase.account_balance["22222"], "600")
        
        transfer_money("33333", "100")
        self.assertEqual(DataBase.account_balance["2023123456"], "400")
        
        log_in("22222", "22222")
        transfer_money("11111", "300", 0)
        self.assertEqual(DataBase.account_balance["22222"], "300")
        self.assertEqual(DataBase.account_balance["11111"], "800")  
        
        log_in("11111", "11111")
        transfer_money("22222", "300", 2)
        self.assertEqual(DataBase.account_balance["22222"], "300")
        
        transfer_money("33333", "800", 1)
        self.assertEqual(DataBase.account_balance["11111"], "800")
        
        
if __name__ == '__main__':
    unittest.main()