from PIL import Image
import sys

#Import shares 
shareC = Image.open("shareC.jpg")
shareM = Image.open("shareM.jpg")
shareY = Image.open("shareY.jpg")

#Create the frame for the final image
final_image = Image.new('CMYK', shareC.size)

#Merges the 3 shares formed to collect the image after decryption
for x in range(0,shareC.size[0],2):
    for y in range(0,shareC.size[1],2):
        C = shareC.getpixel((x+1, y))[0]
        M = shareM.getpixel((x+1, y))[1]
        Y = shareY.getpixel((x+1, y))[2]

        final_image.putpixel((x, y), (C,M,Y,0))
        final_image.putpixel((x+1, y), (C,M,Y,0))
        final_image.putpixel((x, y+1), (C,M,Y,0))
        final_image.putpixel((x+1, y+1), (C,M,Y,0))

#Export the image after decrytion 3 shares
final_image = final_image.resize((850, 567))
final_image.save("final.jpg")

#Show the base image and final image
base_image = Image.open("color_image.jpg")

def get_concat_h(im1, im2):
    dst = Image.new('CMYK', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
    
before_after = get_concat_h(base_image, final_image)
before_after.save('before_after.jpg')
before_after.show()



