from julian.discourse.api import node
from julian.discourse.api import note

def find_by_start_date_and_end_date(start_date, end_date):
    notes = note.find_by_start_date_and_end_date(start_date, end_date)
    for n in notes:
        node_list = node.find_stored_by_note_id(n.id)