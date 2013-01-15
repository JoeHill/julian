from julian.discourse.api.models.model import Model

class Node(Model):
    REQUIRED_FIELDS = set(['title'])
    OPTIONAL_FIELDS = set(['id'])
