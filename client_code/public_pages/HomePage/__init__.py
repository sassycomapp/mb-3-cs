from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
from routing import router
import m3.components as m3


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
