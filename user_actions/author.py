from contract_interaction import register_book as reg_book
START_AUTHOR_md = """
# Book-Store

Hi Author!, To register a book on book-store follwong steps required:

1. submit the private key of your wallet *(hex string)*
2. submit the path of the book's pdf file
3. submit the price of mint (in Wei)

"""

def read_inputs():
    pdf_path = input("Enter you book path: ")
    mint_price = int(input("Enter price of book(In Wei): "))
    print( pdf_path, mint_price)
    return pdf_path,mint_price

def register_book( pdf_path, mint_price):
    reg_book( pdf_path, mint_price)