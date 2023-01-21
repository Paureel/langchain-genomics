"""Util that calls WolframAlpha."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env
import torch

class ESM2APIWrapper(BaseModel):
    """Wrapper for ESM2.
    """

    wolfram_client: Any  #: :meta private:
    wolfram_alpha_appid: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        wolfram_alpha_appid = get_from_dict_or_env(
            values, "wolfram_alpha_appid", "WOLFRAM_ALPHA_APPID"
        )
        values["wolfram_alpha_appid"] = wolfram_alpha_appid

        try:
            import wolframalpha

        except ImportError:
            raise ImportError(
                "wolframalpha is not installed. "
                "Please install it with `pip install wolframalpha`"
            )
        client = wolframalpha.Client(wolfram_alpha_appid)

        values["wolfram_client"] = client

        # TODO: Add error handling if keys are missing
        return values

    def run(self, query: str) -> str:
        """Run query through WolframAlpha and parse result."""
        # Load ESM-2 model
        model, alphabet = torch.hub.load("facebookresearch/esm:main", "esm2_t33_650M_UR50D")
        batch_converter = alphabet.get_batch_converter()
        model.eval()  # disables dropout for deterministic results

        # Prepare data (first 2 sequences from ESMStructuralSplitDataset superfamily / 4)
        data = [
            ("protein1", query)
        ]
        try:
            batch_labels, batch_strs, batch_tokens = batch_converter(data)
            batch_lens = (batch_tokens != alphabet.padding_idx).sum(1)

            # Extract per-residue representations (on CPU)
            with torch.no_grad():
                results = model(batch_tokens, repr_layers=[33], return_contacts=True)
            token_representations = results["representations"][33]

            # Generate per-sequence representations via averaging
            # NOTE: token 0 is always a beginning-of-sequence token, so the first residue is token 1.
            sequence_representations = []
            for i, tokens_len in enumerate(batch_lens):
                sequence_representations.append(token_representations[i, 1 : tokens_len - 1].mean(0))
            torch.set_printoptions(threshold=10_000)
            #print(sequence_representations[0][0:10])
            answer = sequence_representations[0][0:10]

        
            
        except:
            return "ESM2 wasn't able to answer it"

        if answer is None or answer == "":
            # We don't want to return the assumption alone if answer is empty
            return "No good ESM2 Result was found"
        else:
            return f"Answer: {answer}"
