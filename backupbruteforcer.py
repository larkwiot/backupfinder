import requests
import time
import progressbar

things = ['conf', 'bak', 'swp', 'txt', 'old', 'tar', 'tar.gz', 'tar.bz2', 'zip', 'inc',
        'asa', 'tgz', 'gz', 'rar', 'java', 'py', 'js', 'pdf', 'doc', 'docx', 'rtf',
        'pl', 'o', 'obj', 'jar', 'inf', 'exe', 'c', 'bat', 'asm', 'awk', 's', 'sh',
        'src', 'log', 'lock', 'jsp', 'aspx', 'dev', 'orig', 'copy', 'tmp', '~', 'backup',
        'copyof', 'copy of', 'snapshot']

print
print '''
=============
[i] Beginning.
============='''

retry = 1
def retrySet():
    global retry
    print '[!] Connection failed and/or invalid!'
    retcho = str(raw_input('[!] Try again? (Y/n) >>> ')).upper()
    if retcho == 'Y' or retcho == "\\n":
        retry == 1
    elif retcho == 'N':
        retry = 0
        print '\n;(\n'
        exit(1)
    else:
        print "[!] Invalid option!"
        print "[i] Trying again on your behalf."
        retry == 1

while retry:
    http = raw_input("[>] Enter the HTTP host >>> ")
    link = raw_input("[>] Enter the directory >>> ")
    fyle = raw_input("[>] Enter the file      >>> ")
    fiex = raw_input("[>] Enter the extension >>> ")
    try:
        session = requests.head(http)
        if session.status_code == 200:
            print "[i] Connection is working."
            things.append(fiex)
            retry = 0
        else:
            print "[!] Connection made, code not 200!"
            retrySet()
    except requests.exceptions.RequestException:
        retrySet()
            
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

widgets = ['[1/4] Appending |', progressbar.Percentage(), '| ', progressbar.AdaptiveETA()]

print '''
=============
[i] Testing.
============='''
pbar = progressbar.ProgressBar(widgets=widgets)
for ext in pbar(things):
    req = http + link + fyle + "." + fiex + "." + ext
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.001)
    else:
        continue

widgets[0] = '[2/4] Replacing |'
pbar = progressbar.ProgressBar(widgets=widgets)
for repl in pbar(things):
    req = http + link + fyle + "." + repl
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.001)
    else:
        continue

widgets[0] = '[3/4] Prepending |'
pbar = progressbar.ProgressBar(widgets=widgets)
for pre in pbar(things):
    req = http + link + pre + fyle + "." + fiex
    if checkreq(req):
        connection = requests.head(req)
        store(req, connection.status_code, req)
        time.sleep(0.001)
    else:
        continue

widgets[0] = '[4/4] Mixing |'
pbar = progressbar.ProgressBar(widgets=widgets)
for exten in pbar(range(0, len(things))):
    for main in things:
        req = http + link + main + fyle + fiex + "." + things[exten]
        if checkreq(req):
            connection = requests.head(req)
            store(req, connection.status_code, req)
            time.sleep(0.001)
        else:
            continue

print "============="
print "[i] Results."
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
print '''
=============
[*] Done.
============='''
print
exit(0)
