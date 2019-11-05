from led_controller import db

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
