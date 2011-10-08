#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os    
from re import findall
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Last(object):
    def getLibrary(self,username=''):
        total = fetch("http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key=b25b959554ed76058ac220b7b2e0a026&limit=9000&user=%s" % username).content
        return ', '.join(findall(r'<name>(.*?)</name>',total)).decode('utf-8')

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path,()))

class Get(webapp.RequestHandler, Last):
    def post(self):
        if self.request.get('username'):
            out = self.getLibrary(self.request.get('username'))
        else:
            out = '<h1>Введите имя учётной записи на Last.FM</h1>'
        self.response.out.write(out)

application = webapp.WSGIApplication([
                                    ('/', MainPage),
                                    ('/get', Get)],
                                    debug=False
                                    )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()