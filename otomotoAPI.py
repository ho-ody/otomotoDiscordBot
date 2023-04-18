import requests

def test():
    testurl1 = 'https://www.otomoto.pl/osobowe/audi/a3/rzeszow?search%5Bfilter_enum_fuel_type%5D=diesel&search%5Bdist%5D=200&search%5Bfilter_float_mileage%3Ato%5D=200000&search%5Bfilter_float_price%3Afrom%5D=15000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'

    # This will yield only the HTML code
    url = testurl1
    response = requests.get(url)

    print(response.text)
