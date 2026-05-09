from ._anvil_designer import navigation_helpersTemplate
from anvil import *
import anvil.server
from routing import router
import m3.components as m3


class navigation_helpers(navigation_helpersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
