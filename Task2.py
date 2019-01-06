import cv2
import numpy as np
import math

def readImage(path, gray):
    readAsGray = 0
    if(gray == False):
        readAsGray = -1
    image = cv2.imread(path, readAsGray)
    return image

def generatePatch(image, length, x, y):
    patchSize = int(length/2)
    return [[(image[i][j] if ((i >= 0 and i < len(image)) and (j >= 0 and j < len(image[0]))) else 0) for j in range(y-patchSize, y+(patchSize+1), 1)] for i in range(x-patchSize, x+(patchSize+1), 1)]

def convolvePatch(patch):
    convolvedPatch = [patch[j][i] for j in range(len(patch[0])-1,-1,-1) for i in range(len(patch)-1,-1,-1)]
    return [convolvedPatch[i:i+len(patch)] for i in range(0, len(convolvedPatch), len(patch))]

def computeGaussianWeight(x, y, sigma):
    pi = math.pi
    x2 = (x**2)
    y2 = (y**2)
    sigmaSquare = (sigma**2)
    numerator = math.exp(-(( x2 + y2 )/(2*sigmaSquare)))
    denominator = (2*pi*sigmaSquare)
    return numerator/denominator

def generateGaussianKernel(length, sigma):
    kernelSize = int(length/2)
    return ([[computeGaussianWeight(i, j, sigma) for j in range(-kernelSize, (kernelSize+1), 1)] for i in range(-kernelSize, (kernelSize+1), 1)])

def normalizeGaussianKernel(gaussianKernel):
    sumOfKernel = 0
    for i in gaussianKernel:
        for j in i:
            sumOfKernel += j
    return ([[(gaussianKernel[i][j]/sumOfKernel if sumOfKernel > 0 else gaussianKernel[i][j]) for j in range(len(gaussianKernel[0]))] for i in range(len(gaussianKernel))])

def computeGaussianKernel(convolutedPatch, length, sigma):
    gaussianKernel = generateGaussianKernel(length, sigma)
    normalizedKernel = normalizeGaussianKernel(gaussianKernel)
    weight = sum([sum([convolutedPatch[i][j] * gaussianKernel[i][j] for j in range(len(gaussianKernel))]) for i in range(len(gaussianKernel))])
    return weight

def scaleDownImage(image):
    return [[image[i][j] for j in range(0,len(image[0])-1,2)] for i in range(0,len(image)-1,2)]

def generateOctaveList(octaveNumber, length):
    sigma1 = 1/(2**(0.5))
    sigma2 = 1
    sigma3 = 2**(0.5)
    sigma4 = 2
    sigma5 = 2/(2**(0.5))
    sigmaList = [sigma1, sigma2, sigma3, sigma4, sigma5]
    return [((2**(octaveNumber))*i) for i in sigmaList]

def normalizeZeros(image):
    maximum = max([max([abs(image[i][j]) for j in range(len(image[0]))]) for i in range(len(image))])
    return [[(abs(image[i][j])/maximum) for j in range(len(image[0]))]for i in range(len(image))]

def writeImage(imageName, image):
    maximum = max([max([abs(image[i][j]) for j in range(len(image[0]))]) for i in range(len(image))])
    writableImage = [[round((image[i][j]/maximum)*255) for j in range(len(image[0]))]for i in range(len(image))]
    cv2.imwrite(imageName+'.png',np.asarray(writableImage))

def computeDifferenceOfGaussian(octaveNumber, gaussianList):
    differenceOfGaussian = []
    for count in range(len(gaussianList)-1):
        firstGaussian = gaussianList[count]
        nextGaussian = gaussianList[count+1]
        difference = [[(firstGaussian[i][j] - nextGaussian[i][j]) for j in range(len(firstGaussian[0]))] for i in range(len(firstGaussian))]
        normalizedDifference = normalizeZeros(difference)
        differenceOfGaussianName = "Octave_"+str((octaveNumber+1))+"_DifferenceOfGaussian_"+str(count+1)
        writeImage(differenceOfGaussianName, normalizedDifference)
        differenceOfGaussian.append(normalizedDifference)       
    return differenceOfGaussian

def detectKeypoints(differenceOfGaussian):
    keypointImages = []
    for count in range(0,2,1):
        firstGaussian = differenceOfGaussian[count]
        middleGaussian = differenceOfGaussian[count+1] 
        lastGaussian = differenceOfGaussian[count+2]
        keypointImage = [[0 for j in range(len(middleGaussian[0]))]for i in range(len(middleGaussian))]
        for x in range(1,len(middleGaussian)-1,1):
            for y in range(1,len(middleGaussian[0])-1,1):
                neighboursList = [firstGaussian[i][j] for j in range(y-1, y+2, 1) for i in range(x-1, x+2, 1)]
                neighboursList.extend([middleGaussian[i][j] for j in range(y-1, y+2, 1) for i in range(x-1, x+2, 1) if not(i==x and j==y)])
                neighboursList.extend([lastGaussian[i][j] for j in range(y-1, y+2, 1) for i in range(x-1, x+2, 1)])
                neighboursList.sort()
                if((middleGaussian[x][y]<=neighboursList[0]) or (middleGaussian[x][y]>=neighboursList[len(neighboursList)-1])):
                    keypointImage[x][y] = middleGaussian[x][y]
        normalizedImage = normalizeZeros(keypointImage)
        keypointImages.append(normalizedImage)
    return keypointImages

def placeKeypoints(originalImage, keypointImages, imageName):
    for keypointImage in keypointImages:
        maximum = max([max([abs(keypointImage[i][j]) for j in range(len(keypointImage[0]))]) for i in range(len(keypointImage))])
        keypointImage = [[round((keypointImage[i][j]/maximum)*255) for j in range(len(keypointImage[0]))]for i in range(len(keypointImage))]
        for x in range(len(originalImage)):
            for y in range(len(originalImage[0])):
                if(keypointImage[x][y] > 10):
                    originalImage[x][y] = [255,255,255]
    cv2.imwrite(imageName+'.png',np.asarray(originalImage))

def applyGaussianFilter(image, colorImage, length=7):
    numberOfOctaves = 4
    outputImage = [[0 for j in range(len(image[0]))] for i in range(len(image))]
    keypoints = {}
    for octaveNumber in range(numberOfOctaves):
        gaussianList = []
        octaveSigmaList = generateOctaveList(octaveNumber, length)
        for sigma in octaveSigmaList:
            for x in range(len(image)):
                for y in range(len(image[0])):
                    patch = generatePatch(image, length, x, y)
                    convolutedPatch = convolvePatch(patch)
                    outputImage[x][y] = computeGaussianKernel(convolutedPatch, length, sigma)        
            normalizedImage = normalizeZeros(outputImage)
            gaussianName = "Octave_"+str((octaveNumber+1))+"_Gaussian Image_"+str(octaveSigmaList.index(sigma)+1)
            writeImage(gaussianName, normalizedImage)
            gaussianList.append(normalizedImage)
        differenceOfGaussian = computeDifferenceOfGaussian(octaveNumber, gaussianList)
        keypointImages = detectKeypoints(differenceOfGaussian)
        for keypointImage in keypointImages:
            imageName = "Octave_"+str((octaveNumber+1))+"_Keypoint Image_"+str(keypointImages.index(keypointImage)+1)
            keypoints[imageName] = keypointImage
        imageName = "Octave_"+str((octaveNumber+1))+"_Output Image"
        placeKeypoints(colorImage, keypointImages, imageName)
        scaledDownImage = scaleDownImage(image)
        scaledDownColorImage = scaleDownImage(colorImage)
        image = [[0 for j in range(len(scaledDownImage[0]))] for i in range(len(scaledDownImage))]
        colorImage = [[0 for j in range(len(scaledDownColorImage[0]))] for i in range(len(scaledDownColorImage))]
        image = scaledDownImage
        colorImage = scaledDownColorImage
        outputImage = [[0 for j in range(len(image[0]))] for i in range(len(image))]
    return keypoints

image = readImage('task2.jpg', True)
colorImage = readImage('task2.jpg', False)

keypointsList = applyGaussianFilter(image, colorImage)
for keypointImage,keypointValue in keypointsList.items():
    writeImage(keypointImage, keypointValue)

