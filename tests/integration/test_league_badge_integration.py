import pytest
from brownie import Contract, exceptions
from scripts.helpful_scripts import (
    get_account,
    write_metadata,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import deploy_league_badge, deploy_league_manager


def test_add_member(leagues, venture_league_roles):
    # Arrange
    account = get_account()
    league_manager = deploy_league_manager()
    league_badge = Contract.from_abi(
        "LeagueBadge",
        league_manager.leagueBadge(),
        deploy_league_badge().abi,
    )
    badge_awardee = "0xAFa5D1e5fb62851a73AC585540ddAEB35828ACDA"
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_award = league_manager.addMember(
        badge_awardee,
        venture_league,
        analyst_role,
        {"from": account},
    )
    tx_award.wait(1)
    token_id = league_manager.getTokenId(badge_awardee)
    token_uri = write_metadata(token_id, venture_league, league_badge, league_manager)
    tx_set_token_uri = league_manager.setTokenURI(
        token_id, token_uri, {"from": account}
    )
    tx_set_token_uri.wait(1)
    # Assert
    assert league_badge.owner() == league_manager.address
    assert league_badge.ownerOf(token_id) == badge_awardee
    assert league_badge.tokenURI(token_id) == token_uri
    assert league_manager.getMemberRole(badge_awardee) == analyst_role
    assert league_manager.getTokenId(badge_awardee) == token_id


def test_remove_member(leagues, venture_league_roles):
    # Arrange
    account = get_account()
    league_manager = deploy_league_manager()
    league_badge = Contract.from_abi(
        "LeagueBadge",
        league_manager.leagueBadge(),
        deploy_league_badge().abi,
    )
    badge_awardee = "0xAFa5D1e5fb62851a73AC585540ddAEB35828ACDA"
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_award = league_manager.addMember(
        badge_awardee,
        venture_league,
        analyst_role,
        {"from": account},
    )
    tx_award.wait(1)
    token_id = league_manager.getTokenId(badge_awardee)
    token_uri = write_metadata(token_id, venture_league, league_badge, league_manager)
    tx_set_token_uri = league_manager.setTokenURI(
        token_id, token_uri, {"from": account}
    )
    tx_set_token_uri.wait(1)
    tx_revoke = league_manager.removeMember(
        badge_awardee, venture_league, analyst_role, {"from": account}
    )
    tx_revoke.wait(1)
    # Assert
    assert league_badge.balanceOf(badge_awardee) == 0
    assert league_badge.owner() == league_manager.address
    with pytest.raises(exceptions.VirtualMachineError):
        league_badge.ownerOf(token_id) == badge_awardee
    with pytest.raises(exceptions.VirtualMachineError):
        assert league_badge.tokenURI(token_id) == token_uri
    assert league_manager.getMemberRole(badge_awardee) == ""
    assert league_manager.getTokenId(badge_awardee) == 0
