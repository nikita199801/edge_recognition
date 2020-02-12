from PIL import Image, ImageDraw
import time
import sys
start_time = time.time()
im1 = Image.open(r"./pov1.png").convert('RGB')
im2 = Image.open(r"./pov2.png").convert('RGB')
im3 = Image.open(r"./pov3.png").convert('RGB')
im4 = Image.open(r"./pov4.png").convert('RGB')
im5 = Image.open(r"./pov5.png").convert('RGB')

class MatrixValues:
    def __init__(self, expectedValue, dispersion, standartDiviation):
        self.expectedValue = expectedValue
        self.dispersion = dispersion
        self.standartDiviation = standartDiviation


def makeMatrixFromPixels(img):
    imgMatrix = []
    left, top, right, bottom = 0, 0, 100, 100
    for i in range(1, 11):
        for j in range(1, 11):
            im2 = img.crop((left, top, right, bottom))
            pixels = list(im2.getdata())
            tmpValue_1 = getExpectedValue(pixels)
            tmpValue_2 = getDispersion(pixels, tmpValue_1)
            imgMatrix.append(MatrixValues(tmpValue_1, tmpValue_2, tmpValue_2 ** 0.5));
            left = img.size[0] - (img.size[0] - j * 100)
            right = left + 100
            bottom = top + 100
        left = 0
        top = img.size[1] - (img.size[1] - i * 100)
        right = left + 100
        bottom = top + 100
    return imgMatrix

def matrixPicker(pixelBrightness):
    tmpResult = -1
    for i in range (len(pixelBrightness)):
        if trueMatrix(pixelBrightness[i]):
            if (tmpResult == -1):
                tmpResult = i
            elif (pixelBrightness[tmpResult].standartDiviation > pixelBrightness[i].standartDiviation):
                tmpResult = i
    return tmpResult


def trueMatrix(obj):
    if ((obj.expectedValue > 127) & (obj.expectedValue < 255)):
        return True
    else:
        return False


def getDispersion(pixelList, expectedValue):
    tmpResult = 0
    for i in range(len(pixelList)):
        tmpResult += (sum(pixelList[i])/3 - expectedValue) ** 2
    return tmpResult/len(pixelList)


def getExpectedValue(pixelList):
    tmpResult=0
    for i in range(len(pixelList)):
        tmpResult+=sum(pixelList[i])/3
    return tmpResult/len(pixelList)

def showMatrix(img):
    imgMatrix = []
    left, top, right, bottom = 0, 0, 100, 100
    for i in range(1, 11):
        for j in range(1, 11):
            im2 = img.crop((left, top, right, bottom));
            pixels = list(im2.getdata())
            imgMatrix.append(pixels);
            left = img.size[0] - (img.size[0] - j * 100)
            right = left + 100
            bottom = top + 100
        left = 0
        top = img.size[1] - (img.size[1] - i * 100)
        right = left + 100
        bottom = top + 100
    return imgMatrix

def makeFileFromObj(objects):
    lst = []
    for i in range(len(brtns)):
        dict = {}
        dict["expectedValue"] = brtns[i].expectedValue
        dict['dispersion'] = brtns[i].dispersion
        dict['standartDiviation'] = brtns[i].standartDiviation
        lst.append(dict)
        with open("data_pov_4.txt", "w") as output:
            output.write(str(lst))

def avgBrightness(mtrx):
    tmpMtrx=[]
    for i in range(len(mtrx)):
        tmpLst = []
        for j in range(len(mtrx[i])):
            tmpLst.append(sum(mtrx[i][j]) / 3)
        tmpMtrx.append(tmpLst)
    with open("data_brts_pov_4.txt", "w") as output:
        output.write(str(tmpMtrx))

finalResult = matrixPicker(makeMatrixFromPixels(im5))
print("Время исполнения алгоритма %.5s секунд" % (time.time() - start_time))
size = sys.getsizeof(makeMatrixFromPixels(im5))
print("Размер используемой памяти: ", size, " Байт")
print("Номер матрицы (квадрата): ", finalResult)
print('=================================')
if (finalResult != -1):
    img2 = Image.new('RGB', (100,100))
    img2.putdata(showMatrix(im5)[finalResult])
    shape = [0,0,99,99]
    img2.save("landing_point_at_pov_5.png")
surface = im4
brtns=makeMatrixFromPixels(surface)
mtx = showMatrix(surface)
makeFileFromObj(brtns)
avgBrightness(mtx)