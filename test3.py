import requests
import argparse
from datetime import date, datetime, timedelta
from xml.etree import ElementTree as ET

def get_currency_codes():
    url = "https://www.cbr.ru/scripts/XML_valFull.asp"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        root = ET.fromstring(data)
        currency_codes = {}
        for elem in root.findall('.//Item'):
            code = elem.find('ISO_Char_Code').text
            name = elem.find('Name').text
            currency_codes[code] = name
        return currency_codes
    else:
        raise Exception(f"Не удалось получить данные с кодом ошибки: {response.status_code}")

def get_currency_rates(code, date_str):
    today = date.today()
    specified_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if specified_date > today:
        return "Ошибка: Нельзя получить курс для будущей даты."

    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={specified_date.strftime('%d/%m/%Y')}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        currency_name = None
        rate = None
        
        root = ET.fromstring(data)
        for elem in root.findall('.//Valute'):
            valute_code = elem.find('CharCode').text
            if valute_code == code:
                currency_name = elem.find('Name').text
                rate = elem.find('Value').text
                break

        if rate and currency_name:
            return f"{code} ({currency_name}): {rate}"
        else:
            return f"Курс для валюты с кодом '{code}' на {specified_date.strftime('%Y-%m-%d')} не найден."
    else:
        return f"Не удалось получить данные. Код ошибки: {response.status_code}"

def main():
    parser = argparse.ArgumentParser(description="Консольная утилита для получения курсов валют ЦБ РФ за определенную дату.")
    parser.add_argument("--code", required=True, help="Код валюты в формате ISO 4217")
    parser.add_argument("--date", required=True, help="Дата в формате YYYY-MM-DD")
    args = parser.parse_args()

    currency_codes = get_currency_codes()

    if args.code not in currency_codes:
        print(f"Валюта с кодом '{args.code}' не найдена в списке доступных валют.")
        return

    result = get_currency_rates(args.code, args.date)
    print(result)

if __name__ == "__main__":
    main()