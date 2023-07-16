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


# def open_image(file):
#     return Image.open(file)

def open_image(file):
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # Handle regular image file
        return Image.open(file)

    if file.filename.lower().endswith('.dcm'):
        return Image.open(file.stream)

# import pydicom

# def open_image(file):
#     if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#         # Handle regular image file
#         return Image.open(file)

#     if file.filename.lower().endswith('.dcm'):
#         try:
#             # Handle DICOM file
#             dcm = pydicom.dcmread(file)
#             if hasattr(dcm, 'TransferSyntaxUID'):
#                 pixel_array = dcm.pixel_array
#                 image = Image.fromarray(np.uint8(pixel_array))
#                 return image
#             else:
#                 # Assign a default Transfer Syntax UID if missing
#                 default_transfer_syntax = '1.2.840.10008.1.2'  # Adjust the default UID as needed
#                 dcm.TransferSyntaxUID = default_transfer_syntax
#                 pixel_array = dcm.pixel_array
#                 image = Image.fromarray(np.uint8(pixel_array))
#                 return image
#         except pydicom.errors.InvalidDicomError:
#             raise pydicom.errors.InvalidDicomError('DICOM file is missing TransferSyntaxUID in the file meta information.')

#     # Invalid file format
#     raise ValueError('Invalid file format. Only .jpg, .jpeg, .png, and .dcm files are supported.')


# def read_image(file):
    # image_np = np.array(open_image(file))
    # return cv2.UMat(image_np)

# def read_image(file):
#     if isinstance(file, cv2.UMat):
#         return file
#     else:
#         image_np = np.array(open_image(file))
#         return cv2.UMat(image_np)

def read_image(file):
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        if isinstance(file, cv2.UMat):
            return file
        else:
            image_np = np.array(open_image(file))
            return cv2.UMat(image_np)

    if file.filename.lower().endswith('.dcm'):
        # Read DICOM file with pydicom
        dcm = pydicom.dcmread(file, force=True)
        # Get pixel array from DCM data
        pixel_array = dcm.pixel_array
        return pixel_array


def UMatToPIL(image):
    return Image.fromarray(image.get())


# def ndarrayToPIL(image):
#     return Image.fromarray(image)

# def ndarrayToPIL(image):
#     if isinstance(image, cv2.UMat):
#         image = cv2.UMat.get(image)
#     else:
#         image = image.astype(np.uint8)
#     return Image.fromarray(image)

def ndarrayToPIL(image):
    if isinstance(image, cv2.UMat):
        image = cv2.UMat.get(image)
    elif isinstance(image, float):
        image = np.array(image).astype(np.uint8)
    else:
        image = image.astype(np.uint8)

    if len(image.shape) < 2:
        image = np.expand_dims(image, axis=-1)
    
    return Image.fromarray(image)



def get_uri(image):
    image_data = image
    image_data = image_data.convert("RGB")
    data = io.BytesIO()
    image_data.save(data, "JPEG")

    encoded = b64encode(data.getvalue())
    decoded = encoded.decode("utf-8")

    return "data:image/jpeg;base64,%s" % (decoded)