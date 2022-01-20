import pytest


@pytest.fixture()
def URI():
    return "https://ipfs.io/ipfs/QmSgfMARvriBWwPVh4x7mETGkqUJpwtoUQc8BAmoRSK5hU?filename=Defund Venture League #1 - Analyst.json"


@pytest.fixture()
def leagues():
    return ["Venture", "Treasury", "Development", "Compliance"]


@pytest.fixture()
def venture_league_roles():
    return ["Analyst", "Associate"]


@pytest.fixture()
def treasury_league_roles():
    return ["Auditor", "Approver"]


@pytest.fixture()
def development_league_roles():
    return ["Developer", "Product-Owner"]


@pytest.fixture()
def compliance_league_roles():
    return ["Enforcer", "Legal"]
