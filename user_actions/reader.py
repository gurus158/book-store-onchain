from contract_interaction import register_book as reg_book
from contract_interaction import mint
START_AUTHOR_md = """
# Book-Store

Hi Author!, To register a book on book-store follwong steps required:

1. submit the private key of your wallet *(hex string)*
2. submit the path of the book's pdf file
3. submit the price of mint (in Wei)

"""

def read_inputs():
    book_id = input("Enter book id:")
    private_key = input("Enter your private key: ")
    print(private_key)
    return book_id,private_key
    
def mint_book( book_id:int, private_key:str):
    return mint(book_id,private_key)