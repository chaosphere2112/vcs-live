import tornado.web
import pkg_resources
import canvas


class JSHandler(tornado.web.RequestHandler):
    def get(self):
        js_string = pkg_resources.resource_string(__name__, "js/vcs.js")
        js_string = js_string.replace("@@@SERVER@@@", "%s" % (self.request.host))
        self.write(js_string)


class SamplePage(tornado.web.RequestHandler):
    def get(self):
        html = pkg_resources.resource_string(__name__, "html/sample.html")
        self.write(html)


def get_application():
    application = tornado.web.Application([
        (r"/vcs\.js", JSHandler),
        (r"/sample", SamplePage),
        (r"/canvas", canvas.CanvasSocketServer)
    ])
    return application
