from django.test import TestCase
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.__str__(), 'Test Category')

    def test_category_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_update_category_name(self):
        self.category.name = 'Updated Test Category'
        self.category.save()
        self.assertEqual(self.category.name, 'Updated Test Category')

    def test_delete_category(self):
        self.category.delete()
        self.assertEqual(Category.objects.count(), 0)


class ImageModelTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2')
        self.image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.image = Image.objects.create(
            title='Test Image',
            image=self.image_file,
            created_date=date.today(),
            age_limit=18
        )
        self.image.categories.add(self.category1, self.category2)

    def test_image_creation(self):
        self.assertIsInstance(self.image, Image)
        self.assertEqual(self.image.__str__(), 'Test Image')
        self.assertEqual(self.image.title, 'Test Image')
        self.assertEqual(self.image.created_date, date.today())
        self.assertEqual(self.image.age_limit, 18)

    def test_image_categories(self):
        self.assertIn(self.category1, self.image.categories.all())
        self.assertIn(self.category2, self.image.categories.all())

    def test_image_title_max_length(self):
        max_length = self.image._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_update_image_title(self):
        self.image.title = 'Updated Test Image'
        self.image.save()
        self.assertEqual(self.image.title, 'Updated Test Image')

    def test_delete_image(self):
        image_id = self.image.id
        self.image.delete()
        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=image_id)

    def test_remove_category_from_image(self):
        self.image.categories.remove(self.category1)
        self.assertNotIn(self.category1, self.image.categories.all())

    def test_image_without_categories(self):
        self.image.categories.clear()
        self.assertEqual(self.image.categories.count(), 0)

    def test_image_add_multiple_categories(self):
        category3 = Category.objects.create(name='Test Category 3')
        self.image.categories.add(category3)
        self.assertIn(category3, self.image.categories.all())
