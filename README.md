## Cubemap Slice Plug-ins

Cubemap Slice is a GIMP python plug-ins, it cuts an image of cubemap into 6 images for OpenGL ES app.

It works by automaticly adding 5 horizontal guides to an image, then cut along the guides, and give you the resulting images flipped vertically by default.

It's based on python-fu-slice by Manish Singh.

## How to use it?

Click GIMP menu Preferences > Folders > Plug-ins to find location of plug-ins on your system. You'll see one is the system location, another is your personal plug-ins folder.

On Mac OSX it's `~/Library/Application Support/GIMP/2.8/plug-ins/`

Download [cubemap-slice.py](https://github.com/kitnew/gimp-cubemap-slice/raw/master/com.appbead.cubemap-slice.py).

Copy it to GIMP plug-ins folder:

    cp com.appbead.cubemap-slice.py ~/Library/Application\ Support/GIMP/2.8/plug-ins/

or link it:

    ln -sf /full/path/to/com.appbead.cubemap-slice.py ~/Library/Application\ Support/GIMP/2.8/plug-ins/

Don't forget to make it executable:

    chmod +x ~/Library/Application\ Support/GIMP/2.8/plug-ins/com.appbead.cubemap-slice.py

Then restart GIMP, you see it at [Menu] Filters > Web > Cubemap Slice...
