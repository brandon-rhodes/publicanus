from tastypie.api import Api

v1_api = Api(api_name='v1')
urlpatterns = v1_api.urls
