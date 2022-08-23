import json
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

HTTP_PORT = 8000  

class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def finish_json(self, data={}):
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(data))

    def get_json(self):
        if not hasattr(self, '_json'):
            self._json = None
            if self.request.headers.get('Content-Type', '').startswith('application/json'):
                self._json = json.loads(self.request.body)
        return self._json

class getMethod(BaseHandler):
    async def get(self):
        print("getMethod")
        Application(backend="uia")
        json_result = {}
        json_result["success"] = True ## Or False
        json_result["Author"] = "CAA"
        return self.finish_json(json_result)

class getMethodWithParameter(BaseHandler):
    async def get(self):
        print("getMethodWithParameter")
        anything = self.get_argument('parameter', None)
        json_result = {}
        json_result["success"] = anything
        json_result["Author"] = "CAA"
        return self.finish_json(json_result)

def make_app():
    urls = [
        (r'^/', getMethod), # localhost:8000
        (r'^/withParameter/$', getMethodWithParameter), # localhost:8000/withParameter/?parameter=$$$
    ]
    print("App is running in localhost with port 8000")
    return Application(urls, debug=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(HTTP_PORT)
    IOLoop.instance().start()