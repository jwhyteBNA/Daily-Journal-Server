import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_entries, get_single_entry
from views import create_entry, delete_entry, update_entry
from views import get_all_moods, get_single_mood, get_entries_by_term

method_mapper = {
    "moods": {
        "single": get_single_mood,
        "all": get_all_moods
    },
    "entries": {
        "single": get_single_entry,
        "all": get_all_entries
    }
}

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def get_all_or_single(self, resource, id):
        """DRY method for all or single."""
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response

    # def do_GET(self):
    # response = None
    # (resource, id) = self.parse_url(self.path)
    # response = self.get_all_or_single(resource, id)
    # self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        """Handles GET requests to the server """
        response = {}
        (resource, id) = self.parse_url(self.path)
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            ( resource, id ) = parsed
            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = { "message": "Oops! That entry doesn't exist." }
                else:
                    self._set_headers(200)
                    response = get_all_entries()
            elif resource == "moods":
                if id is not None:
                    response = get_single_mood(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = { "message": "Oops! That mood doesn't exist." }
                else:
                    self._set_headers(200)
                    response = get_all_moods()
        else:
            (resource, query) = parsed
            if query.get('q') and resource == 'entries':
                self._set_headers(200)
                response = get_entries_by_term(query['q'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, _) = self.parse_url(self.path)

        #Initialize new entry
        new_entry = None
        if resource == "entries":
            required_fields = {
            "entries": ["concept", "entry",  "mood_id", "date"],
            }
            missing_fields = [
                field for field in required_fields[resource] if field not in post_body
            ]
            if not missing_fields:
                self._set_headers(201)
                new_entry = create_entry(post_body)
                self.wfile.write(json.dumps(new_entry).encode())
            else:
                self._set_headers(400)
                message = {"message": "".join(
                    [f"{field} is required" for field in missing_fields]
                )
                }
                self.wfile.write(json.dumps(message).encode())

    def do_DELETE(self):
        """To Delete Items."""
        # Set a 204 response code

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            self._set_headers(204)
            delete_entry(id)
            self.wfile.write("".encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

#Starting point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
