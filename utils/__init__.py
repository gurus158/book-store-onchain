"""Module for encryption and decryption compatible with MetaMask."""
from base64 import a85decode, a85encode
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfReader, PdfWriter
import requests
import json
from nacl.public import Box, PrivateKey, PublicKey
from dotenv import dotenv_values

from PIL import Image, ImageDraw
import random
config = dotenv_values(".env")
WEB_STORAGE_API = "https://api.web3.storage/upload/"
METADATA_ENDPOINT = 'https://{}.ipfs.dweb.link'

WEB3_STORAGE_API_HEADER_BINARY = {
    'Content-Type': 'application/octet-stream',
    'Authorization': config["WEB3_TOKEN"]
}

def _hex_to_bytes(hex: str) -> bytes:
    return bytes.fromhex(hex[2:] if hex[:2] == "0x" else hex)


def export_public_key(private_key_hex: str) -> bytes:
    """Export public key for contract join request.
    Args:
        private_key: hex string representing private key
    Returns:
        32 bytes representing public key
    """
    return bytes(PrivateKey(_hex_to_bytes(private_key_hex)).public_key)


def encrypt_nacl(public_key: bytes, data: bytes) -> bytes:
    """Encryption function using NaCl box compatible with MetaMask
    For implementation used in MetaMask look into: https://github.com/MetaMask/eth-sig-util
    Args:
        public_key: public key of recipient (32 bytes)
        data: message data
    Returns:
        encrypted data
    """
    emph_key = PrivateKey.generate()
    enc_box = Box(emph_key, PublicKey(public_key))
    # Encryption must work with MetaMask decryption (requires valid utf-8)
    data = a85encode(data)
    ciphertext = enc_box.encrypt(data)
    return bytes(emph_key.public_key) + ciphertext


def decrypt_nacl(private_key: bytes, data: bytes) -> bytes:
    """Decryption function using NaCl box compatible with MetaMask
    For implementation used in MetaMask look into: https://github.com/MetaMask/eth-sig-util
    Args:
        private_key: private key to decrypt with
        data: encrypted message data
    Returns:
        decrypted data
    """
    emph_key, ciphertext = data[:32], data[32:]
    box = Box(PrivateKey(private_key), PublicKey(emph_key))
    return a85decode(box.decrypt(ciphertext))

def upload_data_on_ipfs(data):
    response = requests.request("POST", WEB_STORAGE_API,headers=WEB3_STORAGE_API_HEADER_BINARY,data=data)
    if response.status_code != 200:
        print("upload on ipfs failed")
        return None
    return METADATA_ENDPOINT.format(response.json()['cid'])

def upload_book_on_ipfs(pdf_path:str,password:str) -> str:
    try:
        with open(pdf_path, "rb") as in_file:
            input_pdf = PdfFileReader(in_file)
            output_pdf = PdfFileWriter()
            output_pdf.appendPagesFromReader(input_pdf)
            output_pdf.encrypt(password)
            cid = None
            with open("output.pdf", "wb") as out_file:
                output_pdf.write(out_file)
            cid = upload_data_on_ipfs(open("output.pdf","rb"))
            if not cid:
                print("upload on ipfs failed")
                return None
            return cid
    except Exception as e:
        print(str(e))
        return None

def upload_user_copy(ipfs_link,password):
    response = requests.get(ipfs_link)
    book_metadata = response.json()
    print(book_metadata)
    pdf_uri = book_metadata["book_link"]
    response = requests.get(pdf_uri)
    if response.status_code != 200:
        print("getting pdf from ipfs link failed")
        return None
    open("mint_org_encrypted.pdf", "wb").write(response.content)
    reader = PdfReader("mint_org_encrypted.pdf")
    writer = PdfWriter()
    if reader.is_encrypted:
        reader.decrypt(config["APP_PASSWORD"])

    for page in reader.pages:
        writer.add_page(page)
    if isinstance(password, bytes):
        password = password.decode()
    writer.encrypt(password)
    with open("mint_copy_user.pdf",'wb') as f:
        writer.write(f)
    
    copy_book_uri = upload_data_on_ipfs(open("mint_copy_user.pdf",'rb'))
    book_metadata_dict = {
        "name" : book_metadata["name"],
        "image_url":book_metadata["image_url"],
        "description": book_metadata["description"],
        "book_link": copy_book_uri
    }
    book_metadata = json.dumps(book_metadata_dict,sort_keys=True, default=str)
    print(book_metadata)
    return upload_data_on_ipfs(data=book_metadata)

def create_book_image(book_name) -> str:
    x= random.randrange(30,100)
    y=random.randrange(30,100)
    r = random.randrange(10,120)
    g = random.randrange(10,120)
    b = random.randrange(10,120)
    img = Image.new('RGB', (x, y), color = (r, g, b))
    d = ImageDraw.Draw(img)
    d.text((10,10), "Hello World", fill=(255,255,0))
    img.save('book.png')
    cid = upload_data_on_ipfs(open('book.png','rb'))
    if not cid:
        print("upload on ipfs book image failed")
        return None
    return cid 
    
