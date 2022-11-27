from web3 import Web3
from dotenv import dotenv_values
import json
import utils
import random
import string
from rich.console import Console
import codecs
console = Console()
config = dotenv_values(".env")
rpc_url = config["WEB3_RPC_PROVIDER_URL"]
w3 = Web3(Web3.HTTPProvider(rpc_url))
abi = json.load(open(config["ABI_FILE"]))
contract_address = config["BOOK_CONTRACT_ADDRESS"]
book_store_contract = w3.eth.contract(address=contract_address, abi=abi) 
CHAIN_ID = 80001
BLOCKCHAIN_GAS = 3500000



def get_user_keys(address = None) -> list:
    if address==None:
        return []
    author_keys = book_store_contract.functions.getUserKeys(address).call()
    for i in author_keys:
        if not i:
            return []
    return author_keys

def register_user_transaction(author_account:w3.eth.account, encryption_key:bytes , decryption_key:str):
    transaction = book_store_contract.functions.addKeys(str(encryption_key.hex()),decryption_key).buildTransaction({
            'chainId': CHAIN_ID,
            'gas': BLOCKCHAIN_GAS,
            'gasPrice': w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(author_account.address),
        }
        )
    signed_transaction = author_account.sign_transaction(transaction)
    w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    hash = w3.toHex(w3.keccak(signed_transaction.rawTransaction))
    receipt = w3.eth.wait_for_transaction_receipt(hash)
    console.log(f"register user hash: {hash}\nRecipt: {receipt}")
    return hash


def add_book_transaction(app_account:w3.eth.account,book_ipfs_link:str, price:int):
    transaction = book_store_contract.functions.registerBook(book_ipfs_link,price,0).buildTransaction({
            'chainId': CHAIN_ID,
            'gas': BLOCKCHAIN_GAS,
            'gasPrice': w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(app_account.address),
        }
        )
    signed_transaction = app_account.sign_transaction(transaction)
    w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    hash = w3.toHex(w3.keccak(signed_transaction.rawTransaction))
    receipt = w3.eth.wait_for_transaction_receipt(hash)
    console.log(f"register user hash: {hash}\nRecipt: {receipt}")
    return hash

def register_book(pdf_path:str, mint_price:float) -> bool:
    app_account = w3.eth.account.privateKeyToAccount(config["APP_PRIVATE_KEY"])
    book_ipfs_link = utils.upload_book_on_ipfs(pdf_path=pdf_path,password=config["APP_PASSWORD"])
    if not book_ipfs_link:
        console.print("[ERROR] Upoading copy on ipfs failed", style="bold red")
        return False
    print("book uploaded on ipfs:" , book_ipfs_link)
    name = pdf_path.split('/')[-1]
    book_image_link = utils.create_book_image(name)
    if not book_image_link:
        console.print("[ERROR] Upoading image of book on ipfs failed", style="bold red")
        return False

    book_metadata_dict = {
        "name" : name,
        "image_url":book_image_link,
        "description": f"This is a book uploaded on web3 book-store by author {app_account.address}",
        "book_link": book_ipfs_link
    }

    book_metadata = json.dumps(book_metadata_dict,sort_keys=True, default=str)
    metadata_link = utils.upload_data_on_ipfs(data=book_metadata)
    register_book_hash = add_book_transaction(app_account=app_account,book_ipfs_link=metadata_link,price=mint_price)
    console.log(f"Book register hash = {register_book_hash}")
    return True

def get_book_from_chain(book_id:int):
    book_info = book_store_contract.functions.books(book_id).call()
    return book_info

def mint(book_id:int, private_key:str) -> bool:
    reader_account = w3.eth.account.privateKeyToAccount(private_key)
    reader_keys = get_user_keys(reader_account.address)
    password = ''.join(random.choices(string.ascii_letters, k=12)) 
    if not reader_keys:
        console.log("User is not registerd.\nregistering user")
        encryption_key = utils.export_public_key(private_key_hex=private_key)
        decryption_key = utils.encrypt_nacl(encryption_key,bytes(password.encode())).hex()
        user_register_hash = register_user_transaction(reader_account, encryption_key=encryption_key, decryption_key=decryption_key)
        console.log(f"User register hash = {user_register_hash}")
    else:
        console.log("Getting your encryption and decryption keys from chain")
        encryption_key,decryption_key = reader_keys
        password = utils.decrypt_nacl(bytes.fromhex(private_key),codecs.decode(decryption_key,'hex_codec'))
        console.log(password)
    
    book_info = get_book_from_chain(book_id)
    if not book_info:
        console.log("[ERROR] No Book of given book id present on chain",style="bold red")
        return False
    book_id, book_price , _ , book_uri , _ = book_info
    print(book_id, book_uri, book_price, "---------------------")
    copy_uri = utils.upload_user_copy(book_uri,password)
    if not copy_uri:
        return None
    transaction = book_store_contract.functions.claimBookPaid(book_id,copy_uri).buildTransaction({
            'chainId': CHAIN_ID,
            'gas': BLOCKCHAIN_GAS,
            'gasPrice': w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(reader_account.address),
            "value":book_price
        }
        )
    signed_transaction = reader_account.sign_transaction(transaction)
    w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    hash = w3.toHex(w3.keccak(signed_transaction.rawTransaction))
    receipt = w3.eth.wait_for_transaction_receipt(hash)
    console.log(f"register user hash: {hash}\nRecipt: {receipt}")
    return hash
    
