def hello_world(environment, start_response):
    """ hello world app as defined above """
    status = "200 OK"
    headers = [("content-type", "text/plain")]
    content = ["Hello world!\n", "How are you today?\n"]

    start_response(status, headers)
    return content

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, hello_world)
    print "Serving on port 8000..."
    httpd.serve_forever()
