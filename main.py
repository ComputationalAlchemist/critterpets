import webapp2, os, cgi, datetime, sys, time, logging, json
import colorsys
print sys.modules
from PIL import Image

def recolor(im, r, g, b):
	h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
	result = im.copy()
	pix = result.load()
	for y in range(result.size[1]):
		for x in range(result.size[0]):
			r2, g2, b2, a = pix[x, y]
			h2, l2, s2 = colorsys.rgb_to_hls(r2/255.0, g2/255.0, b2/255.0)
			r3, g3, b3 = colorsys.hls_to_rgb(h, l2, s)
			pix[x, y] = (int(r3*255.99), int(g3*255.99), int(b3*255.99), a)
	return result

basecolor = Image.open("basecolor.png").resize((320, 320))

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
		recolor(basecolor, r, g, b).save(self.response, "png")

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/image', ImagePage)
])
