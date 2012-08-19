"""Tastypie resource objects."""

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from ..engine import models


class PublicanAuthorization(Authorization):

    def apply_limits(self, request, query):

        if request.company is None:
            return query.none()
        account = request.company.account

        if issubclass(query.model, models.Account):
            return query.filter(id=account.id)

        if issubclass(query.model, models.Filing):
            return query.filter(filer_id=account.id)

        return query.none()


class AccountResource(ModelResource):
    class Meta:
        queryset = models.Account.objects.all()
        authorization = PublicanAuthorization()


class FilingResource(ModelResource):
    filer = fields.ForeignKey(AccountResource, 'filer')

    class Meta:
        queryset = models.Filing.objects.all()
        authorization = PublicanAuthorization()
