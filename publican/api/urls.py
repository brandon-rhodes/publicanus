from tastypie.api import Api
from . import resources

v1_api = Api(api_name='v1')
v1_api.register(resources.FilingResource())
urlpatterns = v1_api.urls
