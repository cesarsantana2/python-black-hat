import queue
import threading
import urllib.error
import urllib.parse
import urllib.request

threads = 50
target_url = ""
wordlist_file = "all.txt" #de SVNDigger
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0 Gecko/20100101 Firefox/19.0"


def build_wordlist(wordlist_file):
    
    #Lê a lista de palavras
    fd = open(wordlist_file, "r")
    raw_words = [line.rstrip('\n') for line in fd]
    fd.close()

    found_resume = False
    words = queue.Queue()

    for word in raw_words:
    
        if resume:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % resume)
        else:
            words.put(word)

    return words


def dir_bruter(word_queue, extensions=None):

    while not word_queue.empty():
        
        attempt = word_queue.get()

        attempt_list = []

        # verifica se há uma extensão de arquivo; se não houver,
        # é um path de diretório que estamos verificando com base na força bruta
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)
        
        # se quisermos usar a força bruta em extensões
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt,extension))

        # faz a iteração pela nossa lista de tentativas
        for brute in attempt_list:

            url = "%s%s" % (target_url, urllib.quote(brute))

            try:
                headers = {}
                headers = {"User-Agent" : user_agent}
                r = urllib.request.Request(url, headers=headers)

                response = urllib.request.urlopen(r)

                if len(response.read()):
                    print("[%d] => %s" % (response.code,url))

            except urllib.error.HTTPError as e:
                if e.code !=404:
                    print("!!! %d => %s" % (e.code, url))
                pass


word_queue = build_wordlist(wordlist_file)
file_extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(file_extensions,))
    t.start()
