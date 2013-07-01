from discourse.api.models.model import Model

class Node(Model):
    REQUIRED_FIELDS = set(['title', 'note_id'])
    OPTIONAL_FIELDS = set(['id'])
