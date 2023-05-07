import requests


def get_link(qr_code_text):
    return (f"https://consumer.1-ofd.ru/api/tickets/ticket/{qr_code_text[qr_code_text.find('f') :]}")

def get_info(qr_code_text):
    link = get_link(qr_code_text)
    ticket = requests.get(link, allow_redirects=True).json()
    return ticket['orgId'], ticket['retailPlaceAddress'], ticket['ticket']['items']



