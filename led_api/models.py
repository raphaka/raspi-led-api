from marshmallow import fields
from ast import literal_eval

from led_api import db, ma

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        color_json = {
           'id':self.id,
           'name':self.name,
           'value':self.value
        }
        return color_json

class ColorSchema(ma.ModelSchema):
    class Meta:
        model = Color

class Effect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        effect_json = {
           'id':self.id,
           'name':self.name,
           'value':self.value
        }
        return effect_json

class EffectSchema(ma.ModelSchema):
    class Meta:
        model = Effect

    value = fields.Method("deserialize_value")

    #return list from str representation of list
    def deserialize_value(self, value):
        return literal_eval(value.value)
