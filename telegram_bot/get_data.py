import requests


def get_link(qr_code_text):
    return (f"https://consumer.1-ofd.ru/api/tickets/ticket/{qr_code_text[qr_code_text.find('f') :]}")

def get_info(qr_code_text):
    link = get_link(qr_code_text)
    ticket = requests.get(link, allow_redirects=True).json()
    return (
            ticket['retailPlaceAddress'],
            ticket['ticket']['items'],
            float(ticket['ticket']['options']['totalSum']) / 100,
            int(ticket['ticket']['fiscalDocumentNumber']),
            int(ticket['ticket']['fiscalDriveNumber']),
            int(ticket['ticket']['fiscalId']),
            ticket['ticket']['insertedAt'][:10]
            )



