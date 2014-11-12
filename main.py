import webapp2, os, cgi, datetime, sys, time, logging, json

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		self.response.write("HELLO DARZIE")

application = webapp2.WSGIApplication([
	('/', MainPage)
])
