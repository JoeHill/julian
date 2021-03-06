import discourse

from discourse.api.models.model import Model

class Note(Model):
    REQUIRED_FIELDS = set(['identifier'])
    OPTIONAL_FIELDS = set(['processed', 'id', 'prioritya', 'priorityb', 'priorityc', 'priorityd', 'prioritye', 'created_at', 'updated_at', 'published_at'])
