from PIL import Image

from resizeimage import resizeimage

# Android icon
with open('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-xxxhdpi-icon.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [144, 144])
        cover.save('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-xxhdpi-icon.png', image.format)
        cover2 = resizeimage.resize_cover(image, [96, 96])
        cover2.save('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-xhdpi-icon.png', image.format)
        cover3 = resizeimage.resize_cover(image, [72, 72])
        cover3.save('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-hdpi-icon.png', image.format)
        cover4 = resizeimage.resize_cover(image, [48, 48])
        cover4.save('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-mdpi-icon.png', image.format)
        cover5 = resizeimage.resize_cover(image, [36, 36])
        cover5.save('/home/angel/SomMobilitat/pictures/res/icon/android/drawable-ldpi-icon.png', image.format)

# iOS icon
with open('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-60@3x.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [152, 152])
        cover.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-76@2x.png', image.format)
        cover2 = resizeimage.resize_cover(image, [144, 144])
        cover2.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-72@2x.png', image.format)
        cover3 = resizeimage.resize_cover(image, [120, 120])
        cover3.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-60@2x.png', image.format)
        cover4 = resizeimage.resize_cover(image, [114, 114])
        cover4.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon@2x.png', image.format)
        cover5 = resizeimage.resize_cover(image, [100, 100])
        cover5.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-50@2x.png', image.format)
        cover6 = resizeimage.resize_cover(image, [87, 87])
        cover6.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-small@3x.png', image.format)
        cover7 = resizeimage.resize_cover(image, [80, 80])
        cover7.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-40@2x.png', image.format)
        cover8 = resizeimage.resize_cover(image, [76, 76])
        cover8.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-76.png', image.format)
        cover9 = resizeimage.resize_cover(image, [72, 72])
        cover9.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-72.png', image.format)
        cover10 = resizeimage.resize_cover(image, [60, 60])
        cover10.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-60.png', image.format)
        cover11 = resizeimage.resize_cover(image, [58, 58])
        cover11.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-small@2x.png', image.format)
        cover12 = resizeimage.resize_cover(image, [57, 57])
        cover12.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon.png', image.format)
        cover13 = resizeimage.resize_cover(image, [50, 50])
        cover13.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-50.png', image.format)
        cover14 = resizeimage.resize_cover(image, [40, 40])
        cover14.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-40.png', image.format)
        cover15 = resizeimage.resize_cover(image, [29, 29])
        cover15.save('/home/angel/SomMobilitat/pictures/res/icon/ios/icon-small.png', image.format)

# Android screen
with open('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-xxxhdpi-screen.9.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [962, 1602])
        cover.save('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-xxhdpi-screen.9.png', image.format)
        cover2 = resizeimage.resize_cover(image, [722, 1282])
        cover2.save('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-xhdpi-screen.9.png', image.format)
        cover3 = resizeimage.resize_cover(image, [482, 802])
        cover3.save('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-hdpi-screen.9.png', image.format)
        cover4 = resizeimage.resize_cover(image, [322, 482])
        cover4.save('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-mdpi-screen.9.png', image.format)
        cover5 = resizeimage.resize_cover(image, [242, 322])
        cover5.save('/home/angel/SomMobilitat/pictures/res/screen/android/drawable-port-ldpi-screen.9.png', image.format)
# iOS screen portrait
with open('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-Portrait@2x~ipad.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [768, 1024])
        cover.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-Portrait~ipad.png', image.format)
        cover2 = resizeimage.resize_cover(image, [640, 960])
        cover2.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default@2x~iphone.png', image.format)
        cover3 = resizeimage.resize_cover(image, [320, 480])
        cover3.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default~iphone.png', image.format)

# iOS screen portrait 2
with open('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-736h.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [750, 1334])
        cover.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-667h.png', image.format)
        cover2 = resizeimage.resize_cover(image, [640, 1136])
        cover2.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-568h@2x~iphone.png', image.format)

# iOS screen landscape
with open('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-Landscape@2x~ipad.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [2208, 1242])
        cover.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-Landscape-736h.png', image.format)
        cover2 = resizeimage.resize_cover(image, [1024, 768])
        cover2.save('/home/angel/SomMobilitat/pictures/res/screen/ios/Default-Landscape~ipad.png', image.format)
