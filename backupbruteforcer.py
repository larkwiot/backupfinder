import requests
import time
from progressbar import ProgressBar

things = ['conf', 'bak', 'swp', 'txt', 'old', 'tar', 'tar.gz', 'tar.bz2', 'zip', 'inc',
        'asa', 'tgz', 'gz', 'rar', 'java', 'py', 'js', 'pdf', 'doc', 'docx', 'rtf',
        'pl', 'o', 'obj', 'jar', 'inf', 'exe', 'c', 'bat', 'asm', 'awk', 's', 'sh',
        'src', 'log', 'lock', 'jsp', 'aspx', 'dev', 'orig', 'copy', 'tmp', '~', 'backup',
        'copyof', 'copy of', 'snapshot']

print
print "============="
print "[i] Beginning..."
print "============="

http = raw_input("[>] Enter the HTTP host >>> ")
link = raw_input("[>] Enter the directory >>> ")
file = raw_input("[>] Enter the file      >>> ")
fiex = raw_input("[>] Enter the extension >>> ")
things.append(fiex)

session = requests.head(http)
if session.status_code == 200:
    print "[i] Connection is working."
else:
    print "[!] Connection does not work!"
    print "============="
    exit(1)

urls = []
codes = []
direct = []

def store(request, code, directlink):
    urls.append(request)
    codes.append(code)
    direct.append(directlink)

def checkreq(request):
    if request in direct:
        return False
    else:
        return True

print "============="
print "=== Appending ==="
pbar = ProgressBar()
for ext in pbar(things):
    req = http + link + file + "." + fiex + "." + ext
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.05)
    else:
        continue

print "=== Replacing ==="
pbar = ProgressBar()
for repl in pbar(things):
    req = http + link + file + "." + repl
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.05)
    else:
        continue

print "=== Prepending ==="
pbar = ProgressBar()
for pre in pbar(things):
    req = http + link + pre + file + "." + fiex
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.05)
    else:
        continue

print "=== Mixing ==="
pbar = ProgressBar()
for exten in pbar(range(0, len(things))):
    for main in things:
        req = http + link + main + file + fiex + "." + things[exten]
        if checkreq(req):
            connection = requests.head(req)
            store(req, connection.status_code, req)
            time.sleep(0.05)
        else:
            continue

c200s = 0
for search in range(0, len(codes)):
    if codes[search] != 404:
        c200s += 1
        print "============="
        print "[" + str(c200s) + "] URL ::: " + urls[search].replace("\n", "").replace("\r", "")
        print "|__ COD ::: " + str(codes[search])

print "============="
print "[i] " + str(c200s) + " URLs found."
print "[i] " + str(len(codes)) + " URLs attempted."
print "============="
print "[*] Done."
print "============="
print
exit(0)
