from wsgiref.simple_server import make_server
from cgi import FieldStorage

html = '''
<html>
    <head>
        <title>Upload file</title>
    </head>
    <body>
        <h1>Upload file</h1>
        <p>
            <form method="post" enctype="multipart/form-data">
                <label>File</label>
                <input type="file" name="myfile">
                <input type="submit" value="Send">
            </form>
        </p>
        <p><!--RESULT--></p>
    </body>
</html>
'''

# Some settings
upload_dir = '/storage/tempfiles/'
website = 'https://example.com/tempfiles/'
port = 8000

i = 0
def app(environ, start_response):
    global i
    response = ''
    
    if environ['REQUEST_METHOD'].upper() == 'POST':
        fs = FieldStorage(fp=environ['wsgi.input'], environ=environ,keep_blank_values=True)['myfile']
        
        if fs.file:
            # Just some temporary name using a counter.
            name = str(i).rjust(3, '0') + '.' + fs.filename.split('.')[1:][0]
            
            open(upload_dir + name, 'wb').write(fs.file.read())
            response = html.replace('<!--RESULT-->', '<a href="' + website + name + '">' + website + name + '</a>')
            
            # Increase counter.
            if i == 999:
                i = 0
            else:
                i += 1
        else:
            response = html.replace('<!--RESULT-->', 'No file.')

    else:
        response = html

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [bytes(response, 'utf-8')]

print('Starting web server.')
httpd = make_server('', port, app)
httpd.serve_forever()
