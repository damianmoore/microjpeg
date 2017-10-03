# microjpeg

Often on the web and in apps it is nice to display a blurry placeholder image while the full-size image is being downloaded. You will have seen happen in lots of places - especially on mobile. It gives the user a feel for the content straight away and lets them know they can expect more details to follow.

If we could make thumbnails that have a tiny filesize then they could be included in the API responses without even making a request for them. It turns out that the dimensions of these blurred images can be so small that it is actually the headers in JPEG images that are the largest part (specifically the quantization tables for discrete cosine transformation).

If all of our thumbnails are created with the same process using the same quality settings (quantization table) and no extra optimisation then we can include the JPEG header once in the site/app and then only have to send the small remaining content for the image data.

In my experimentation of resolution and quality I have found **32×32 pixels** and **quality=32** in PIL or ImageMagick (they use the same quantization tables) to be sufficient for my use case (using CSS blur filter). Excluding the headers, my sample of images come to **between 125 and 225 bytes** each. That is a saving of **70–80%** file size compared to the JPEGs that contain the headers.

This project is based on an [idea implemented by Facebook](https://code.facebook.com/posts/991252547593574/the-technology-behind-preview-photos/).


## Usage

1. First create a JPEG image at the quality you want all other thumbnails to use.
2. Extract the quantization table out of this image so we can re-use it.
   `python extract_qtable_from_jpeg.py QTABLE_INPUT.jpg`
3. An identifier for this quantization table will be printed out so you can specify which one you want to use in the next step. The header file will have been generated in the directory `headers`.
4. Generate a microjpeg (arguments are size dimensions and the quantization table identifier).
    `python generate_microjpeg.py -q QTABLE_IDENTIFIER -s 32 INPUT.jpg`
5.  The microjpeg will have been created in the directory `microjpegs`. You should notice that it is a smaller number of bytes than the header. You will not be able to view these microjpegs until you combine them with the header again.
6.  You can combine the microjpeg and it's header using the following command. It is expected that in reality you will do this operation on the client side (e.g. in JavaScript or native code).
    `python generate_jpeg.py -q QTABLE_IDENTIFIER -s 32 microjpegs/INPUT.microjpeg`


## Notes

* You should pick a width/height size that is a multiple of 8 otherwise you will be wasting precious partially used JPEG blocks.
* Experiment with different graphics applications to generate the original quantization table - applications often have completely different sets of quantization tables and can label them however they want (80% in one app is different to 80% in another).
* Gather a set of varying images to test out your dimensions and quality parameters. There is a script `generate_comparison.py` that can help with this by creating a webpage to view many at the same time.


## References

* https://code.facebook.com/posts/991252547593574/the-technology-behind-preview-photos/
* http://milankie.huffmancoding.com/chollowayjpegimagecompression.pdf
* http://www.impulseadventure.com/photo/jpeg-huffman-coding.html
