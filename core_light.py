import urllib.request, re, time, os
from base64 import b64decode as ops

def get_all_authors():
    with open('authors.txt', 'r') as authors_file: 
        ret = authors_file.readlines() 
        authors_file.close()
        return ret

def dump(authors, sleep_time=2, bformat="epub"):
    reg_ex_interno = r'a href="\/book-n[^>]+>([^<]+)'
    if bformat == "mobi": reg_ex_books = r'>([^\.]+\.mobi)<\/a>'
    elif bformat == "pdf": reg_ex_books = r'>([^\.]+\.pdf)<\/a>'
    else: reg_ex_books = r'>([^\.]+\.epub)<\/a>'
    base_url = "aHR0cHM6Ly9kd25sZy50ZWwvYm9vay1uLw==" #b64 to evoid being triggered by target searches
    

    try:
        for author in authors: 
            try:
                author = author.rstrip()
                new_url = ops(base_url).decode("utf-8") + author + "/"
                print("\nWorking on " + author)

                req = urllib.request.Request(new_url)
                resp = urllib.request.urlopen(req)
                respData = resp.read()
                
                print("Downloaded author page")
                cartella = './d/'+author+'/'
                choice="y"                
                if not os.path.isdir(cartella):
                    os.mkdir(cartella)
                else:
                    choice=input("La cartella esiste già. Vuoi riscaricare questo autore? y/n: ")
                if choice=="y":
                    books = re.findall(reg_ex_interno, str(respData))
                    print("Verranno scaricati:")
                    for b in books:
                        print(b)
                    c=input("Press enter to continue, type 0 to abort: ")
                    if c == '0':
                        break
                    for book in books:
                        if "Directory" not in book:
                            print("Progessing book " + book)
                            url_download_book = new_url + book + "/"
                            req = urllib.request.Request(url_download_book)
                            resp = urllib.request.urlopen(req)
                            respData = resp.read()

                            titles = re.findall(reg_ex_books, str(respData))

                            for title in titles:
                                download_url = url_download_book + title
                                filename = author.replace("-", " ") + " - " + title.replace("-", " ")
                                try:
                                    req = urllib.request.Request(
                                        download_url, 
                                        data=None, 
                                        headers={
                                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                        }
                                    )
                                    definitive_filename = filename.title()
                                    definitive_filename = definitive_filename.replace("Epub", "epub")
                                    
                                    out_file = open(os.path.join(cartella,definitive_filename), 'wb')
                                    with urllib.request.urlopen(download_url) as response:
                                        print("===============================================================")
                                        print("Downloading! " + definitive_filename)
                                        print("===============================================================")
                                        data = response.read() # a `bytes` object
                                        out_file.write(data)
                                    print("Sleeping for " + str(sleep_time) + " seconds\n")
                                    time.sleep(sleep_time)
                                except:
                                    print("Something bad happened :/")
                
            except: print("Something Happened, I don't know what and I don't give a fuck about. If u didn't select 'epub', try to do it now")
        print("===============================================================\n\n\n\n\n")
        run()
    except KeyboardInterrupt:
        exit(0)

def search_author(user_input):
    authors = get_all_authors()
    user_input = user_input.replace(" ", "-").lower()
    match = []
    for author in authors:
        if user_input in author: 
            match.append(author)
            break
    
    if len(match)>0: 
        return match
    print("Author is not in the DB")
    input("Press any key to continue")
    return False

def print_logo():
    print("\n██╗     ██╗██████╗ ██████╗ ██╗████████╗███████╗██╗")     
    print("██║     ██║██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝██║")     
    print("██║     ██║██████╔╝██████╔╝██║   ██║   █████╗  ██║")     
    print("██║     ██║██╔══██╗██╔══██╗██║   ██║   ██╔══╝  ██║")     
    print("███████╗██║██████╔╝██║  ██║██║██╗██║   ███████╗███████╗")
    print("╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝╚═╝   ╚══════╝╚══════╝\n\n")
                                                      
def why():
    print("\n===============================================================")
    print("Q. Why attack someone who supports free culture?")
    print("A. This is not free culture, this is piracy. If you republish a book or a movie after 1 year it's free culture, if you do the same after 1 day it's piracy.")
    print("\nOn their website they say that links are provided by hosting provider: WRONG.\nOn their website there are a ton of ads, shortlink and shit like this.\nThey say 'we love free culture'? Ok, let's make culture free again without ads :) (semi cit.)\n===============================================================")
    print("\n===============================================================")
    

def menu2():
    choice = "99"
    while choice == "99":
        choice=input("type \"exit\" to close the app, an author to search in the DB: ")
        if choice == "exit": exit(0)
        else:
            print("===============================================================")
            author = choice
            match = search_author(author)
            
            if match is bool:
                print("===============================================================\nCannot find " + author + " in DB, you spelt it wrong?") 
                choice = 99
            elif match is not False and len(match) > 0:
                print("===============================================================\nAuthor found!\n[1] EPUB\n[2] MOBI\n[3] PDF\n[0] Exit")
                ext = input("Choice format [1-3, default epub] ")
                if ext == "2": bformat = "mobi"
                elif ext == "3": bformat = "pdf"
                elif ext == "0": 
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    run()
                else: bformat = "epub"
                print("===============================================================") 
                dump(authors = match, sleep_time=2, bformat=bformat)
            else: menu2()



def run():
    print_logo()
    why()
    menu2()

