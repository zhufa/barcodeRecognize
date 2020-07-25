from pyzbar.pyzbar import decode
from PIL import Image


def recon(filename):
    t=decode(Image.open(filename))
    return t
