## Description:
## Convert input image from RGB to CIELAB, progress on L channel

## Calculate the average pixel intensity - M value

## Fuzzification: For each pixel, calculate degree of membership of each class based on pixel intensity and M value.  𝐼𝑛𝑡𝑒𝑛𝑠𝑖𝑡𝑦∈[0,255]
 

## Inference: Calculate the output fuzzy set from the input pixel intensity based on the proposed rule set

## Defuzzification: For each pixel, calculate centroid value of its output fuzzy set.  𝐶𝑒𝑛𝑡𝑟𝑜𝑖𝑑∈[−50,305]
 

## Normalize output pixel intensity from [-50, 305] to [0, 255]

## Merge modified L channel to the original AB channels, convert output image from CIELAB to RGB.

import math

import cv2
import numpy as np


## Fuzzification of Pixel Intensity
# Gaussian Function:
def G(x, mean, std):
    return np.exp(-0.5*np.square((x-mean)/std))

# Membership Functions:
def ExtremelyDark(x, M):
    return G(x, -50, M/6)

def VeryDark(x, M):
    return G(x, 0, M/6)

def Dark(x, M):
    return G(x, M/2, M/6)

def SlightlyDark(x, M):
    return G(x, 5*M/6, M/6)

def SlightlyBright(x, M):
    return G(x, M+(255-M)/6, (255-M)/6)

def Bright(x, M):
    return G(x, M+(255-M)/2, (255-M)/6)

def VeryBright(x, M):
    return G(x, 255, (255-M)/6)

def ExtremelyBright(x, M):
    return G(x, 305, (255-M)/6)

## Rule Set
## IF input is VeryDark THEN output is ExtremelyDark
## IF input is Dark THEN output is VeryDark
## IF input is SlightlyDark THEN output is Dark
## IF input is SlightlyBright THEN output is Bright
## IF input is Bright THEN output is VeryBright
## IF input is VeryBright THEN output is ExtremelyBright

## Inference and Defuzzication (Mamdani's method)
def OutputFuzzySet(x, f, M, thres):
    x = np.array(x)
    result = f(x, M)
    result[result > thres] = thres
    return result

def AggregateFuzzySets(fuzzy_sets):
    return np.max(np.stack(fuzzy_sets), axis=0)

def Infer(i, M, get_fuzzy_set=False):
    # Calculate degree of membership for each class
    VD = VeryDark(i, M)
    Da = Dark(i, M)
    SD = SlightlyDark(i, M)
    SB = SlightlyBright(i, M)
    Br = Bright(i, M)
    VB = VeryBright(i, M)
    
    # Fuzzy Inference:
    x = np.arange(-50, 306)
    Inferences = (
        OutputFuzzySet(x, ExtremelyDark, M, VD),
        OutputFuzzySet(x, VeryDark, M, Da),
        OutputFuzzySet(x, Dark, M, SD),
        OutputFuzzySet(x, Bright, M, SB),
        OutputFuzzySet(x, VeryBright, M, Br),
        OutputFuzzySet(x, ExtremelyBright, M, VB)
    )
    
    # Calculate AggregatedFuzzySet:
    fuzzy_output = AggregateFuzzySets(Inferences)
    
    # Calculate crisp value of centroid
    if get_fuzzy_set:
        return np.average(x, weights=fuzzy_output), fuzzy_output
    return np.average(x, weights=fuzzy_output)

## Implementasi Fuzzy Mamdani
# Proposed fuzzy method
# def FuzzyContrastEnhance(gray):
#     # Convert cv2.UMat to NumPy array
#     gray_array = gray.get().astype(np.uint8)

#     # Precompute the fuzzy transform
#     x = list(range(0, 256))
#     FuzzyTransform = [Infer(np.array([i]), 127) for i in x]

#     # Apply the transform to grayscale image
#     enhanced = np.array([FuzzyTransform[pixel] for pixel in gray_array.flatten()]).reshape(gray_array.shape)

#     # Min-max scale the output image to fit (0, 255)
#     Min = np.min(enhanced)
#     Max = np.max(enhanced)
#     enhanced = (enhanced - Min) / (Max - Min) * 255

#     # Convert NumPy array back to cv2.UMat
#     enhanced = cv2.UMat(enhanced.astype(np.uint8))

#     return enhanced

def FuzzyContrastEnhance(gray):
    if isinstance(gray, cv2.UMat):
        gray_array = gray.get().astype(np.uint8)
    else:
        gray_array = gray.astype(np.uint8)

    # Precompute the fuzzy transform
    x = list(range(0, 256))
    FuzzyTransform = [Infer(np.array([i]), 127) for i in x]

    # Apply the transform to grayscale image
    enhanced = np.array([FuzzyTransform[pixel] for pixel in gray_array.flatten()]).reshape(gray_array.shape)

    # Min-max scale the output image to fit (0, 255)
    Min = np.min(enhanced)
    Max = np.max(enhanced)
    enhanced = (enhanced - Min) / (Max - Min) * 255

    # Convert NumPy array back to cv2.UMat if necessary
    if isinstance(gray, cv2.UMat):
        enhanced = cv2.UMat(enhanced.astype(np.uint8))

    return enhanced