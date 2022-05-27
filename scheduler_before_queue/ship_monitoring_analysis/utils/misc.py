import hashlib
import fiona
from shapely.geometry import shape


def md5sum(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def single_feature_geojson_to_shapely(geojson_file):
    with fiona.open(geojson_file, 'r') as features:
        first_feature = features[0]
        shapely_geometry = shape(first_feature['geometry'])
    return shapely_geometry
