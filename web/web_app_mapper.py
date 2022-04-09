import Queue
import threading
import os
import urllib3

threads = 10

target = "https://www.wonderingschool.org/"
directory = "/home/cs/Documents/map"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.wal("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib3.Request(url)

        try:
            response = urllib3.urlopen(request)
            content = response.read()

            print("[%d] => %s" % (response.code, path))
            response.close()

        except urllib3.HTTPError as error:
            #print("Failed %s" % error.code)
            pass

for i in range(threads):
    print("Spawing thread: %d" % i)
    t = threading.Thread(target=test_remote)
    t.start()