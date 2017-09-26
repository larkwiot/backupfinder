import requests, time, progressbar

things = ['conf', 'bak', 'swp', 'txt', 'old', 'tar', 'tar.gz', 'tar.bz2', 'zip', 'inc',
        'asa', 'tgz', 'gz', 'rar', 'java', 'py', 'js', 'pdf', 'doc', 'docx', 'rtf',
        'pl', 'o', 'obj', 'jar', 'inf', 'exe', 'c', 'bat', 'asm', 'awk', 's', 'sh',
        'src', 'log', 'lock', 'jsp', 'aspx', 'dev', 'orig', 'copy', 'tmp', '~', 'backup',
        'copyof', 'copy of', 'snapshot']

print
print "=============\n[i] Beginning.\n============="

urls = []
codes = []
direct = []

conns = []

retry = 1
def main():
    # 0 = http, 1 = link, 2 = fyle, 3 = fiex
    atmp = int(raw_input("[>] Enter No. of files  >>> "))
    global retry
    while retry:
        if atmp == 1:
            obtain()
            attempt(*conns[0])
        else:
            for conn in range(1, atmp+1):
                obtain()
            for conn2 in conns:
                print "[1/" + str(len(conns)+1) + "] Attempting " + conn2[0] + conn2[1] + conn2[2] + '.' + conn2[3]
                attempt(*conn2)

def obtain():
    global retry
    http = str(raw_input("[>] Enter the HTTP host >>> "))
    link = str(raw_input("[>] Enter the directory >>> "))
    fyle = str(raw_input("[>] Enter the file      >>> "))
    fiex = str(raw_input("[>] Enter the extension >>> "))
    try:
        session = requests.head(http)
        if session.status_code == 200:
            print "[i] Connection to " + http + " successful."
            things.append(fiex)
            retry = 0
            conns.append([http, link, fyle, fiex])
        else:
            print "[!] Error, connection made, code not 200!"
            if retrySet():
                obtain()
            else:
                print "1111111"
    except requests.exceptions.RequestException:
        if retrySet():
            obtain()
        else:
            print "222222222"

def retrySet():
    global retry
    print '[!] Connection failed and/or invalid!'
    retcho = str(raw_input('[!] Try again? (Y/n) >>> ')).upper()
    if retcho == 'N':
        retry = 0
        print '\n;(\n'
        exit(1)
    else:
        return True

def store(request, code, directlink):
        urls.append(request)
        codes.append(code)
        direct.append(directlink)

def checkreq(request):
        if request in direct:
            return False
        else:
            return True

def attempt(http, link, fyle, fiex):
    widgets = ['[1/4] Appending |', progressbar.Percentage(), '| ', progressbar.AdaptiveETA()]

    print "=============\n[i] Testing.\n============="
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
    print "=============\n[*] Done.\n============="
    print

main()

exit(0)
