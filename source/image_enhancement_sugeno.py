## Description:
## Convert input image from RGB to CIELAB, progress on L channel

## Calculate the average pixel intensity - M value

## Fuzzification: For each pixel, calculate degree of membership of each class based on pixel intensity and M value.  𝐼𝑛𝑡𝑒𝑛𝑠𝑖𝑡𝑦∈[0,255]
 

## Inference: Calculate the output fuzzy set from the input pixel intensity based on the proposed rule set

## Defuzzification: For each pixel, calculate centroid value of its output fuzzy set.  𝐶𝑒𝑛𝑡𝑟𝑜𝑖𝑑∈[−50,305]
 

## Normalize output pixel intensity from [-50, 305] to [0, 255]

## Merge modified L channel to the original AB channels, convert output image from CIELAB to RGB.

import numpy as np
import cv2


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

## Inference and Defuzzication (Sugeno's method)
def InferSugeno(i, M, get_fuzzy_set=False):
    # Calculate degree of membership for each class
    VD = VeryDark(i, M)
    Da = Dark(i, M)
    SD = SlightlyDark(i, M)
    SB = SlightlyBright(i, M)
    Br = Bright(i, M)
    VB = VeryBright(i, M)
    EB = ExtremelyBright(i, M)

    # Fuzzy Sugeno Inference:
    output = (
        0.1 * EB,
        0.2 * VB,
        0.3 * Br,
        0.2 * SB,
        0.1 * Da,
        0.1 * VD
    )

    ## Defuzzication
    # Calculate weighted average
    crisp_output = np.average(output)

    # Return fuzzy set and crisp output if requested
    if get_fuzzy_set:
        return crisp_output, output
    return crisp_output


# Proposed fuzzy sugeno method
def FuzzySugenoContrastEnhance(gray):
    # Convert cv2.UMat to NumPy array
    gray_array = gray.get().astype(np.uint8)

    # Precompute the fuzzy transform
    x = list(range(0, 256))
    FuzzySugenoTransform = [InferSugeno(np.array([i]), 127) for i in x]

   # Apply the transform to grayscale image
    enhanced = np.array([FuzzySugenoTransform[pixel] for pixel in gray_array.flatten()]).reshape(gray_array.shape)

    # Min-max scale the output image to fit (0, 255)
    Min = np.min(enhanced)
    Max = np.max(enhanced)
    enhanced = (enhanced - Min) / (Max - Min) * 255

    # Convert NumPy array back to cv2.UMat
    enhanced = cv2.UMat(enhanced.astype(np.uint8))

    return enhanced
