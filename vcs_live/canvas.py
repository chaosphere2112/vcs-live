import vcs
import vtk
import numpy
import cdms2
import json
import tornado.websocket


def parse_plot(msg):
    assert msg["event"] == "plot"
    gm = msg["gm"]
    data = msg["data"]
    tmpl = msg.get("tmpl", None)
    gm_type = gm.keys()[0]
    gm_name = gm[gm_type].keys()[0]
    gm = gm[gm_type][gm_name]
    for k in gm.keys():
        if gm[k] == 100000000000000000000L:
            gm[k] = 1e20
        if isinstance(gm[k], list):
            for i in range(len(gm[k])):
                if gm[k][i] == 100000000000000000000L:
                    gm[k][i] = 1e20
    gm = vcs.loadVCSItem(gm_type, gm_name, gm)
    data = cdms2.open(json.dumps(data))
    return data, gm, tmpl


class CanvasSocketServer(tornado.websocket.WebSocketHandler):
    def open(self):
        self.canvas = vcs.init()
        self.canvas.open()

    def write_canvas(self):
        w, h = self.canvas.backend.renWin.GetSize()
        pixels = vtk.vtkUnsignedCharArray()

        self.canvas.backend.renWin.GetRGBACharPixelData(0, 0, w - 1, h - 1, 1, pixels)
        pixel_arr = numpy.zeros((h, w, pixels.GetNumberOfComponents()), dtype="b")
        for i in range(pixels.GetNumberOfTuples()):
            for j in range(pixels.GetNumberOfComponents()):
                pixel_arr[i / w, i % w, j] = pixels.GetTuple(i)[j]
        flipped = numpy.flipud(pixel_arr)
        self.write_message(flipped.tobytes(), binary=True)

    def on_message(self, message):
        msg = json.loads(message)
        if msg["event"] == "resize":
            self.canvas.geometry(msg["width"], msg["height"])
            self.write_canvas()
        elif msg["event"] == "plot":
            data, gm, tmpl = parse_plot(msg)
            if tmpl:
                self.canvas.plot(data, gm, tmpl)
            else:
                self.canvas.plot(data, gm)
            print self.canvas.canvasinfo()
            self.write_canvas()

    def on_close(self):
        self.canvas.close()
