#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Manish Singh

#   Gimp-Python - allows the writing of Gimp plugins in Python.
#   Copyright (C) 2003, 2005  Manish Singh <yosh@gimp.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# (c) 2003 Manish Singh.
# Modified by Mo Nianliang (2014)

import os

from gimpfu import *
import os.path

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)


def pyslice(image, drawable, save_path, image_basename,
            flip_vertical, image_extension, separate, image_path):

    vert, horz = get_guides(image)

    if len(vert) == 0 and len(horz) == 0:
        return

    gimp.progress_init(_("Cubemap_slice"))
    progress_increment = 1 / ((len(horz) + 1) * (len(vert) + 1))
    progress = 0.0

    def check_path(path):
        path = os.path.abspath(path)

        if not os.path.exists(path):
            os.mkdir(path)

        return path

    save_path = check_path(save_path)

    if not os.path.isdir(save_path):
        save_path = os.path.dirname(save_path)

    if separate:
        image_relative_path = image_path
        if not image_relative_path.endswith("/"):
            image_relative_path += "/"
        image_path = check_path(os.path.join(save_path, image_path))
    else:
        image_relative_path = ''
        image_path = save_path

    top = 0

    for i in range(0, len(horz) + 1):
        if i == len(horz):
            bottom = image.height
        else:
            bottom = image.get_guide_position(horz[i])

        left = 0

        for j in range(0, len(vert) + 1):
            if j == len(vert):
                right = image.width
            else:
                right = image.get_guide_position(vert[j])

            slice(image, None, image_path,
                    image_basename, image_extension,
                    left, right, top, bottom, i, flip_vertical)

            left = right

            progress += progress_increment
            gimp.progress_update(progress)

        top = bottom


def slice(image, drawable, image_path, image_basename, image_extension,
          left, right, top, bottom, i, flip_vertical):
    src = "%s_%d.%s" % (image_basename, i, image_extension)
    filename = os.path.join(image_path, src)

    if not drawable:
        temp_image = image.duplicate()
        temp_drawable = temp_image.active_layer
    else:
        if image.base_type == INDEXED:
            # gimp_layer_new_from_drawable doesn't work for indexed images.
            # (no colormap on new images)
            original_active = image.active_layer
            image.active_layer = drawable
            temp_image = image.duplicate()
            temp_drawable = temp_image.active_layer
            image.active_layer = original_active
            temp_image.disable_undo()
            # remove all layers but the intended one
            while len(temp_image.layers) > 1:
                if temp_image.layers[0] != temp_drawable:
                    pdb.gimp_image_remove_layer(temp_image, temp_image.layers[0])
                else:
                    pdb.gimp_image_remove_layer(temp_image, temp_image.layers[1])
        else:
            temp_image = pdb.gimp_image_new(drawable.width, drawable.height,
                                         image.base_type)
            temp_drawable = pdb.gimp_layer_new_from_drawable(drawable, temp_image)
            temp_image.insert_layer(temp_drawable)

    temp_image.disable_undo()
    temp_image.crop(right - left, bottom - top, left, top)
    if image_extension == "jpg" and image.base_type == INDEXED:
        pdb.gimp_image_convert_rgb(temp_image)

    # flip image vertical
    if flip_vertical:
        pdb.gimp_image_flip(temp_image, ORIENTATION_VERTICAL)

    pdb.gimp_file_save(temp_image, temp_drawable, filename, filename)

    gimp.delete(temp_image)
    return src


def get_guides(image):
    hguides = []

    for p in [i for i in range(image.width, image.height, image.width)]:
        guide = pdb.gimp_image_add_hguide(image, p)
        hguides.append(guide)

    return [], hguides


register(
    "python-fu-cubemap-slice",
    # table snippet means a small piece of HTML code here
    N_("Cuts an image of cubemap into 6 images for OpenGL ES app."),
    """Automaticly add 5 horizontal guides to an image. Then cut along the
    guides, and give you the resulting images flipped vertically by default.
    It's based on python-fu-slice by Manish Singh.""",
    "Mo Nianliang",
    "Manish Singh",
    "2014",
    _("_Cubemap Slice..."),
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_DIRNAME, "save-path",     _("Path for HTML export"), os.getcwd()),
        (PF_STRING, "image-basename", _("Image name prefix"),    "cubemap"),
        (PF_TOGGLE, "flip-vertical",  _("Flip image vertically"), True),
        (PF_RADIO, "image-extension", _("Image format"), "png", (("png", "png"), ("jpg", "jpg"))),
        (PF_TOGGLE, "separate-image-dir",  _("Separate image folder"), False),
        (PF_STRING, "relative-image-path", _("Folder for image export"), "images"),
    ],
    [],
    pyslice,
    menu="<Image>/Filters/Web",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
