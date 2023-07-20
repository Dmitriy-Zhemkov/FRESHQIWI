import unittest
from test3 import get_currency_rates, get_currency_codes

class TestCurrencyRates(unittest.TestCase):
    def test_get_currency_rates(self):
        # Тест для получения курса доллара США на 2022-10-08
        result = get_currency_rates("USD", "2022-10-08")
        expected_result = "USD (Доллар США): 61.2475"
        self.assertEqual(result.replace(',', '.'), expected_result)

        # Тест для получения курса евро на 2022-10-08
        result = get_currency_rates("EUR", "2022-10-08")
        expected_result = "EUR (Евро): 59.9756"
        self.assertEqual(result.replace(',', '.'), expected_result)

        # Тест для некорректного кода валюты
        result = get_currency_rates("ABC", "2022-10-08")
        expected_result = "Курс для валюты с кодом 'ABC' на 2022-10-08 не найден."
        self.assertEqual(result, expected_result)

        # Тест для будущей даты
        result = get_currency_rates("USD", "2023-10-08")
        expected_result = "Ошибка: Нельзя получить курс для будущей даты."
        self.assertEqual(result, expected_result)

    def test_get_currency_codes(self):
        # Тест для проверки наличия кода валюты USD
        currency_codes = get_currency_codes()
        self.assertIn("USD", currency_codes)

        # Тест для проверки наличия кода валюты EUR
        self.assertIn("EUR", currency_codes)

        # Тест для некорректного кода валюты
        self.assertNotIn("ABC", currency_codes)

if __name__ == "__main__":
    unittest.main()
