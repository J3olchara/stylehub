"""
page views for clothes shop

write your clothes shop views here
"""
from typing import Any, Dict

from django.contrib.auth import mixins
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

import auth.forms
import auth.mixins
import auth.models
import clothes.forms
import clothes.models


class Main(generic.TemplateView):
    """
    MAIN STYLEHUB PAGE

    there are popular designers and collections and unpopular designers
    that we want to popularize
    """

    template_name = 'clothes/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['designers'] = auth.models.User.designers.top()[:10].all()
        context['collections'] = clothes.models.Collection.objects.top()[
            :5
        ].all()
        context['unpopular'] = (
            clothes.models.Item.objects.unpopular().order_by('?')[:20].all()
        )
        return context


class PopularCollections(generic.ListView[clothes.models.Collection]):
    """returns popular collections based on their count of buys"""

    paginate_by = 10
    template_name = 'clothes/collections.html'
    queryset = clothes.models.Collection.objects.top()[
        : paginate_by * 15
    ].all()
    context_object_name = 'collectionsp'


class PopularDesigners(generic.ListView[auth.models.User]):
    """returns popular designers based on their count of buys"""

    paginate_by = 20
    template_name = 'clothes/designers.html'
    queryset = auth.models.User.designers.top()[: paginate_by * 15].all()
    context_object_name = 'designersp'


class UnpopularItems(generic.ListView[clothes.models.Item]):
    """
    returns unpopular items paginator based on designer count of bought items
    """

    paginate_by = 40
    template_name = 'clothes/items.html'
    queryset = (
        clothes.models.Item.objects.unpopular()
        .order_by('?')[: paginate_by * 15]
        .all()
    )
    context_object_name = 'itemsp'


class Wear(generic.DetailView[clothes.models.Item]):
    """gives an item information"""

    template_name = 'clothes/wear.html'
    context_object_name = 'item'
    queryset = clothes.models.Item.objects.get_details()


class Collection(generic.DetailView[clothes.models.Collection]):
    """gives a collection information"""

    template_name = 'clothes/collection.html'
    queryset = clothes.models.Collection.objects.with_items()
    context_object_name = 'collection'


class Designer(generic.ListView[clothes.models.Collection]):
    """Gives information about designer"""

    template_name = 'clothes/designer_detail.html'

    context_object_name = 'collections'

    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """Returns queryset for listview"""
        designer_id = self.kwargs.get('pk')
        designer = auth.models.User.designers.get_designer_with_collections(
            designer_id
        )
        return (
            clothes.models.Collection.objects.with_items()
            .filter(designer=designer)
            .order_by(f'-{clothes.models.Collection.created.field.name}')
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
                reverse_lazy('clothes:designer', kwargs={'pk': designer_id})
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


class Lovely(mixins.LoginRequiredMixin, generic.ListView[auth.models.User]):
    """gives a lovely user designers"""

    template_name = 'clothes/lovely.html'
    context_object_name = 'designers'
    login_url = 'admin/'

    def get_queryset(self) -> QuerySet[Any]:
        """Returns designers"""
        user = self.request.user
        return auth.models.User.objects.get_lovely_designers(user)


class CreateSomething(
    auth.mixins.DesignerRequiredMixin, generic.CreateView[Any, Any]
):
    """view to create some designer models"""

    template_name = 'core/formpage.html'
    forms = {
        'collection': clothes.forms.CollectionCreateForm,
        'item': clothes.forms.ItemCreateForm,
    }

    def get_form_class(self) -> Any:
        """getting form class by froms variable"""
        requested_form = self.kwargs.get('form')
        form = self.forms.get(requested_form)
        if form:
            return form
        raise Http404()

    def get_form_kwargs(self) -> Dict[str, Any]:
        """custom return kwargs to return designer object for form"""
        kwargs = super().get_form_kwargs()
        kwargs['designer'] = self.request.user
        return kwargs

    def form_valid(
        self,
        form: Any,
    ) -> Any:
        """custom form_valid to save item gallery"""
        gallery = self.request.FILES.getlist('gallery')
        if gallery:
            form.save(files=gallery)
        else:
            form.save()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        """returns success url"""
        return self.request.path


class Saved(mixins.LoginRequiredMixin, generic.ListView[clothes.models.Item]):
    """gives saved user items"""

    template_name = 'clothes/liked.html'
    context_object_name = 'items'
    login_url = 'admin/'

    def get_queryset(self) -> QuerySet[Any]:
        """returns items(clothes)"""
        user = self.request.user
        return auth.models.User.objects.get_saved_items(user)
