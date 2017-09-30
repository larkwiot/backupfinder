import requests, time
from multiprocessing import Process, Manager

def findchar(enteredString, searchString, occurence):
    ecx = 1
    place = 1
    for iter in range(0, len(enteredString)):
        if enteredString[iter:len(searchString) + iter:] == searchString and ecx == occurence:
            return iter
            break
        elif enteredString[iter:len(searchString) + iter:] == searchString and ecx != occurence:
            ecx += 1
            continue
        place += 1

# 0 = http, 1 = link, 2 = fyle, 3 = fiex
conns = []

def obtain():
    enteredURL = str(raw_input("[>] Enter the URL >>> "))
    http = enteredURL[:findchar(enteredURL, '/', 3):]
    link = ''
    for linker in range(len(enteredURL)-1, 0, -1):
        if enteredURL[linker] == '/':
            link = enteredURL[findchar(enteredURL, '/', 3):linker+1:]
            break
        else:
            continue
    fyle = enteredURL[findchar(enteredURL, link, 1)+len(link):findchar(enteredURL, '.', 3):]
    fiex = enteredURL[findchar(enteredURL, fyle, 1)+len(fyle)+1::]
    print '[?] We received ::: ' + http + link + fyle + '.' + fiex
    correction = str(raw_input('[?] Is this correct? (Y/n) >>> '))
    if correction == 'n':
        return False
    else:
        try:
            session = requests.head(http+link+fyle+'.'+fiex)
            if session.status_code == 200:
                print "[i] Connection to " + http + " successful."
                global conns
                conns.append([http, link, fyle, fiex])
                return True
            else:
                print "[!] Error, connection made, code not 200!"
                return False
        except requests.exceptions.RequestException:
            return False

def attempt(http, link, fyle, fiex, iam, urls):
    things = ['conf', 'bak', 'swp', 'txt', 'old', 'tar', 'tar.gz', 'tar.bz2', 'zip', 'inc',
              'asa', 'tgz', 'gz', 'rar', 'java', 'py', 'js', 'pdf', 'doc', 'docx', 'rtf',
              'pl', 'o', 'obj', 'jar', 'inf', 'exe', 'c', 'bat', 'asm', 'awk', 's', 'sh',
              'src', 'log', 'lock', 'jsp', 'aspx', 'dev', 'orig', 'copy', 'tmp', '~', 'backup',
              'copyof', 'copy of', 'snapshot', fiex]

    print iam + ' ::: Attempt method [1/4]'
    for ext in things:
        req = http + link + fyle + "." + fiex + "." + ext
        connection = requests.head(req)
        urls.append(req)
        urls.append(connection.status_code)
        time.sleep(0.001)
    
    print iam + ' ::: Attempt method [2/4]'
    for repl in things:
        req = http + link + fyle + "." + repl
        connection = requests.head(req)
        urls.append(req)
        urls.append(connection.status_code)
        time.sleep(0.001)

    print iam + ' ::: Attempt method [3/4]'
    for pre in things:
        req = http + link + pre + fyle + "." + fiex
        connection = requests.head(req)
        urls.append(req)
        urls.append(connection.status_code)
        time.sleep(0.001)

    print iam + ' ::: Attempt method [4/4]'
    for exten in range(0, len(things)):
        for main in things:
            req = http + link + main + fyle + fiex + "." + things[exten]
            connection = requests.head(req)
            urls.append(req)
            urls.append(connection.status_code)
            time.sleep(0.001)
    print iam + ' ::: Done.'

if __name__ == '__main__':
    print "\n=============\n[i] Beginning.\n============="

    atmp = int(raw_input("[>] Enter No. of files  >>> "))
    while atmp != 0:
        if obtain():
            atmp -= 1
            continue

    manager = Manager()
    urls = manager.list()

    ecx = 0
    jobs = []
    for argz in conns:
        procName = 'Process -> #' + str(ecx)
        p = Process(target=attempt, args=(argz[0], argz[1], argz[2], argz[3], procName, urls))
        jobs.append(p)
        p.start()
        ecx += 1
    time.sleep(5)
    for close in jobs:
        close.join()
    print "=============\n[i] Results."
    c200s = 0
    for search in range(0, len(urls)):
        if not isinstance(urls[search], basestring) and urls[search] != 404:
            c200s += 1
            print "============="
            print "[" + str(c200s) + "] URL ::: " + urls[search-1].replace("\n", "").replace("\r", "")
            print "|__ COD ::: " + str(urls[search])
    print "============="
    print "[i] " + str(c200s) + " URLs found."
    print "[i] " + str(len(urls)/2) + " URLs attempted."
    print "=============\n[*] Done.\n=============\n"
    exit(0)
