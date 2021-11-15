from PIL import Image as PIL
from pdf417decoder import PDF417Decoder

# This will be able to take in a photo of a driver's license and return 3 outcomes
# 1. The bar code on the license was obscured/unreadable and the license was unable to be read
# 2. The bar code was readable, but the age on the given license was under 21
# 3. The bar code was readable and the person was of age

def readLicense(image):
    return "licenseText"


def isOfAge(licenseData):
    pass