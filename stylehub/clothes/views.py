"""
page views for clothes shop

write your clothes shop views here
"""
from typing import Any, Dict, Optional

from django.contrib.auth import mixins
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

import auth.forms
import auth.models
import clothes.models


class Wear(generic.DetailView[clothes.models.Item]):
    """gives an item information"""

    template_name = 'clothes/wear.html'
    context_object_name = 'item'
    queryset = clothes.models.Item.objects.get_details()


class Collection(generic.DetailView[clothes.models.Collection]):
    """gives a collection information"""

    template_name = 'clothes/collection.html'
    queryset = clothes.models.Collection.objects.get_items_in_collection()
    context_object_name = 'collection'


class Designer(generic.ListView[clothes.models.Collection]):
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
            clothes.models.Collection.objects.get_items_in_collection().filter(
                designer=designer.user
            )
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """returns context data to show forms"""
        context = super().get_context_data(
            object_list=self.get_queryset(), **kwargs
        )
        designer_id = self.kwargs.get('pk')
        designer = get_object_or_404(
            auth.models.DesignerProfile, pk=designer_id
        )
        readonly = not self.request.user.id == designer.user.id
        user_form = auth.forms.UserForm(
            self.request.POST or None,
            readonly=readonly,
            instance=designer.user,
        )
        designer_form = auth.forms.DesignerProfileForm(
            self.request.POST or None, readonly=readonly, instance=designer
        )
        context['user_form'] = user_form
        context['designer_form'] = designer_form
        context['readonly'] = readonly
        return context

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """Processing request.POST"""
        context = self.get_context_data(**kwargs)
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


class Recommend(generic.ListView[clothes.models.Collection]):
    """gives a popular collections based on user seen history"""

    template_name = 'clothes/recommend.html'
    context_object_name = 'collections'

    def get_queryset(self) -> QuerySet[Any]:
        """get popular collections queryset"""
        return clothes.models.Collection.objects.recommend(self.request.user)


class Orders(
    mixins.LoginRequiredMixin, generic.ListView[clothes.models.Collection]
):
    """gives a user orders"""

    template_name = 'clothes/orders.html'
    context_object_name = 'orders'
    login_url = '/admin/'

    def get_queryset(self) -> QuerySet[Any]:
        """get user orders queryset"""
        user = self.request.user
        return clothes.models.OrderClothes.objects.get_user_orders(user)


class Lovely(mixins.LoginRequiredMixin, generic.ListView[clothes.models.Item]):
    """gives a lovely user designers"""

    template_name = 'clothes/lovely.html'
    context_object_name = 'designers'
    login_url = 'admin/'

    def get_queryset(self) -> Optional[AbstractUser]:
        """Returns designers"""
        user = self.request.user
        return auth.models.User.objects.get_lovely_designers(user)
