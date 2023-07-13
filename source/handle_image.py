from PIL import Image
import numpy as np
import cv2
import io
import imageio
from base64 import b64encode
import pydicom


def convert_dcm(dcm_file_path):
    # Read DCM file
    dcm = pydicom.dcmread(dcm_file_path)

    # Get pixel data from DCM
    pixel_array = dcm.pixel_array.astype(np.uint8)

    # Convert to JPEG and encode as base64
    data = io.BytesIO()
    imageio.imwrite(data, pixel_array, format="JPEG")
    data.seek(0)

    encoded = b64encode(data.getvalue())
    decoded = encoded.decode("utf-8")

    return "data:image/jpeg;base64,%s" % decoded


def open_image(file):
    return Image.open(file)


def read_image(file):
    image_np = np.array(open_image(file))
    return cv2.UMat(image_np)


def UMatToPIL(image):
    return Image.fromarray(image.get())


def ndarrayToPIL(image):
    return Image.fromarray(image)


def get_uri(image):
    image_data = image
    image_data = image_data.convert("RGB")
    data = io.BytesIO()
    image_data.save(data, "JPEG")

    encoded = b64encode(data.getvalue())
    decoded = encoded.decode("utf-8")

    return "data:image/jpeg;base64,%s" % (decoded)