from julian.discourse.api.models.model import Model

class Edge(Model):
    REQUIRED_FIELDS = set(['from_node_id', 'to_node_id', 'edge_type_id', 'discourse_id', 'note_id'])
    OPTIONAL_FIELDS = set(['id'])
