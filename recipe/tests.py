from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Recipe


class MainViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        for i in range(7):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description=f'Description {i}',
                instructions=f'Instructions {i}',
                ingredients=f'Ingredients {i}',
                category=self.category
            )

    def test_main_view_status_code(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_main_view_returns_only_5_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(len(response.context['recipes']), 5)

    def test_main_view_returns_latest_recipes(self):
        response = self.client.get(reverse('main'))
        recipes = list(response.context['recipes'])
        for i in range(len(recipes) - 1):
            self.assertGreaterEqual(recipes[i].created_at, recipes[i + 1].created_at)


class CategoryListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cat1 = Category.objects.create(name='Breakfast')
        self.cat2 = Category.objects.create(name='Dinner')
        Recipe.objects.create(
            title='Pancakes', description='...', instructions='...', ingredients='...', category=self.cat1
        )
        Recipe.objects.create(
            title='Soup', description='...', instructions='...', ingredients='...', category=self.cat1
        )
        Recipe.objects.create(
            title='Steak', description='...', instructions='...', ingredients='...', category=self.cat2
        )

    def test_category_list_view_status_code(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_category_list_view_uses_correct_template(self):
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, 'category_list.html')

    def test_category_list_returns_all_categories(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(len(response.context['categories']), 2)

    def test_category_list_has_recipe_count(self):
        response = self.client.get(reverse('category_list'))
        categories = {c.name: c.recipe_count for c in response.context['categories']}
        self.assertEqual(categories['Breakfast'], 2)
        self.assertEqual(categories['Dinner'], 1)