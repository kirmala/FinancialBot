import cv2


def read_qr_code_from_file(qr_code_filename):
    img = cv2.imread(qr_code_filename)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    return value


def read_qr_code_from_bytes(qr_code_bytes):
    img = cv2.imdecode(qr_code_bytes, cv2.IMREAD_COLOR)
    cv2.imwrite('test.jpg', img)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)

    return value

# dir_name = os.path.dirname(__file__)
# qr_code_filename = os.path.join(dir_name, 'data/photo_2023-03-23_23-24-07.jpg')
# print(read_qr_code_from_file(qr_code_filename))
