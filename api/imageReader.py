from dbr import *
import re
import datetime

# This will be able to take in a photo of a driver's license and return 3 outcomes
# 1. The bar code on the license was obscured/unreadable and the license was unable to be read
# 2. The bar code was readable, but the age on the given license was under 21
# 3. The bar code was readable and the person was of age
reader = BarcodeReader()
reader.init_license("t0070fQAAACtzOxoYQhfs56mnv7OvJP/vY+MDD8Jx3TjSpRw7S61eRNkMxXqnmB4ESbSPkqlxUxxoqXPJHc4r6ED9CefOzAQaZQ==")


def readLicense(fileName):
    # Detect the bar code, get the correct one with license info into a string
    text_results = reader.decode_file(fileName)
    barcode_text = ""
    for text_result in text_results:
        if len(text_result.barcode_text) > 20:
            barcode_text = text_result.barcode_text
            break

    if barcode_text == "":
        return {"isOfAge": False, "license_id": "Invalid License: Cannot be read"}

    print("BAR CODE TEXT: " + barcode_text)
    # Determine if the person is of age
    return_text = re.findall("\nDBB\d\d\d\d\d\d\d\d\n", barcode_text)
    print("RETURN TEXT: " + str(return_text))
    birth_date = return_text[0][4:len(return_text[0])]
    birth_date = datetime.date(int(birth_date[4:]), int(birth_date[:2]), int(birth_date[2:4]))
    today = datetime.date.today()

    isOfAge = False

    if today.year - birth_date.year > 21:
        isOfAge = True
    elif today.year - birth_date.year == 21 and today.month > birth_date.month:
        isOfAge = True
    elif today.year - birth_date.year == 21 and today.month == birth_date.month and today.day >= birth_date.day:
        isOfAge = True

    license_id = re.findall("DAQ.+\n", barcode_text)

    print("LICENSE_ID: " + str(license_id))

    return {"isOfAge": isOfAge, "license_id": license_id[0][3:-1]}


def main():
    print(readLicense("drivers_license.jpg"))


if __name__ == "__main__":
    main()
