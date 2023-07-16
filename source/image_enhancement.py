# untuk komputasi numerik. seperti konversi list menjadi array, menghitung statistik, dan memanipulasi array
import numpy as np 

# untuk operasi morfologi pada citra, seperti dilasi, erosi, opening, closing, dan transformasi lainnya.
import skimage.morphology

# untuk membuat elemen struktur berbentuk disk (lingkaran) yang akan digunakan dalam operasi morfologi.
from skimage.morphology import disk

# menggunakannya untuk membaca, menulis, dan memanipulasi gambar, mengaplikasikan filter dan efek, melakukan deteksi objek, dsb
import cv2

import math

from source.handle_image import get_uri, read_image, open_image, UMatToPIL, ndarrayToPIL, convert_dcm

# https://stackoverflow.com/questions/7110899/how-do-i-apply-a-dct-to-an-image-in-python
# transformasi Fourier cepat (FFT) dan transformasi kosinus diskret (DCT)
# `dct` (Discrete Cosine Transform) digunakan untuk menerapkan transformasi kosinus diskret pada sinyal atau data. DCT mengonversi sinyal waktu atau data menjadi domain frekuensi dengan menghasilkan serangkaian koefisien spektral yang mewakili sinyal tersebut. DCT sering digunakan dalam kompresi data, pemrosesan citra, dan bidang lainnya di mana analisis spektral diperlukan.
# `idct` (Inverse Discrete Cosine Transform) digunakan untuk menerapkan transformasi kosinus diskret terbalik pada koefisien spektral yang dihasilkan oleh dct. DCT terbalik mengembalikan sinyal atau data dari domain frekuensi ke domain waktu atau spasial aslinya. Ini memungkinkan pemulihan data asli setelah proses analisis atau kompresi menggunakan DCT.
from scipy.fftpack import dct, idct

from source.image_enhancement_mamdani import Infer, FuzzyContrastEnhance
from source.image_enhancement_sugeno import FuzzySugenoContrastEnhance
from source.image_enhancement_tsukamoto import FuzzyTsukamotoContrastEnhance

def MamdaniFuzzyContrastEnhance(gray):
    # # Convert cv2.UMat to NumPy array
    # gray_array = gray.get().astype(np.uint8)

    # # Precompute the fuzzy transform
    # x = list(range(0, 256))
    # FuzzyTransform = [Infer(np.array([i]), 127) for i in x]

    # # Apply the transform to grayscale image
    # enhanced = np.array([FuzzyTransform[pixel] for pixel in gray_array.flatten()]).reshape(gray_array.shape)

    # # Min-max scale the output image to fit (0, 255)
    # Min = np.min(enhanced)
    # Max = np.max(enhanced)
    # enhanced = (enhanced - Min) / (Max - Min) * 255

    # # Convert NumPy array back to cv2.UMat
    # enhanced = cv2.UMat(enhanced.astype(np.uint8))

    # return enhanced
    # Precompute the fuzzy transform
    x = list(range(0, 256))
    FuzzyTransform = [Infer(np.array([i]), 127) for i in x]
    
    # Apply the transform to grayscale image
    enhanced = np.array([FuzzyTransform[pixel] for pixel in gray.flatten()]).reshape(gray.shape)
    
    # Min-max scale the output image to fit (0, 255)
    Min = np.min(enhanced)
    Max = np.max(enhanced)
    enhanced = (enhanced - Min) / (Max - Min) * 255
    
    return enhanced.astype(np.uint8)

## Clahe
# def clahe(img_example):
#     img_gray = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8, 8))
#     img_clahe = clahe.apply(img_gray)
#     return img_clahe

def clahe(img_example):
    if isinstance(img_example, cv2.UMat):
        img_example = cv2.UMat.get(img_example)

    if len(img_example.shape) > 2 and img_example.shape[2] == 3:
        img_gray = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    else:
        img_gray = img_example  # Grayscale image

    clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_gray)
    return img_clahe



## Morphologi
## applyStructuringElement masukkin si fuzzy nya
def applyStructuringElement(img_fuzzy):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    tophat = cv2.morphologyEx(img_fuzzy, cv2.MORPH_TOPHAT, kernel)
    bothat = cv2.morphologyEx(img_fuzzy, cv2.MORPH_BLACKHAT, kernel)
    img = cv2.add(img_fuzzy, tophat)
    img = cv2.subtract(img, bothat)
    return img

def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

# transformasi kosinus diskret terbalik dua dimensi (IDCT-2D) secara berurutan
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')  

def dtc_transform(img):
    return idct2(dct2(img))

## Median filter
def medianFilter(img_example):
    noised_samples_example = cv2.medianBlur(img_example, 5)
    return noised_samples_example

# Combine the different approaches
# def combineMamdani(img_example):
#     # img_fuzzy = MamdaniFuzzyContrastEnhance(img_example)
#     # channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     # channel_2 = clahe(img_example)
#     # channel_3 = applyStructuringElement(img_fuzzy)

#     # output = np.dstack((channel_1, channel_2, channel_3))

#     # return output
#     img_fuzzy = FuzzyContrastEnhance(img_example)

#     # Ensure img_example has 3 channels (RGB format)
#     if len(img_example.get().shape) < 3 or img_example.get().shape[2] != 3:
#         img_example = cv2.cvtColor(img_example.get(), cv2.COLOR_GRAY2RGB)

#     channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     channel_2 = clahe(img_example)
#     channel_3 = applyStructuringElement(img_fuzzy)

#     # Convert channel_1 and channel_3 to numpy arrays
#     channel_1 = np.array(channel_1)
#     channel_3 = np.array(channel_3.get())

#     # Resize channel_2 to match the dimensions of channel_1
#     channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

#     # Stack the channels together
#     output = np.dstack((channel_1, channel_2, channel_3))

#     return output[:, :, :3]

def combineMamdani(img_example):
    img_example_np = img_example.get().astype(np.uint8)  # Convert cv2.UMat to NumPy array
    img_fuzzy = FuzzyContrastEnhance(img_example_np)

    # Ensure img_example has 3 channels (RGB format)
    if len(img_example_np.shape) < 3 or img_example_np.shape[2] != 3:
        img_example_np = cv2.cvtColor(img_example_np, cv2.COLOR_GRAY2RGB)

    channel_1 = cv2.cvtColor(img_example_np, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    channel_2 = clahe(img_example_np)
    channel_3 = applyStructuringElement(img_fuzzy)

    # Convert channel_1 and channel_3 to numpy arrays
    channel_1 = np.array(channel_1)

    # Resize channel_2 to match the dimensions of channel_1
    channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

    # Stack the channels together
    output = np.dstack((channel_1, channel_2, channel_3))

    return output[:, :, :3]


# def combineSugeno(img_example):
#     img_fuzzy = FuzzySugenoContrastEnhance(img_example)

#     # Ensure img_example has 3 channels (RGB format)
#     if len(img_example.get().shape) < 3 or img_example.get().shape[2] != 3:
#         img_example = cv2.cvtColor(img_example.get(), cv2.COLOR_GRAY2RGB)

#     channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     channel_2 = clahe(img_example)
#     channel_3 = applyStructuringElement(img_fuzzy)

#     # Convert channel_1 and channel_3 to numpy arrays
#     channel_1 = np.array(channel_1)
#     channel_3 = np.array(channel_3.get())

#     # Resize channel_2 to match the dimensions of channel_1
#     channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

#     # Stack the channels together
#     output = np.dstack((channel_1, channel_2, channel_3))

#     return output[:, :, :3]

def combineSugeno(img_example):
    img_fuzzy = FuzzySugenoContrastEnhance(img_example)

    # Convert img_example to NumPy array if it is a cv2.UMat object
    if isinstance(img_example, cv2.UMat):
        img_example = cv2.UMat.get(img_example)

    # Ensure img_example has 3 channels (RGB format)
    if len(img_example.shape) < 3 or img_example.shape[2] != 3:
        img_example = cv2.cvtColor(img_example, cv2.COLOR_GRAY2RGB)

    channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    channel_2 = clahe(img_example)
    channel_3 = applyStructuringElement(img_fuzzy)

    # Convert channel_1 and channel_3 to numpy arrays
    channel_1 = np.array(channel_1)
    channel_3 = np.array(channel_3.get())

    # Resize channel_2 to match the dimensions of channel_1
    channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

    # Stack the channels together
    output = np.dstack((channel_1, channel_2, channel_3))

    return output[:, :, :3]


# def combineTsukamoto(img_example):
#     img_fuzzy = FuzzyTsukamotoContrastEnhance(img_example)

#     # Ensure img_example has 3 channels (RGB format)
#     if len(img_example.get().shape) < 3 or img_example.get().shape[2] != 3:
#         img_example = cv2.cvtColor(img_example.get(), cv2.COLOR_GRAY2RGB)

#     channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     channel_2 = clahe(img_example)
#     channel_3 = applyStructuringElement(img_fuzzy)

#     # Convert channel_1 and channel_3 to numpy arrays
#     channel_1 = np.array(channel_1)
#     channel_3 = np.array(channel_3.get())

#     # Resize channel_2 to match the dimensions of channel_1
#     channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

#     # Stack the channels together
#     output = np.dstack((channel_1, channel_2, channel_3))

#     return output[:, :, :3]

    # img_fuzzy = FuzzyTsukamotoContrastEnhance(img_example)
    # channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    # channel_2 = clahe(img_example)
    # channel_3 = applyStructuringElement(img_fuzzy)

    # # Convert channel_1, channel_2, and channel_3 to numpy arrays
    # channel_1 = np.array(channel_1.get())
    # channel_2 = np.array(channel_2.get())
    # channel_3 = np.array(channel_3.get())

    # # Resize channel_2 and channel_3 to match the dimensions of channel_1
    # channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))
    # channel_3 = cv2.resize(channel_3, (channel_1.shape[1], channel_1.shape[0]))

    # # Stack the channels together
    # output = np.dstack((channel_1, channel_2, channel_3))

    # return output[:, :, :3]

def combineTsukamoto(img_example):
    img_fuzzy = FuzzyTsukamotoContrastEnhance(img_example)

    # Convert img_example to NumPy array if it is a cv2.UMat object
    if isinstance(img_example, cv2.UMat):
        img_example = cv2.UMat.get(img_example)

    # Ensure img_example has 3 channels (RGB format)
    if len(img_example.shape) < 3 or img_example.shape[2] != 3:
        img_example = cv2.cvtColor(img_example, cv2.COLOR_GRAY2RGB)

    channel_1 = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    channel_2 = clahe(img_example)
    channel_3 = applyStructuringElement(img_fuzzy)

    # Convert channel_1 and channel_3 to numpy arrays
    channel_1 = np.array(channel_1)
    channel_3 = np.array(channel_3.get())

    # Resize channel_2 to match the dimensions of channel_1
    channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))

    # Stack the channels together
    output = np.dstack((channel_1, channel_2, channel_3))

    return output[:, :, :3]



# def histogramEqualization(img_example):
#     img_example_hist = cv2.equalizeHist(img_example)
#     return img_example_hist

def histogramEqualization(img_example):
    if isinstance(img_example, cv2.UMat):
        img_example = cv2.UMat.get(img_example)

    if len(img_example.shape) > 2 and img_example.shape[2] == 3:
        img_gray = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    else:
        img_gray = img_example  # Grayscale image

    if img_gray.dtype != np.uint8:
        img_gray = img_gray.astype(np.uint8)

    img_example_hist = cv2.equalizeHist(img_gray)
    return img_example_hist



# def combineHistogram(img_example):
#     # img_example_gray = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     # img_example_hist = cv2.equalizeHist(img_example_gray)

#     # channel_1 = np.array(img_example_gray.get())  # Convert to NumPy array
#     # channel_2 = clahe(img_example)
#     # channel_3 = applyStructuringElement(img_example_hist)

#     # # Check if channel_1 has valid dimensions
#     # if len(channel_1.shape) < 2:
#     #     return None

#     # # Resize channel_2 and channel_3 to match the dimensions of channel_1
#     # channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))
#     # channel_3 = cv2.resize(channel_3, (channel_1.shape[1], channel_1.shape[0]))

#     # # Convert channel_2 and channel_3 to NumPy arrays
#     # channel_2 = np.array(channel_2.get())
#     # channel_3 = np.array(channel_3.get())

#     # # Stack the channels together
#     # output = np.dstack((channel_1, channel_2, channel_3))

#     # return output[:, :, :3]
#     # Ensure img_example has 3 channels (RGB format)
#     if len(img_example.get().shape) < 3 or img_example.get().shape[2] != 3:
#         img_example = cv2.cvtColor(img_example.get(), cv2.COLOR_GRAY2RGB)
    
#     img_example_gray = cv2.cvtColor(img_example, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
#     img_example_hist = cv2.equalizeHist(img_example_gray)

#     channel_1 = np.array(img_example_gray)  # Convert to NumPy array
#     channel_2 = clahe(img_example)
#     channel_3 = applyStructuringElement(img_example_hist)

#     # Check if channel_1 has valid dimensions
#     if len(channel_1.shape) < 2:
#         return None

#     # Resize channel_2 and channel_3 to match the dimensions of channel_1
#     channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))
#     channel_3 = cv2.resize(channel_3, (channel_1.shape[1], channel_1.shape[0]))

#     # Convert channel_2 and channel_3 to NumPy arrays
#     channel_2 = np.array(channel_2)
#     channel_3 = np.array(channel_3)

#     # Stack the channels together
#     output = np.dstack((channel_1, channel_2, channel_3))

#     return output[:, :, :3]

def combineHistogram(img_example):
    img_example_np = img_example.get()

    if len(img_example_np.shape) < 3 or img_example_np.shape[2] != 3:
        img_example_np = cv2.cvtColor(img_example_np, cv2.COLOR_GRAY2RGB)
    
    img_example_gray = cv2.cvtColor(img_example_np, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    img_example_hist = cv2.equalizeHist(img_example_gray)

    channel_1 = np.array(img_example_gray)  # Convert to NumPy array
    channel_2 = clahe(img_example_np)
    channel_3 = applyStructuringElement(img_example_hist)

    # Check if channel_1 has valid dimensions
    if len(channel_1.shape) < 2:
        return np.zeros((img_example_np.shape[0], img_example_np.shape[1], 3), dtype=np.uint8)

    # Resize channel_2 and channel_3 to match the dimensions of channel_1
    channel_2 = cv2.resize(channel_2, (channel_1.shape[1], channel_1.shape[0]))
    channel_3 = cv2.resize(channel_3, (channel_1.shape[1], channel_1.shape[0]))

    # Convert channel_2 and channel_3 to NumPy arrays
    channel_2 = np.array(channel_2)
    channel_3 = np.array(channel_3)

    # Stack the channels together
    output = np.dstack((channel_1, channel_2, channel_3))

    return output[:, :, :3]



# def MSE(img1, img2):
#     return np.mean(np.square(img1 - img2))

def MSE(img1, img2):
    return np.mean(np.square(img1 - img2))

def PSNR(Max, MSE):
    return 10*math.log10(Max**2/MSE)

def calculate(img_original):
    # Convert the image to grayscale
    img_fuzzy = FuzzyContrastEnhance(img_original)

    # Calculate the MSE values
    # mse_histogram = MSE(img_original, img_fuzzy)

    # # Calculate the PSNR using the MSE
    # psnr_histogram = PSNR(255**2, mse_histogram)

    return img_fuzzy