import urllib.request, re, time, os
from base64 import b64decode as ops

def get_all_authors():
    with open('authors.txt', 'r') as authors_file: 
        return authors_file.readlines() 

def dump(authors, sleep_time=2, bformat="epub"):
    reg_ex_interno = r'a href="\/book-n[^>]+>([^<]+)'
    if bformat == "mobi": reg_ex_books = r'>([^\.]+\.mobi)<\/a>'
    elif bformat == "pdf": reg_ex_books = r'>([^\.]+\.pdf)<\/a>'
    elif bformat == "epub": reg_ex_books = r'>([^\.]+\.epub)<\/a>'
    else: reg_ex_books = r'>([^\.]+\.[epub|pdf|mobi]+)<\/a>'
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
                author_folder = os.path.join(".", "download", author.title().replace("-", " "))
                if not os.path.isdir(author_folder): os.makedirs(author_folder)

                books = re.findall(reg_ex_interno, str(respData))
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
                                definitive_filename = definitive_filename.replace("Epub", "epub").replace("Pdf", "pdf").replace(".Mobi", ".mobi")
                                print("************\n"+definitive_filename+"\n**********")
                                out_file = open(os.path.join(author_folder, definitive_filename), 'wb')
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
            except: print("Something Happened, I don't know what and I don't give a fuck about.")
        print("===============================================================\nMy job here is done! Bye bye!")
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
    if match: return match
    else: return False


def print_logo():
    print("\n██╗     ██╗██████╗ ██████╗ ██╗████████╗███████╗██╗")     
    print("██║     ██║██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝██║")     
    print("██║     ██║██████╔╝██████╔╝██║   ██║   █████╗  ██║")     
    print("██║     ██║██╔══██╗██╔══██╗██║   ██║   ██╔══╝  ██║")     
    print("███████╗██║██████╔╝██║  ██║██║██╗██║   ███████╗███████╗")
    print("╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝╚═╝   ╚══════╝╚══════╝\nYou just fucked with the wrong person.\n")
                                                      
def why():
    print("\n===============================================================")
    print("Q. Why this?")
    print("A. They fucked with the wrong person.")
    print("Q. Why attack someone who supports free culture?")
    print("A. This is not free culture, this is piracy. If you republish a book or a movie after 1 year it's free culture, if you do the same after 1 day it's piracy.")
    print("\nOn their website they say that links are provided by hosting provider: WRONG.\nOn their website there are a ton of ads, shortlink and shit like this.\nThey say 'we love free culture'? Ok, let's make culture free again without ads :) (semi cit.)\n===============================================================")
    k = input("Press enter to go back ")
    print_logo()
    menu()

def menu():
    choice = "99"
    while choice == "99":
        print("[1] Download specific author.")
        print("[2] Download entire DB.")
        print("[3] Why this?")
        print("[0] Exit.")
        choice = input("Please make a choice: ")
        if choice == "1": 
            print("===============================================================")
            author = input("Insert author name [ex. Dante Aligheri or Dante] ")
            match = search_author(author)
            if match:
                print("===============================================================\nAuthor found!\n[1] EPUB\n[2] MOBI\n[3] PDF\n[0] Exit")
                ext = input("Choice format [1-3, default epub] ")
                if ext == "2": bformat = "mobi"
                elif ext == "3": bformat = "pdf"
                elif ext == "0": exit(0)
                else: bformat = "epub"
                print("===============================================================") 
                dump(authors = match, sleep_time=2, bformat=bformat)
            else:
                print("===============================================================\nCannot find " + author + " in DB, you spelt it wrong?") 
                choice = 99
        elif choice == "2": 
            print("===============================================================\n[1] EPUB\n[2] MOBI\n[3] PDF\n[4] All\n[0] Exit")
            ext = input("Choice format [1-4, default epub] ")
            if ext == "2": bformat = "mobi"
            elif ext == "3": bformat = "pdf"
            elif ext == "4": bformat = "all"
            elif ext == "0": exit(0)
            else: bformat = "epub"
            print("===============================================================\nCAUTION! It could take SOOOOOO long!")
            yn = input("Continue? [y/n] ")
            if yn.lower() == "y":
                print("===============================================================")
                dump(authors = get_all_authors(), sleep_time=1, bformat=bformat)
            else: exit(0)
        elif choice == "3": why()
        elif choice == "0": exit(0)
        else: print("You can't even choice a number between 0 and 3, c'mon.")

def run():
    print_logo()
    menu()

