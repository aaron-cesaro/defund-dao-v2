# Leagues

## League Badge

### Description
The League Badge is a NFT based badge that permit League members to join specific and regulated channels on the DeFund discord server. Each NFT contains its own information metadata that resides on IPFS.

### Specs
1. Each League Role belongs to a specific League. A role cannot exists without a League.
2. Each League Role (Analyst, Developer, etc..) has its own League Badge, that is a NFT.
3. League Badges are awarded (minted) and revoked (burned) to DeFund members through the voting mechanism.
4. League Badge ids start from 1 and are incremented after each minting
5. League Members cannot mint, transfer, or burn any League Badge. Even if they are the Badge owners
6. Eeach League Badge, as well as its owner, is unique by definition. No badge can be owned by more than one member.
7. No one can transfer a League Badge, not even through a passed proposal. In case of a new member is selected and another member with same role (and League) is removed, the League Badge from the removed member is burned, and the League Badge for the new member is minted. 
8. Each League Member can own at most one Badge. No member can have more than one role throughout all Leagues.
9. Roles can be added and deleted through the voting mechanism.
10. Leagues can be added and deleted through the voting mechanism. By deleting a League, all associated roles are deleted, as well as all minted badges

### Tools
#### Community
1. Collab.land (discord bot, to check if the user is owner of the NFT with a specific tokenId)