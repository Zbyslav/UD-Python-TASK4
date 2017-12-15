import os
import socket

def dirs_page(address):
  answer = """HTTP/1.0 200 OK\nContent-Type: text/html\n\n"""
  answer += """<!DOCTYPE html>"""
  answer += """<html>\n<head>\n<title>%s</title>\n""" % address
  answer += """</head>\n<body><h1>%s</h1><hr>\n<ul>"""  % address
  format = """<li><a  href="{path}">{name}</a></li>\n"""
  dirs  = []
  files = []
  for name in os.listdir(address):
    name = os.path.join(address, name)
    if os.path.isdir(name):
      dirs.append(name)
    else:
      files.append(name)
  dirs.sort()
  files.sort()
  answer += format.format(name="../", path=os.path.dirname(address))
  for name in dirs: 
    answer += format.format(name=name.split('/')[-1], path=name)
  for name in files: 
    answer += format.format(name=name.split('/')[-1], path=name)
  answer += """</ul>\n</body>\n</html>\n"""

  return answer

def files_page(address):
  answer = """HTTP/1.0 200 OK\nContent-Type: text/html\n\n"""
  with open(address, "r") as file:
    answer += """<!DOCTYPE html>"""
    answer += """<html>\n<head>\n<title>%s</title>\n""" % address
    answer += """</head>\n<body><h1>%s</h1><hr><plaintext>"""  % address
    try:
      for line in file:
        answer += """\n %s """ % line.encode("utf-8")
    except Exception:
      answer = """HTTP/1.0 200 OK\nContent-Type: text/html\n\n"""
      answer += """<!DOCTYPE html>"""
      answer += """<html>\n<head>\n<title>%s</title>\n""" % address
      answer += """</head>\n<body><h1>%s</h1><hr>"""  % address
      answer += """<p>Sorry, this file can not be opened correctly. </p><hr>"""
  return answer

def web_page_code(request, address):
  new_address = request.split()[1]
  if new_address != "/":
    address = new_address

  print(address)
  if os.path.isfile(address):
    answer = files_page(address)
  else:
    answer = dirs_page(address)
  return answer

def root(sock, address):
  while True:
    client_sock, client_addr = sock.accept()

    user_data = client_sock.recv(1024).decode(encoding="utf-8",errors='strict')
    request = user_data.split("\r\n", 1)[0]        
    if request.split()[1].rstrip('/') == "/favicon.ico":
      continue
    print('-' * 10) 
    print('REQUEST:')
    print(request)
    answer = web_page_code(request, address)
    client_sock.send(answer)

def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind((HOST, PORT))
  sock.listen(5)
  address = ROOT

  root(sock, address)
  client_sock.close()


if __name__ == "__main__":
  ROOT = os.getcwd()
  HOST = "localhost"
  PORT = 8000 
  print "Serving on %s:%s ..." % (HOST, PORT)
  print(ROOT)
  main()