import shutil
import os, sys, re
from PIL import Image
import numpy as np
import tempfile

def render_pdf(filename, imagemagick_convert_path, dpi=150):
    output_dpi = str(dpi)
    """
        This function renders the document unsing imagemagick and returns a list of images, one for each page.
        The images are PIL Image type.
    """
    sep = os.path.sep    
    outputDir = tempfile.mkdtemp()

    rasterScale = 3  # increase this if you want higher resolution images  # added by Huhu
    rasterDensity = str(rasterScale * 100)  # added by Huhu

    # If you have your path setup correctly in 'nix this should work,
    # right now its set up to have explicit path in windows
    if os.name == 'nt':
        imagemagickPath = imagemagick_convert_path
        # imagemagickPath = 'C:\Users\zzzheng\SOFTWARE\others\ImageMagick-7.0.3-5-portable-Q16-x86\convert.exe'
        os.system(
            imagemagickPath + ' -density ' + rasterDensity + ' -resample ' + output_dpi + ' -set colorspace RGB ' +
            filename + ' ' + os.path.join(outputDir, 'image.png'))
    else:
        os.system('gs -q -sDEVICE=png16m -o ' + os.path.join(outputDir, 'file-%02d.png') + ' -r' + output_dpi + ' ' + filename)

    files = [f for f in os.listdir(outputDir) if os.path.isfile(os.path.join(outputDir, f)) and not f.startswith('.')]
    files = natural_sort(files)
    images = []
    for f in files:
        if f.endswith('.png'):
            pageIm = Image.open(os.path.join(outputDir, f)).convert('RGB')
            pageIm.load()  # load into memory (also closes the file associated)
            images.append(pageIm)
    shutil.rmtree(outputDir)
    return images


def natural_sort(l): # this is taken from stack overflow.
    """
        This function will sort strings with numeric values in natural ascending order, 
        such that it does not go 1,11,2 etc.
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
