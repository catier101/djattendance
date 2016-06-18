from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
from django.template import Library
from django.utils.encoding import smart_text

register = Library()

from django.core.serializers.json import Serializer

class JSONSerializer(Serializer):
  def get_dump_object(self, obj):
    model = self._current
    model['id'] = smart_text(obj._get_pk_val(), strings_only=True)
    return model

s = JSONSerializer()

def jsonify(object):
  if isinstance(object, QuerySet):
    return s.serialize(object)
  return json.dumps(object)

register.filter('jsonify', jsonify)