# microjpeg

Based on https://code.facebook.com/posts/991252547593574/the-technology-behind-preview-photos/


We want to identify the DCT part of the JPEG so we can keep it separate from our encoded output.

jpegtran or libjpeg may be able to identify where we need to split.

JPEGS are split into 8x8 pixel blocks and each of these has the DCT applied.


Probably don't want optimisation as this adapts the huffman table to each image based on statistical frequency and doesn't give much of a decrease in file size

All EXIF data removed for comparison with
  exiftool -all= 1px.jpg

As an initial comparison between similar images I'm using dhex (hex viewer) and meld (diff tool)



Making the images all the same size means all headers will match across files and also it's most efficient to choose a dimension that's divisible by 8 so we're using 40x40.
Export all images at the same quality with no optimisation or progressiveness so same DCT is used. In the test I used 10% quality in GIMP.
Remove all EXIF data with exiftool
Diff the files and you should see the first parts of the file are the same
In my testing the 2 images were originally 755 and 792 bytes. They shared the first 604 bytes so would only need 151 and 188 bytes to store each.


References:
milankie.huffmancoding.com/chollowayjpegimagecompression.pdf
http://www.impulseadventure.com/photo/jpeg-huffman-coding.html
