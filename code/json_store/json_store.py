#!/bin/env python

import sys
import json
import urlparse


def get_json_subpart(path, data):
    subpart = data

    for x in path:
        try:
            subpart = subpart[x]
        except KeyError:
            subpart = None
        except TypeError:
            try:
                x = int(x)
            except ValueError:
                subpart = None
            else:
                try:
                    subpart = subpart[x]
                except IndexError:
                    subpart = None

    return subpart


def get_data():
    try:
        with open('store.json', 'rw') as f:
            data = f.read()
        return json.loads(data)
    except (IOError):
        with open('store.json', 'w') as f: pass

        return {}


def update_json(path, data, new_data):
    if path:
        subpath = path[:len(path) - 1]
        subpart = get_json_subpart(subpath, data)

        if subpart is not None:
            key = path[-1]
            try:
                subpart[key] = new_data
            except TypeError as e:
                try:
                    subpart[int(key)] = new_data
                except ValueError:
                    print path, key, subpart, new_data, subpath
                    raise e

    else:
        return new_data

    return data


def app(env, start_response):
    """ hello world app as defined above """
    status = "200 OK"
    headers = [("content-type", "application/json")]

    path = [x for x in env['PATH_INFO'].split('/') if x]

    data = get_data()
    subpart = get_json_subpart(path, data)
    content = []

    if env['REQUEST_METHOD'] == 'PUT':
        # read request body
        try:
            req_body_size = int(env.get('CONTENT_LENGTH', 0))
        except ValueError:
            req_body_size = 0
        req_body = env['wsgi.input'].read(req_body_size)

        new_data = json.loads(req_body)

        data = update_json(path, data, new_data)
        content.append(json.dumps(data, indent=2))
    else:
        if subpart is None:
            status = "404 Not Found"

        content.append(json.dumps(subpart))

    with open('store.json', 'w') as f:
        f.write(json.dumps(data))

    start_response(status, headers)
    return content

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 9000, app)
    print "Serving on port 9000..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down server."
