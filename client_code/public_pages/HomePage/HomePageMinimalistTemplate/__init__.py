from ._anvil_designer import HomePageMinimalistTemplateTemplate
from anvil import *
import anvil.server
from routing import router
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class HomePageMinimalistTemplate(HomePageMinimalistTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
