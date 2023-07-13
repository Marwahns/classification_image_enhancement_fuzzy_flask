from PIL import Image
import numpy as np
import cv2
import io
import imageio
import base64
from base64 import b64encode
import pydicom


def convert_dcm(file_content):
    # Membuat objek file-like dari konten file
    file_obj = io.BytesIO(file_content)

    # Membaca file DICOM dari objek file-like
    ds = pydicom.dcmread(file_obj)

    # Mendapatkan array piksel
    im = ds.pixel_array.astype(float)

    # Melakukan normalisasi dan rescaling
    rescaled_image = (np.maximum(im, 0) / im.max()) * 255

    # Mengonversi tipe data menjadi unsigned integer 8-bit
    final_image = np.uint8(rescaled_image)

    # Membuat objek gambar dari array piksel
    image = Image.fromarray(final_image)

    # # Membuat objek file sementara dalam memori
    # img_byte_arr = io.BytesIO()
    # image.save(img_byte_arr, format='PNG')
    # img_byte_arr.seek(0)

    # return img_byte_arr
    
    # Mengonversi gambar menjadi format JPEG
    with io.BytesIO() as output:
        image.save(output, format='JPEG')
        encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
        return encoded_image


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