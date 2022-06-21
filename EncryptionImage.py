from PIL import Image
import sys

#Import the color image
image = Image.open("color_image.jpg")
color_image = image.convert('CMYK')

#Decompose the given in image into three individual C,M,Y monotone images.
image_C = Image.new("CMYK", [dimension for dimension in image.size])
image_M = Image.new("CMYK", [dimension for dimension in image.size])
image_Y = Image.new("CMYK", [dimension for dimension in image.size])

for x in range(0, image.size[0], 1):
    for y in range(0, image.size[1], 1):
        sourcepixel = image.getpixel((x, y))
        image_C.putpixel((x, y),(sourcepixel[0],0,0,0))
        image_M.putpixel((x, y),(0,sourcepixel[1],0,0))
        image_Y.putpixel((x, y),(0,0,sourcepixel[2],0))

#Converts the monotone images into its respective halftones.
image_C = image_C.convert('1')
image_M = image_M.convert('1')
image_Y = image_Y.convert('1')

hf_C = Image.new("CMYK", [dimension for dimension in image_C.size])
hf_M = Image.new("CMYK", [dimension for dimension in image_C.size])
hf_Y = Image.new("CMYK", [dimension for dimension in image_C.size])

for x in range(0, image_C.size[0]):
    for y in range(0, image_C.size[1]):
        pixel_color1 = image_C.getpixel((x, y))
        pixel_color2 = image_M.getpixel((x, y))
        pixel_color3 = image_Y.getpixel((x, y))
        if pixel_color1 == 255:
            hf_C.putpixel((x, y),(255,0,0,0))
        else:
            hf_C.putpixel((x, y),(0,0,0,0))

        if pixel_color2 == 255:
            hf_M.putpixel((x, y),(0,255,0,0))
        else:
            hf_M.putpixel((x, y),(0,0,0,0))

        if pixel_color3 == 255:
            hf_Y.putpixel((x, y),(0,0,255,0))
        else:
            hf_Y.putpixel((x, y),(0,0,0,0))

#Converts the halftone images into respective shares when overlapped should form the actual image.
hf_C = hf_C.convert('CMYK')
hf_M = hf_M.convert('CMYK')
hf_Y = hf_Y.convert('CMYK')

shareC = Image.new("CMYK", [dimension * 2 for dimension in hf_C.size])
shareM = Image.new("CMYK", [dimension * 2 for dimension in hf_M.size])
shareY = Image.new("CMYK", [dimension * 2 for dimension in hf_Y.size])

for x in range(0, hf_C.size[0]):
    for y in range(0, hf_C.size[1]):
        #fill color for shareC
        pixelcolor = hf_C.getpixel((x, y))
        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            shareC.putpixel((x * 2, y * 2), (255,0,0,0))
            shareC.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            shareC.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            shareC.putpixel((x * 2 + 1, y * 2 + 1), (255,0,0,0))
        else:
            shareC.putpixel((x * 2, y * 2), (0,0,0,0))
            shareC.putpixel((x * 2 + 1, y * 2), (255,0,0,0))
            shareC.putpixel((x * 2, y * 2 + 1), (255,0,0,0))
            shareC.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

        #fill color for shareM
        pixelcolor = hf_M.getpixel((x, y))
        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            shareM.putpixel((x * 2, y * 2), (0,255,0,0))
            shareM.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            shareM.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            shareM.putpixel((x * 2 + 1, y * 2 + 1), (0,255,0,0))
        else:
            shareM.putpixel((x * 2, y * 2), (0,0,0,0))
            shareM.putpixel((x * 2 + 1, y * 2), (0,255,0,0))
            shareM.putpixel((x * 2, y * 2 + 1), (0,255,0,0))
            shareM.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

        #fill color for shareY
        pixelcolor = hf_Y.getpixel((x, y))
        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            shareY.putpixel((x * 2, y * 2), (0,0,255,0))
            shareY.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            shareY.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            shareY.putpixel((x * 2 + 1, y * 2 + 1), (0,0,255,0))
        else:
            shareY.putpixel((x * 2, y * 2), (0,0,0,0))
            shareY.putpixel((x * 2 + 1, y * 2), (0,0,255,0))
            shareY.putpixel((x * 2, y * 2 + 1), (0,0,255,0))
            shareY.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

#Export shares after encrytion the color image
shareC.save('shareC.jpg')
shareM.save('shareM.jpg')
shareY.save('shareY.jpg')


