import os
from pathlib import Path
import requests
import json
from brownie import accounts, network, config
from metadata import league_badge_metadata_template

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

LEAGUES = ["Venture", "Treasury", "Development", "Compliance"]

VENTURE_LEAGUE_ROLES = ["Analyst", "Associate"]
TREASURY_LEAGUE_ROLES = ["Auditor", "Approver"]
DEVELOPMENT_LEAGUE_ROLES = ["Developer", "Product-Owner"]
COMPLIANCE_LEAGUE_ROLES = ["Enforcer", "Legal"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def write_metadata(token_id, league, league_badge_contract, league_manager_contract):
    collectible_metadata = league_badge_metadata_template.metadata_template
    member_address = league_badge_contract.ownerOf(token_id)
    role = league_manager_contract.getMemberRole(member_address)
    metadata_file_name = (
        "./metadata/{}/".format(network.show_active())
        + str(token_id)
        + "-"
        + str(league).upper()
        + "-LEAGUE-"
        + str(role).upper()
        + ".json"
    )
    print("Creating Metadata file: " + metadata_file_name)
    collectible_metadata["name"] = "{} League #{} - {}".format(league, token_id, role)
    collectible_metadata["description"] = "DeFund {} League Badge".format(league)
    image_to_upload = None
    image_path = "./img/{}.png".format(str(league).lower())
    image_to_upload = upload_to_ipfs(image_path, token_id)
    collectible_metadata["image"] = image_to_upload
    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    metadata_ipfs_path = upload_to_ipfs(metadata_file_name, token_id)
    return metadata_ipfs_path


def upload_to_ipfs(filepath, token_id):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL") if os.getenv("IPFS_URL") else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        if filepath.split(".")[-1:][0] != "json":
            filename = str(str(token_id) + "-" + filepath.split("/")[-1:][0]).lower()
        file_uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(file_uri)
    return file_uri
