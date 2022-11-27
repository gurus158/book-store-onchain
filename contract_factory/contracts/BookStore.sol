// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.16;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./utils/AdminPermissionable.sol";

contract BookStore is 
    ERC721Burnable,
    AdminPermissionable{
    uint256 currentbookId;
    uint256 currentTokenId;
    uint256[] public allBooksIds;

    struct Book {
        uint256 bookID;
        uint256 price;
        uint256 transferPrice;
        string bookPublicUri;
        address bookAuther;
    }
    
    struct UserKeys{
        string encryptionKey;
        string decryptionKey;
    }

    mapping (uint256 => Book) public books; // map book ids with book
    mapping(uint256 => string) public uriMapping;
    mapping(address => uint256[]) public userTokenMapping;
    mapping(address => UserKeys) public userKeysMapping;

    error BookNotFound();
    error NotEnoughPrice();
    error CannotTransfer();
    error BadKey();

    event BookPurchased(uint256 _booksID , address _byer, uint256 _tokenID);

    constructor(
        address _admin,
        string memory _name,
        string memory _symbol
    ) 
    ERC721(_name,_symbol) {
       _grantRole(DEFAULT_ADMIN_ROLE, _admin);
       currentbookId=1;
       currentTokenId=1;

    }

    function addKeys(string memory _encryptionkey, string memory _decryptionKey) public {
        if(bytes(_encryptionkey).length ==0 || bytes(_decryptionKey).length ==0) revert BadKey();
        userKeysMapping[msg.sender].encryptionKey = _encryptionkey;
        userKeysMapping[msg.sender].decryptionKey = _decryptionKey;
    }

    function getUserKeys(address _user) public view returns(string memory ,string memory){
        return (userKeysMapping[_user].encryptionKey,userKeysMapping[_user].decryptionKey);
    }

    function registerBook(string memory _bookPublicUri, uint256 _price, uint256 _transferPrice) public {
        books[currentbookId].bookID = currentbookId;
        books[currentbookId].price = _price;
        books[currentbookId].transferPrice = _transferPrice;
        books[currentbookId].bookPublicUri = _bookPublicUri;
        books[currentbookId].bookAuther = msg.sender;
        allBooksIds.push(currentbookId);
        currentbookId = currentbookId +1;
    }

    function getBook(uint256 _bookId) public view returns (uint256,uint256,string memory) {
        if(books[_bookId].bookID==0) revert BookNotFound();
        return (books[_bookId].bookID,books[_bookId].price,books[_bookId].bookPublicUri);
    }

    function claimBookPaid(uint256 _bookId, string memory _bookCopyUri) payable public {
        if(books[_bookId].bookID==0) revert BookNotFound();
        if( msg.value < books[_bookId].price) revert NotEnoughPrice();
        uriMapping[currentTokenId] = _bookCopyUri;
        payable(books[_bookId].bookAuther).transfer(msg.value);
        userTokenMapping[msg.sender].push(currentTokenId);
        currentTokenId = currentTokenId+1;
        emit BookPurchased(_bookId, msg.sender,currentTokenId-1);
        _safeMint(msg.sender,currentTokenId-1,"");
    }

    function claimBookFree(uint256 _bookId, string memory _bookCopyUri) public{
        if(books[_bookId].bookID==0) revert BookNotFound();
        if(books[_bookId].price > 0) revert NotEnoughPrice();
        uriMapping[_bookId] = _bookCopyUri;
        userTokenMapping[msg.sender].push(currentTokenId);
        currentTokenId = currentbookId+1;
        emit BookPurchased(_bookId, msg.sender,currentTokenId-1);
        _safeMint(msg.sender,currentTokenId-1,"");
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenID,
        uint256 batchSize
    ) virtual internal override {
        if(from == address(0) || to == address(0)){
            super._beforeTokenTransfer(from,to,tokenID,batchSize);
        }
        else{
        revert CannotTransfer();
        }
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory){
            return uriMapping[tokenId];
        }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}