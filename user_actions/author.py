from contract_interaction import register_book as reg_book
START_AUTHOR_md = """
# Book-Store

Hi Author!, To register a book on book-store follwong steps required:

1. submit the private key of your wallet *(hex string)*
2. submit the path of the book's pdf file
3. submit the price of mint (in Wei)

"""

def read_inputs():
    # private_key = '6a7505b3f79a121779f307dacf8e23e1b7b52f87749211ad6518e6a606f0ac77'#input("Enter your private key: ")
    pdf_path = '/home/gurdeep/Downloads/Advanced Python Programming ( PDFDrive ).pdf' #input("Enter you book path: ")
    mint_price = 100000000000000#int(input("Enter price of book(In Wei): "))
    print( pdf_path, mint_price)
    return pdf_path,mint_price

def register_book( pdf_path, mint_price):
    reg_book( pdf_path, mint_price)