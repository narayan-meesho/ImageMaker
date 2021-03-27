import xml.dom.minidom as md
import cairosvg
import base64
import time
from PIL import Image

def current_milli_time():
    return round(time.time() * 1000)


def replaceText(node, newText):
    if node.firstChild.nodeType != node.TEXT_NODE:
        raise Exception("node does not contain text")
    node.firstChild.replaceWholeText(newText)


def findElementByTagNameAndIdAndReplaceText(document, tagName, idValue, newText):
    elements = document.getElementsByTagName(tagName)
    for element in elements:
        if element.hasAttribute('id') and element.getAttribute('id') == idValue:
            replaceText(element, newText)


# def findElementByIdAndReplaceText(document, idValue, newText):
#     element = document.getElementById(idValue)
#     replaceText(element, newText)
#
#
# def findElementByIdAndChangeAttribute(document, idValue, attributeKey, attributeValue):
#     element = document.getElementById(idValue)
#     element.setAttribute(attributeKey, attributeValue)


def findElementByTagNameAndIdAndChangeAttribute(document, tagName, idValue, attributeKey, attributeValue):
    elements = document.getElementsByTagName(tagName)
    for element in elements:
        if element.hasAttribute('id') and element.getAttribute('id') == idValue:
            element.setAttribute(attributeKey, attributeValue)


def resizeImage(originalImagePath, resizedImagePath, newSizeWidth, newSizeHeight):
    img = Image.open(originalImagePath).convert('RGB')
    newsize = (newSizeWidth, newSizeHeight)
    img = img.resize(newsize)
    img.save(resizedImagePath, 'JPEG')

def getImageBase64EncodedString(imagePath):

    with open(imagePath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    encoded_string = str(encoded_string, 'utf-8')
    encoded_string = "data:image/png;base64," + encoded_string
    return encoded_string

def saveAsSVG(document,saveFilePath):

    with open(saveFilePath+".svg", "w") as fs:

        fs.write( document.toxml())
        fs.close()

def saveAsPNG(document,saveFilePath):

    cairosvg.svg2png(bytestring=document.toxml(), write_to=saveFilePath+".png")

def saveAsJPEG(document,saveFilePath):

    saveAsPNG(document, saveFilePath)
    im1 = Image.open(saveFilePath+".png")
    im1.save(saveFilePath+".jpeg")



def main():

    startTime = current_milli_time()

    document = md.parse("Reference1.svg")

    inputImagePath = "product6.jpeg"

    resizedImagePath = "resized_image.jpeg"

    resizeImage(inputImagePath, resizedImagePath, 853, 1280)

    findElementByTagNameAndIdAndReplaceText(document, "tspan", "marketing_text", "Super se Upar")

    findElementByTagNameAndIdAndReplaceText(document, "tspan", "category_text", "Alisha Refined Kurtis")

    findElementByTagNameAndIdAndReplaceText(document, "text", "discount_text", "UP TO 50% OFF")

    findElementByTagNameAndIdAndChangeAttribute(document, "image", "product_image", "xlink:href", getImageBase64EncodedString(resizedImagePath))

    # stop-color:#00D889 stop-color:#00D9FB
    findElementByTagNameAndIdAndChangeAttribute(document, "stop", "start-gradient",  "style", "stop-color:#6F26FF")

    findElementByTagNameAndIdAndChangeAttribute(document, "stop", "stop-gradient", "style", "stop-color:#FFAAFF")

    # saveAsSVG(document, "output")

    # saveAsPNG(document, "output")

    saveAsJPEG(document, "output")

    print(current_milli_time() - startTime)


if __name__ == "__main__":
    main();
