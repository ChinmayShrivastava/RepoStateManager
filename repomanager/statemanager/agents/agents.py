import os
from superagent.client import Superagent

client = Superagent(
    base_url="https://api.beta.superagent.sh",
    token=os.environ["SUPERAGENT_API_KEY"]
)