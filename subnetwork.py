import functools
import bittensor as bt


from typing import Any, ClassVar, Dict, Optional, Type
from pydantic import BaseModel, Field, PositiveInt

# The maximum bytes for metadata on the chain.
MAX_METADATA_BYTES = 128
# The length, in bytes, of a git commit hash.
GIT_COMMIT_LENGTH = 40
# The length, in bytes, of a base64 encoded sha256 hash.
SHA256_BASE_64_LENGTH = 44
# The max length, in characters, of the competition id
MAX_COMPETITION_ID_LENGTH = 2

class ModelId(BaseModel):
    """Uniquely identifies a trained model"""

    MAX_REPO_ID_LENGTH: ClassVar[int] = (
        MAX_METADATA_BYTES
        - GIT_COMMIT_LENGTH
        - SHA256_BASE_64_LENGTH
        - MAX_COMPETITION_ID_LENGTH
        - 4  # separators
    )

    namespace: str = Field(
        description="Namespace where the model can be found. ex. Hugging Face username/org."
    )
    block: Optional[int] = Field(
        description="block number"
    )
    name: str = Field(description="Name of the model.")

    chat_template: str = Field(description="Chat template for the model.")

    # When handling a model locally the commit and hash are not necessary.
    # Commit must be filled when trying to download from a remote store.
    commit: Optional[str] = Field(
        description="Commit of the model. May be empty if not yet committed."
    )
    # Hash is filled automatically when uploading to or downloading from a remote store.
    hash: Optional[str] = Field(description="Hash of the trained model.")
    # Identifier for competition
    competition_id: Optional[str] = Field(description="The competition id")

    def to_compressed_str(self) -> str:
        """Returns a compressed string representation."""
        return f"{self.namespace}:{self.name}:{self.chat_template}:{self.commit}:{self.hash}:{self.competition_id}"

    @classmethod
    def from_compressed_str(cls, cs: str) -> Type["ModelId"]:
        """Returns an instance of this class from a compressed string representation"""
        tokens = cs.split(":")
        return cls(
            namespace=tokens[0],
            name=tokens[1],
            chat_template=tokens[2] if tokens[2] != "None" else None,
            commit=tokens[3] if tokens[3] != "None" else None,
            hash=tokens[4] if tokens[4] != "None" else None,
            competition_id=(
                tokens[5] if len(tokens) >= 6 and tokens[5] != "None" else None
            ),
        )




def fetch_stats(subtensor, hotkey: str):
        subnet_uid = 11
        metadata = bt.extrinsics.serving.get_metadata(subtensor, subnet_uid, hotkey=hotkey)
        if metadata is None:
              return None
        return f(metadata)



def get_data():
        ssubtensor = bt.subtensor()
        subnet_uid = 11
        metagraph = ssubtensor.metagraph(subnet_uid)
        return_data = {}
        for uid, hotkey in enumerate(list(metagraph.hotkeys)):
              ggg = fetch_stats(ssubtensor, hotkey)
              if ggg is not None:
                return_data[uid] = {
                      "hotkey": hotkey,
                    "block": ggg.block,
                    "namespace": ggg.namespace,
                    "name": ggg.name,
                    "chat_template": ggg.chat_template,
                    "commit": ggg.commit,
                    "competition_id": ggg.competition_id,
                }


        if return_data:
              print(return_data)
        return return_data        


        

def f(metadata):
        commitment = metadata["info"]["fields"][0]
        hex_data = commitment[list(commitment.keys())[0]][2:]

        chain_str = bytes.fromhex(hex_data).decode()
        model_id = ModelId.from_compressed_str(chain_str)
        model_id.block = metadata["block"]
        return model_id

get_data()