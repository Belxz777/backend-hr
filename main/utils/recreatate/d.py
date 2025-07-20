from django.db import connection

from main.models import LaborCosts

def recreate_table():
  
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(LaborCosts)