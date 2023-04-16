""" prepare db to managers tests """

import clothes.models
from market.tests.base import MarketSetUp


class ClothesSetup(MarketSetUp):
    """ setup db clothes models """
    def setUp(self) -> None:
        """ setup method """
        super().setUp()
        self.order = clothes.models.OrderClothes.objects.create(
            user=self.user,
            designer=self.designer_user,
            item=self.item1,
            sum=1200,
        )
        self.order1 = clothes.models.OrderClothes.objects.create(
            user=self.user,
            designer=self.designer_user,
            item=self.item2,
            sum=self.item2.cost,
        )
