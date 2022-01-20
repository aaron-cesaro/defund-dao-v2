//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "./LeagueBadge.sol";

contract LeagueManager {
    string[] public leagues = [
        "Venture",
        "Treasury",
        "Development",
        "Compliance"
    ];

    mapping(string => string[]) private leaguesToRoles;
    mapping(string => address[]) private rolesToMembers;
    mapping(address => string) private membersToRoles;
    mapping(address => uint256) private membersToTokenIds;

    LeagueBadge public leagueBadge;

    event RoleAdded(string _league, string _role);
    event RoleRemoved(string _league, string _role);
    event MemberAdded(
        address _to,
        string _league,
        string _role,
        uint256 _tokenId
    );
    event MemberRemoved(address _to, string _role, uint256 _tokenId);

    constructor() {
        leagueBadge = new LeagueBadge();

        leaguesToRoles[leagues[0]] = ["Analyst", "Associate"];
        leaguesToRoles[leagues[1]] = ["Auditor", "Approver"];
        leaguesToRoles[leagues[2]] = ["Developer", "Product-Owner"];
        leaguesToRoles[leagues[3]] = ["Enforcer", "Legal"];
    }

    function leagueExists(string memory _league)
        public
        view
        returns (bool, int256)
    {
        require(bytes(_league).length > 0, "leagueExists: league is empty");
        bool isPresent = false;
        int256 leagueIndex = -1;
        for (uint256 index = 0; index < leagues.length && !isPresent; index++) {
            if (
                keccak256(abi.encodePacked(leagues[index])) ==
                keccak256(abi.encodePacked(_league))
            ) {
                isPresent = true;
                leagueIndex = int256(index);
            }
        }
        return (isPresent, leagueIndex);
    }

    function addRole(string memory _league, string memory _role) public {
        (bool roleIsPresent, ) = roleExists(_league, _role);
        require(!roleIsPresent, "addRole: role already present");

        leaguesToRoles[_league].push(_role);

        emit RoleAdded(_league, _role);
    }

    function removeRole(string memory _league, string memory _role) public {
        (bool roleIsPresent, int256 rolePosition) = roleExists(_league, _role);
        require(
            roleIsPresent && rolePosition >= 0,
            "removeRole: role does not exist"
        );

        for (
            uint256 index = uint256(rolePosition);
            index < leaguesToRoles[_league].length - 1;
            index++
        ) {
            leaguesToRoles[_league][index] = leaguesToRoles[_league][index + 1];
        }
        leaguesToRoles[_league].pop();
        removeAllMembers(_league, _role);

        emit RoleRemoved(_league, _role);
    }

    function roleExists(string memory _league, string memory _role)
        public
        view
        returns (bool, int256)
    {
        require(bytes(_role).length > 0, "roleExists: _role is empty");

        (bool leagueIsPresent, ) = leagueExists(_league);
        require(leagueIsPresent, "roleExists: league does not exist");

        bool isPresent = false;
        int256 roleIndex = -1;
        for (
            uint256 index = 0;
            index < leaguesToRoles[_league].length && !isPresent;
            index++
        ) {
            if (
                keccak256(abi.encodePacked(leaguesToRoles[_league][index])) ==
                keccak256(abi.encodePacked(_role))
            ) {
                isPresent = true;
                roleIndex = int256(index);
            }
        }
        return (isPresent, roleIndex);
    }

    function getRoles(string memory _league)
        public
        view
        returns (string[] memory)
    {
        return leaguesToRoles[_league];
    }

    function getMemberRole(address _member)
        public
        view
        returns (string memory)
    {
        return membersToRoles[_member];
    }

    function addMember(
        address _newMember,
        string memory _league,
        string memory _role
    ) public returns (uint256) {
        (bool roleIsPresent, ) = roleExists(_league, _role);
        require(roleIsPresent, "addMember: role does not exists");

        uint256 _tokenId = leagueBadge.mintLeagueBadge(_newMember);
        rolesToMembers[_role].push(_newMember);
        membersToTokenIds[_newMember] = _tokenId;
        membersToRoles[_newMember] = _role;

        emit MemberAdded(_newMember, _league, _role, _tokenId);

        return _tokenId;
    }

    function setTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        leagueBadge._setTokenURI(_tokenId, _tokenURI);
    }

    function getTokenId(address _member) public view returns (uint256) {
        return membersToTokenIds[_member];
    }

    function removeMember(
        address _member,
        string memory _league,
        string memory _role
    ) public {
        (bool roleIsPresent, ) = roleExists(_league, _role);
        require(roleIsPresent, "removeMember: role does not exists");

        (bool memberIsPresent, int256 memberPosition) = memberExists(
            _member,
            _role
        );
        require(
            memberIsPresent && memberPosition >= 0,
            "removeMember: member does not exists"
        );

        for (
            uint256 index = uint256(memberPosition);
            index < rolesToMembers[_role].length - 1;
            index++
        ) {
            rolesToMembers[_role][index] = rolesToMembers[_role][index + 1];
        }
        rolesToMembers[_role].pop();
        uint256 _tokenId = membersToTokenIds[_member];

        leagueBadge.burnLeagueBadge(_tokenId);
        delete membersToTokenIds[_member];
        delete membersToRoles[_member];

        emit MemberRemoved(_member, _role, _tokenId);
    }

    function memberExists(address _member, string memory _role)
        public
        view
        returns (bool, int256)
    {
        bool isPresent = false;
        int256 memberIndex = -1;
        for (
            uint256 index = 0;
            index < rolesToMembers[_role].length && !isPresent;
            index++
        ) {
            if (rolesToMembers[_role][index] == _member) {
                isPresent = true;
                memberIndex = int256(index);
            }
        }
        return (isPresent, memberIndex);
    }

    function removeAllMembers(string memory _league, string memory _role)
        internal
    {
        for (uint256 index = 0; index < rolesToMembers[_role].length; index++) {
            removeMember(rolesToMembers[_role][index], _league, _role);
        }
    }

    function getMembers(string memory _role)
        public
        view
        returns (address[] memory)
    {
        return rolesToMembers[_role];
    }

    function transferOwnership(address newOwner) public virtual {
        require(
            newOwner != address(0),
            "transferOwnership: new owner is the zero address"
        );
        leagueBadge.transferOwnership(newOwner);
    }
}
