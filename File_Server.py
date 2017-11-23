import web
import os

urls = (
    '/(.*)','hello'
)

class hello:
    def GET(self, File_name):
        if not File_name:
            File_size = 'No file name given'
            return File_size
        else:
            File_size = os.path.getsize(File_name)
            return File_size


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()