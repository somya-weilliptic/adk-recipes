from dotenv import load_dotenv

# Load variables from .env if present. In production the environment is
# already populated by the platform (Cloud Run, GKE, etc.), so a missing
# .env is expected and not an error.
load_dotenv()

# Uncomment when using Weil identities (add a noqa for E402 to it):
# from . import agent
