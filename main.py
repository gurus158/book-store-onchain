from rich.console import Console
from rich.markdown import Markdown
from user_actions import reader, author

console = Console()
WELCOME_BANNER_md = Markdown("""
# Welcome to web3 book-store
This project is about ,  how one should implement sharing private data on public blockchain?

Book-store application is implemented as POC

## Features
1. Author can register a book(in pdf format)
2. Reader can mint book regiter by author
3. User will have its own unique encrypted copy
4. only owner of Copy(NFT) can only read the book

Press any key to start

""")

START_OPTION_md = Markdown("""
# Book-Store

1. Press 1 to regiter a book
2. Press 2 to Mint a book
3. Press 3 to list minted books
""")



def startApp():
    console.print(WELCOME_BANNER_md)
    console.print("\n\n")
    x = input()
    if x !=None:
        console.clear()
        action = 10000
        while(1):
            if action not in [1,2,3]:
                if action!=10000:
                    console.print("Please select valid options",style="bold red")
                console.print(START_OPTION_md)
                action = int(input())
                continue
            break
        console.clear()
        if action==1:
            console.print(Markdown( author.START_AUTHOR_md))
            pdf_path,mint_price = author.read_inputs()
            author.register_book(pdf_path,mint_price)
        if action==2:
            pass
        if action==3:
            pass
            
    return


if __name__=="__main__":
    startApp()
    # msg = "test_msg"
    # private_key = '793f741086e9b0b87dee635660b671db2e60e98d1e87e22d96be176cb757618a'
    # encrypt_hex = utils.encrypt_nacl(utils.export_public_key(private_key_hex=private_key),bytes(msg.encode())).hex()
    # print(encrypt_hex)
    # # print(codecs.decode(encrypt_hex,'hex_codec'))
    # decode_text = utils.decrypt_nacl(bytes.fromhex(private_key),codecs.decode(encrypt_hex,'hex_codec'))
    # print(decode_text)
    

