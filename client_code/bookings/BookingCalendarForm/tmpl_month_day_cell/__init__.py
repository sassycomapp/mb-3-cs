from ._anvil_designer import tmpl_month_day_cellTemplate
from anvil import *
import anvil.server
from routing import router
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class tmpl_month_day_cell(tmpl_month_day_cellTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
