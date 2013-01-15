from django.db import models

class Note(models.Model):
    identifier = models.TextField(default='')
    prioritya = models.TextField(default='')
    priorityb = models.TextField(default='')
    priorityc = models.TextField(default='')
    priorityd = models.TextField(default='')
    prioritye = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    processed = models.BooleanField(default=False)

class Discourse(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Node(models.Model):
    title = models.CharField(max_length=255)

class EdgeType(models.Model):
    title = models.CharField(max_length=255)

class Edge(models.Model):
    from_node_id = models.BigIntegerField()
    to_node_id = models.BigIntegerField()
    edge_type = models.ForeignKey(EdgeType)
    discourse = models.ForeignKey(Discourse)
    note = models.ForeignKey(Note)
