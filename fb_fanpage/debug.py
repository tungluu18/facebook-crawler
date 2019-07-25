from datetime import datetime

def write_html_byte(response, filename="output_{}.html".format(datetime.now())):
    with open(filename, "wb") as f:
        f.write(response.body)
