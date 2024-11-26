import img2pdf

# opening from filename
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg'))

# opening from file handle
with open("name.pdf","wb") as f1, open("test.jpg") as f2:
	f1.write(img2pdf.convert(f2))

# opening using pathlib
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(pathlib.Path('test.jpg')))

# using in-memory image data
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert("\x89PNG...")

# multiple inputs (variant 1)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert("test1.jpg", "test2.png"))

# multiple inputs (variant 2)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(["test1.jpg", "test2.png"]))

# convert all files ending in .jpg inside a directory
dirname = "/path/to/images"
imgs = []
for fname in os.listdir(dirname):
	if not fname.endswith(".jpg"):
		continue
	path = os.path.join(dirname, fname)
	if os.path.isdir(path):
		continue
	imgs.append(path)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(imgs))

# convert all files ending in .jpg in a directory and its subdirectories
dirname = "/path/to/images"
imgs = []
for r, _, f in os.walk(dirname):
	for fname in f:
		if not fname.endswith(".jpg"):
			continue
		imgs.append(os.path.join(r, fname))
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(imgs))


# convert all files matching a glob
import glob
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(glob.glob("/path/to/*.jpg")))

# convert all files matching a glob using pathlib.Path
from pathlib import Path
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(*Path("/path").glob("**/*.jpg")))

# ignore invalid rotation values in the input images
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg'), rotation=img2pdf.Rotation.ifvalid)

# writing to file descriptor
with open("name.pdf","wb") as f1, open("test.jpg") as f2:
	img2pdf.convert(f2, outputstream=f1)

# specify paper size (A4)
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))

# use a fixed dpi of 300 instead of reading it from the image
dpix = dpiy = 300
layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))

# create a PDF/A-1b compliant document by passing an ICC profile
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', pdfa="/usr/share/color/icc/sRGB.icc"))