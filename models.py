import re

class Shape(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.Unicode(80))
    slug             = db.Column(db.String(80),unique=True)
	description      = db.Column(db.UnicodeText)
	center_point_lat = db.Column(db.Float)
	center_point_lon = db.Column(db.Float)
	geojson          = db.Column(db.UnicodeText) 	# http://geojson.org 
	
	def transport_geojson(self,lat,lon):
		updated_geojson = self.geojson
		# This will move the center point of the shape to the new location and return updated geo_json
		"""
		{
		  "type": "Feature",
		  "geometry": {
		    "type": "Point",
		    "coordinates": [125.6, 10.1]
		  },
		  "properties": {
		    "name": "Dinagat Islands"
		  }
		}
		"""
		coordinates = updated_geojson.geometry.coordinates
		new_coordinates = []
		
		# Loop through all the shape's coordinates
		for latlon in coordinates:
			# find the distance from the center
			offset_lat = self.center_point_lat-latlon[0]
			offset_lon = self.center_point_lon-latlon[1]

			# move each point based on the offset to the new center
			new_lat = lat-offset_lat
			new_lon = lat-offset_lon

			# build-up the list
			new_coordinates.append([new_lat,new_lon])

		# update the json before sending it off to be displayed
		updated_geojson.geometry.coordinates = new_coordinates
		
		return updated_geojson
	
	def add_tag(self, tag):
		t = Tag(tag,self.id)
		t.save()
		return
		
	def make_slug(self):
		self.slug = self.name
		# find and replace problematic characters
		self.slug = re.sub('[^a-z0-9-]', '-', self.slug)
		self.slug = re.sub('[-+]', '-', self.slug)
		self.slug = re.sub('[ ]', '_', self.slug)
		return
			
	def __init__(self, name):
		self.name = name
		return
		
    def __repr__(self):
        return '<Name %r>' % self.name



class Tags(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    shape_id = db.Column(db.Integer, ForeignKey=Shape.id)
    name     = db.Column(db.String(80))

    def __init__(self, name, shape_id):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name