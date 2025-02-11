"""Util that calls Stablediffusion."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env
from diffusers import StableDiffusionPipeline



class StablediffusionAPIWrapper(BaseModel):
    """Wrapper for Stable Diffusion.

    Docs for using:

    1. Go to wolfram alpha and sign up for a developer account
    2. Create an app and get your APP ID
    3. Save your APP ID into WOLFRAM_ALPHA_APPID env variable
    4. pip install wolframalpha

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
            print("Importing stablediffusion.")

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
        #res = self.wolfram_client.query(query)
        res = "Always return this sentence."
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        try:
            #assumption = next(res.pods).text
            #answer = next(res.results).text
            prompt = query

            image = pipe(prompt).images[0]
            image.save(f"output.png")
            answer = "Image saved!"
            assumption = "Thinking..."
        except StopIteration:
            return "Stablediffusion wasn't able to answer it"

        if answer is None or answer == "":
            # We don't want to return the assumption alone if answer is empty
            return "No good Stablediffusion Result was found"
        else:
            return f"Assumption: {assumption} \nAnswer: {answer}"
