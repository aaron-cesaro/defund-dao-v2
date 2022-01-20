from hashlib import new
from brownie import network, exceptions
import pytest
from scripts.deploy import deploy_league_manager, deploy_league_badge
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_league_exists(leagues):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    development_league = leagues[2]
    treasury_league = leagues[1]
    # Act
    venture_league_position = league_manager.leagueExists(venture_league)[1]
    development_league_position = league_manager.leagueExists(development_league)[1]
    treasury_league_position = league_manager.leagueExists(treasury_league)[1]
    # Assert
    assert league_manager.leagues(venture_league_position) == venture_league
    assert league_manager.leagues(development_league_position) == development_league
    assert league_manager.leagues(treasury_league_position) == treasury_league


def test_add_role(leagues):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    researcher_role = "Researcher"
    # Act
    tx_add_role = league_manager.addRole(
        venture_league, researcher_role, {"from": account}
    )
    tx_add_role.wait(1)
    role_exists, role_position = league_manager.roleExists(
        venture_league, researcher_role
    )
    # Assert
    assert role_exists == True
    assert league_manager.getRoles(venture_league)[role_position] == researcher_role


def test_remove_role(leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_remove_role = league_manager.removeRole(
        venture_league, analyst_role, {"from": account}
    )
    tx_remove_role.wait(1)
    role_exists, role_position = league_manager.roleExists(venture_league, analyst_role)
    # Assert
    assert role_exists == False
    assert role_position == -1


def test_league_persists_after_remove_all_role(leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_remove_role = league_manager.removeRole(
        venture_league, analyst_role, {"from": account}
    )
    tx_remove_role.wait(1)
    league_exists, league_position = league_manager.leagueExists(venture_league)
    # Assert
    assert league_exists == True
    assert league_manager.leagues(league_position) == venture_league


def test_add_member(URI, leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    new_member = get_account(1)
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_add_new_member = league_manager.addMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_add_new_member.wait(1)
    token_id = league_manager.getTokenId(new_member)
    tx_set_token_uri = league_manager.setTokenURI(token_id, URI)
    tx_set_token_uri.wait(1)
    member_exists, member_position = league_manager.memberExists(
        new_member, analyst_role
    )
    # Assert
    assert member_exists == True
    assert league_manager.getMembers(analyst_role)[member_position] == new_member


def test_cannot_add_same_member_twice(URI, leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    new_member = get_account(1)
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_add_new_member = league_manager.addMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_add_new_member.wait(1)
    token_id = league_manager.getTokenId(new_member)
    tx_set_token_uri = league_manager.setTokenURI(token_id, URI)
    tx_set_token_uri.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tx_add_new_member = league_manager.addMember(
            new_member, venture_league, analyst_role, {"from": account}
        )


def test_cannot_add_same_member_to_more_than_one_role(
    URI, leagues, venture_league_roles
):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    new_member = get_account(1)
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    trasury_league = leagues[1]
    analyst_role = venture_league_roles[0]
    associate_role = venture_league_roles[1]
    # Act
    tx_add_new_member = league_manager.addMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_add_new_member.wait(1)
    token_id = league_manager.getTokenId(new_member)
    tx_set_token_uri = league_manager.setTokenURI(token_id, URI)
    tx_set_token_uri.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tx_add_new_member = league_manager.addMember(
            new_member, trasury_league, associate_role, {"from": account}
        )


def test_remove_member(URI, leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    new_member = get_account(1)
    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_add_new_member = league_manager.addMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_add_new_member.wait(1)
    token_id = league_manager.getTokenId(new_member)
    tx_set_token_uri = league_manager.setTokenURI(token_id, URI)
    tx_set_token_uri.wait(1)
    member_exists, member_position = league_manager.memberExists(
        new_member, analyst_role
    )
    # Assert
    assert member_exists == True
    assert member_position == 0
    tx_remove_member = league_manager.removeMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_remove_member.wait(1)
    member_exists, member_position = league_manager.memberExists(
        new_member, analyst_role
    )
    # Assert
    assert member_exists == False
    assert member_position == -1


def test_cannot_remove_same_member_twice(URI, leagues, venture_league_roles):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    new_member = get_account(1)

    league_manager = deploy_league_manager()
    venture_league = leagues[0]
    analyst_role = venture_league_roles[0]
    # Act
    tx_add_new_member = league_manager.addMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_add_new_member.wait(1)
    token_id = league_manager.getTokenId(new_member)
    tx_set_token_uri = league_manager.setTokenURI(token_id, URI)
    tx_set_token_uri.wait(1)
    tx_remove_member = league_manager.removeMember(
        new_member, venture_league, analyst_role, {"from": account}
    )
    tx_remove_member.wait(1)
    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tx_remove_member = league_manager.removeMember(
            new_member, venture_league, analyst_role, {"from": account}
        )
