import tornado.web
import pkg_resources


class JSHandler(tornado.web.RequestHandler):
    def get(self):
        js_string = pkg_resources.resource_string(__name__, "js/vcs.js")
        self.write(js_string)


class SamplePage(tornado.web.RequestHandler):
    def get(self):
        html = pkg_resources.resource_string(__name__, "html/sample.html")
        self.write(html)


def get_application():
    application = tornado.web.Application([
        (r"/vcs\.js", JSHandler),
        (r"/sample", SamplePage),
    ])
    return application
