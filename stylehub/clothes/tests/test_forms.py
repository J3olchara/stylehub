"""
clothes forms tests

write your form tests here
"""
import os
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

import clothes.forms
import clothes.models
from market.tests.base import MarketSetUp


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'test_media')
class FilesSetup(TestCase):
    """setups image files for testing"""

    def setUp(self) -> None:
        content_image = (
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00'
        )
        self.image1 = SimpleUploadedFile('test1.jpg', content_image)
        self.image2 = SimpleUploadedFile('test1.jpg', content_image)
        self.image3 = SimpleUploadedFile('test1.jpg', content_image)
        return super().setUp()

    def tearDown(self) -> None:
        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        return super().tearDown()


class TestItem(FilesSetup, MarketSetUp):
    """tests Item forms"""

    def test_creating_item(self):
        """тестирует, может ли дизайнер создать вещь"""
        self.client.login(
            username=self.designer_user.username,
            password=self.designer_password,
        )
        path = reverse('clothes:create', kwargs={'form': 'item'})
        model = clothes.models.Item
        kwargs = {
            model.name.field.name: 'item1name',
            model.cost.field.name: 100,
            model.category.field.name: self.category_extended1.id,
            model.collection.field.name: self.collection1.id,
            model.styles.field.name: [self.style1.id],
            model.gender.field.name: 'male',
            model.text.field.name: '123123t3213312312132231ext',
            model.designer.field.name: self.designer_user.id,
            model.image.field.name: self.image1,
            'gallery': [
                self.image2,
                self.image3,
            ],
        }
        resp = self.client.post(path, data=kwargs)
        self.assertRedirects(
            resp, path, msg_prefix='Дизайнер не может создать Item'
        )

        qs_item = model.objects.filter(
            designer=self.designer_user,
            name=kwargs[model.name.field.name],
            text=kwargs[model.text.field.name],
        )
        self.assertTrue(qs_item.exists(), 'Дизайнер не может создать Item')

        item = qs_item.first()
        item_gallery = clothes.models.ItemPicture.objects.filter(item=item)
        self.assertEqual(item_gallery.count(), 2)


class TestCollection(FilesSetup, MarketSetUp):
    """Tests collection forms"""

    def test_creating_collection(self):
        """тестирует, может ли дизайнер создать коллекцию"""
        self.client.login(
            username=self.designer_user.username,
            password=self.designer_password,
        )
        path = reverse('clothes:create', kwargs={'form': 'collection'})
        model = clothes.models.Collection
        kwargs = {
            model.name.field.name: 'collection1name',
            model.styles.field.name: [self.style1.id],
            model.text.field.name: '123123text',
            model.designer.field.name: self.designer_user.id,
            model.image.field.name: self.image1,
        }
        resp = self.client.post(path, data=kwargs)
        self.assertRedirects(
            resp, path, msg_prefix='Дизайнер не может создать Collection'
        )

        qs_collection = model.objects.filter(
            designer=self.designer_user,
            name=kwargs[model.name.field.name],
            text=kwargs[model.text.field.name],
        )
        self.assertTrue(
            qs_collection.exists(), 'Дизайнер не может создать Collection'
        )
