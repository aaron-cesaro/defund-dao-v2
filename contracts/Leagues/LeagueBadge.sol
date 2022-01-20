//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Pausable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LeagueBadge is ERC721Pausable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private tokenId;
    string private baseURI;
    mapping(uint256 => string) private tokenURIs;

    event BaseURIUpdated(string _baseURI);

    constructor() ERC721("DeFund League Badge", "DFLB") {
        _pause();
    }

    function mintLeagueBadge(address _to)
        external
        virtual
        onlyOwner
        returns (uint256)
    {
        // update tokenId
        tokenId.increment();

        uint256 _tokenId = tokenId.current();

        _unpause();
        // _beforeTokenTransfer
        _safeMint(_to, _tokenId);
        // _afterTokenTransfer
        //_setTokenURI(_tokenId, _tokenURI);

        return _tokenId;
    }

    function burnLeagueBadge(uint256 _tokenId) external virtual onlyOwner {
        _unpause();
        super._burn(_tokenId);
    }

    function _setTokenURI(uint256 _tokenId, string memory _tokenURI)
        external
        virtual
        onlyOwner
    {
        require(
            _exists(_tokenId),
            "setTokenURI: tokenURI set of nonexistent token"
        );
        require(
            bytes(_tokenURI).length > 0,
            "setTokenURI: tokenURI cannot be empty"
        );
        require(
            bytes(tokenURIs[_tokenId]).length == 0,
            "setTokenURI: tokenURI cannot be changed"
        );

        tokenURIs[_tokenId] = _tokenURI;
    }

    function tokenURI(uint256 _tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(_exists(_tokenId), "tokenURI: URI query for nonexistent token");

        string memory baseURI = _baseURI();
        string memory _tokenURI = tokenURIs[_tokenId];
        return
            bytes(baseURI).length > 0
                ? string(abi.encodePacked(baseURI, _tokenURI))
                : _tokenURI;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function _beforeTokenTransfer(
        address _from,
        address _to,
        uint256 _tokenId
    ) internal virtual override {
        super._beforeTokenTransfer(_from, _to, _tokenId);
        if (_to != address(0)) {
            require(
                balanceOf(_to) == 0,
                "_beforeTokenTransfer: members cannot have more than one badge"
            );
        }
    }

    function _afterTokenTransfer(
        address _from,
        address _to,
        uint256 _tokenId
    ) internal virtual override {
        super._afterTokenTransfer(_from, _to, _tokenId);
        // Token has been minted
        if (_from == address(0)) {
            _approve(msg.sender, _tokenId);
        }
        // Token has been transferred, otherwise token has been burned
        else if (_to != address(0)) {
            _approve(_from, _tokenId);
        }
        _pause();
    }
}
