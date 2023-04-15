"""
page views for clothes shop

write your clothes shop views here
"""
from typing import Any, Dict

from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

import auth.forms
import auth.models
import market.models


class Wear(generic.DetailView[market.models.Item]):
    """gives an item information"""

    model = market.models.Item
    template_name = 'clothes/wear.html'
    context_object_name = 'item'


class Collection(generic.DetailView[market.models.Collection]):
    """gives an collection information"""

    template_name = 'clothes/collection.html'
    queryset = market.models.Collection.objects.get_items_in_collection()
    context_object_name = 'collection'


class Designer(generic.ListView[market.models.Collection]):
    """Gives information about designer"""

    template_name = 'clothes/designer_detail.html'

    context_object_name = 'collections'

    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """Returns queryset for listview"""
        designer_id = self.kwargs.get('pk')
        designer = auth.models.DesignerProfile.objects.filter(
            pk=designer_id
        ).first()
        return (
            market.models.Collection.objects.get_items_in_collection().filter(
                designer=designer.user
            )
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """returns context data to show forms"""
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        designer_id = self.kwargs.get('pk')
        designer = get_object_or_404(
            auth.models.DesignerProfile, pk=designer_id
        )
        readonly = not self.request.user.id == designer.user.id
        user_form = auth.forms.User_form(
            self.request.POST or None,
            readonly=readonly,
            instance=designer.user,
        )
        designer_form = auth.forms.Designer_profile_form(
            self.request.POST or None, readonly=readonly, instance=designer
        )
        context['user_form'] = user_form
        context['designer_form'] = designer_form
        context['readonly'] = readonly
        return context

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Processing request.POST"""
        context = self.get_context_data(*args, **kwargs)
        designer_id = self.kwargs.get('pk')
        readonly = context['readonly']
        if not readonly:
            user_form = context['user_form']
            designer_form = context['designer_form']
            if user_form.is_valid() and designer_form.is_valid():
                user_form.save()
                designer_form.save(files=request.FILES)
            return redirect(
                reverse_lazy(
                    'clothes:designer_detail', kwargs={'pk': designer_id}
                )
            )
        raise Http404()
