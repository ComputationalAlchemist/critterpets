import webapp2, os, cgi, datetime, sys, time, logging, json, StringIO
import colorsys
from PIL import Image
from google.appengine.ext import ndb

class ImageBlock(ndb.Model):
	color = ndb.StringProperty(required=True, indexed=True)
	contents = ndb.BlobProperty(required=True)

def recolor(im, r, g, b):
	result = im.copy()
	pix = result.load()
	for y in range(result.size[1]):
		for x in range(result.size[0]):
			r2, g2, b2, a = pix[x, y]
			if a != 0:
				pix[x, y] = (r, g, b, a)
	return result

basecolor = Image.open("basecolor.png").resize((320, 320))

def get_recolored(r, g, b):
	color = "%.2x/%.2x/%.2x" % (r, g, b)
	found = ImageBlock.query().filter(ImageBlock.color == color).get()
	if found != None:
		return found.contents
	sout = StringIO.StringIO()
	out = recolor(basecolor, r, g, b)
	out.save(sout, "png")
	sgot = sout.getvalue()
	sout.close()
	created = ImageBlock(color=color, contents=sgot)
	created.put()
	return sgot

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/html"
		self.response.write("""<!DOCTYPE html>
<html lang="en">
<head>
<title>CritterPets</title>
</head>
<body>
<h1>Input Settings</h1>
<input id="red" value="0" />
<input id="green" value="0" />
<input id="blue" value="0" />
<br>
<img id="image" src="/image" />
<script type="text/javascript">
var old = "", image = document.getElementById("image"), red = document.getElementById("red"), green = document.getElementById("green"), blue = document.getElementById("blue");
function update() {
	var r = parseInt(red.value), g = parseInt(green.value), b = parseInt(blue.value);
	if (!isNaN(r) && !isNaN(g) && !isNaN(b)) {
		var nurl = "/image?r=" + r + "&g=" + g + "&b=" + b;
		if (nurl != old) {
			image.src = old = nurl;
		}
	}
}
setInterval(update, 500);
</script>
</body>
</html>
""")
class ImagePage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "image/png"
		r = int(self.request.get("r", 0))
		g = int(self.request.get("g", 255))
		b = int(self.request.get("b", 0))
		r = min(255, max(0, r))
		g = min(255, max(0, g))
		b = min(255, max(0, b))
		self.response.write(get_recolored(r, g, b))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/image', ImagePage)
])
