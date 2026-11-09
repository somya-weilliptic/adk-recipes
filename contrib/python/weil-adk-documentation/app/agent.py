"""Entry point for the recipe: the docs updater is the root agent.

The release analyzer is a second, independent agent in
``app/adk_release_analyzer``; run it with
``python -m app.adk_release_analyzer.main``.
"""

from google.adk.apps import App

from app.adk_docs_updater.agent import root_agent as docs_updater_agent

root_agent = docs_updater_agent

app = App(root_agent=root_agent, name="app")
