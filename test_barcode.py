from dbr import *



reader = BarcodeReader()
reader.init_license("t0070fQAAACtzOxoYQhfs56mnv7OvJP/vY+MDD8Jx3TjSpRw7S61eRNkMxXqnmB4ESbSPkqlxUxxoqXPJHc4r6ED9CefOzAQaZQ==") 

try:
    text_results = reader.decode_file("drivers_license.jpg")
    if text_results != None:
        for text_result in text_results:
            print(text_result.barcode_text)
except BarcodeReaderError as bre:
    print(bre)
