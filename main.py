#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from re import findall
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

http_client = tornado.httpclient.HTTPClient()

class Last(object):
    def getLibrary(self, username=''):
        total = http_client.fetch("http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key=b25b959554ed76058ac220b7b2e0a026&limit=9000&user=%s" % username).body
        return ', '.join(findall(r'<name>(.*?)</name>',total)).decode('utf-8')
                                    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler, Last):

    def get(self):
        self.render("index.html")

    def post(self):
    	username = self.get_argument('username')
        if username:
            out = self.getLibrary(username)
        else:
            out = '<h1>Введите имя учётной записи на Last.FM</h1>'
        self.write(out)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()