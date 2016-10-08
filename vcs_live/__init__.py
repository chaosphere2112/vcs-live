import tornado.web
import os
import pkg_resources


class JSHandler(tornado.web.RequestHandler):
    def get(self):
        js_string = pkg_resources.resource_string(__name__, "js/vcs.js")
        self.write(js_string)


def get_application():
    application = tornado.web.Application([
        (r"/vcs\.js", JSHandler)
    ])
    return application
