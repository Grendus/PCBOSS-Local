import tornado.ioloop
import tornado.httpserver
import tornado.web
import os
import Handlers
import SystemRequestHandler

def application():
    handlers=[(r"/", Handlers.MainHandler),
            (r"/Login", Handlers.LoginHandler),
            (r"/ViewHistory",Handlers.ViewHistoryHandler),
            (r"/UploadFile", Handlers.UploadHandler),
            (r"/Index", Handlers.IndexHandler),
            (r"/About", Handlers.AboutHandler),
            (r"/Profile", Handlers.ProfileHandler),
            (r"/Logout", Handlers.LogoutHandler),
            (r"/System", SystemRequestHandler.SystemRequestHandler)]

    settings=dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                debug=True)
    
    return tornado.web.Application(handlers, "", **settings)

def main():
    http_server = tornado.httpserver.HTTPServer(application())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
