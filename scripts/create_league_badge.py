from scripts.deploy import deploy_league_badge, deploy_league_manager
from scripts.helpful_scripts import (
    get_account,
    write_metadata,
    OPENSEA_FORMAT,
    LEAGUES,
    VENTURE_LEAGUE_ROLES,
)
from brownie import Contract


def main():
    league_manager = deploy_league_manager()
    (exists, position) = league_manager.memberExists(
        "0xAFa5D1e5fb62851a73AC585540ddAEB35828ACDA", VENTURE_LEAGUE_ROLES[0]
    )
    if exists:
        remove_member(LEAGUES, VENTURE_LEAGUE_ROLES)
    add_member(LEAGUES, VENTURE_LEAGUE_ROLES)


def add_member(LEAGUES, VENTURE_LEAGUE_ROLES):
    account = get_account()
    league_manager = deploy_league_manager()
    league_badge = Contract.from_abi(
        "LeagueBadge",
        league_manager.leagueBadge(),
        deploy_league_badge().abi,
    )
    badge_awardee = "0xAFa5D1e5fb62851a73AC585540ddAEB35828ACDA"
    venture_league = LEAGUES[0]
    analyst_role = VENTURE_LEAGUE_ROLES[0]
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
    print(f"tokenURI: {league_badge.tokenURI(token_id)}")
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(league_manager.leagueBadge(), token_id)
        )
    )


def remove_member(LEAGUES, VENTURE_LEAGUE_ROLES):
    account = get_account()
    league_manager = deploy_league_manager()
    league_badge = Contract.from_abi(
        "LeagueBadge",
        league_manager.leagueBadge(),
        deploy_league_badge().abi,
    )
    badge_awardee = "0xAFa5D1e5fb62851a73AC585540ddAEB35828ACDA"
    venture_league = LEAGUES[0]
    analyst_role = VENTURE_LEAGUE_ROLES[0]
    tx_remove = league_manager.removeMember(
        badge_awardee,
        venture_league,
        analyst_role,
        {"from": account},
    )
    tx_remove.wait(1)
    print("Member {} removed".format(badge_awardee))
