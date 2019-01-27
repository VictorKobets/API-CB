from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(
        f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
        )  # Использовать переданный requests
    # ...
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    # From
    if cur_from == 'RUR':
        value_from = 1
    else:
        char_from = soup.find('charcode', string=cur_from)
        nominal_from = char_from.find_next('nominal')
        value_from = nominal_from.find_next('value')
        value_from = value_from.string[:-5] + '.' + value_from.string[-4:]
        value_from = Decimal(value_from)
        nominal_from = Decimal(nominal_from.string)
        if nominal_from != 1:
            value_from = value_from / nominal_from
            nominal_from = 1

    # To
    char_to = soup.find('charcode', string=cur_to)
    nominal_to = char_to.find_next('nominal')
    value_to = nominal_to.find_next('value')
    value_to = value_to.string[:-5] + '.' + value_to.string[-4:]
    value_to = Decimal(value_to)
    nominal_to = Decimal(nominal_to.string)
    if nominal_to != 1:
        value_to = value_to / nominal_to
        nominal_to = 1

    # Convert
    amount_from = amount * value_from
    result = amount_from / value_to
    result = result.quantize(Decimal('1.0000'))
    return result  # не забыть про округление до 4х знаков после запятой
