"""Tastypie resource objects."""

from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from ..engine import filings, models


class PublicanAuthorization(Authorization):

    def apply_limits(self, request, query):
        if request.company is None:
            return query.none()
        account = request.company.account

        if issubclass(query.model, filings.Filing):
            return query.filter(filer_id=account.id)

        return query.none()


class FilingResource(ModelResource):
    class Meta:
        queryset = models.Filing.objects.all()
        authorization = PublicanAuthorization()
