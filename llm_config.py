from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"), override=True)

USE_PROVIDER = os.environ.get("USE_PROVIDER")

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL")
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL")

providers_dict = {
    "google": ChatGoogleGenerativeAI(model=GOOGLE_MODEL),
    "anthropic": ChatAnthropic(model=ANTHROPIC_MODEL)
    }

model = providers_dict[USE_PROVIDER]
