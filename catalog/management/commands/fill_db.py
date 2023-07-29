import json
from pathlib import Path
from typing import List, Type

from django.core.management import BaseCommand
from django.db import connection, models
from django.db.utils import IntegrityError

from catalog.models import Category, Product, Contact


class Command(BaseCommand):
    """
    Custom Django management command to fill the DB with data
    from a JSON file.
    """

    help = (
        'Fill DB with data from catalog/data/test_datatest_data.json '
        'or with specified using \'-p\' or \'--filepath\' parameter'
    )

    def add_arguments(self, parser):
        """
        Add command-line arguments for the management command.
        """
        parser.add_argument(
            '-p',
            '--filepath',
            type=Path,
            help='Path to file containing data',
        )

    def truncate_and_restart_sequence(self, model: Type[models.Model]):
        """
        Truncate the table associated with the model and restart its
        sequence.
        """
        model.objects.all().delete()
        table_name = model._meta.db_table
        sequence_name = f'{table_name}_id_seq'
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully reset auto-incrementing sequence '
                f'for {model.__name__}'
            )
        )

    def handle(self, *args, **kwargs):
        """
        Handle the management command execution.

        """

        self.truncate_and_restart_sequence(Category)
        self.truncate_and_restart_sequence(Product)
        self.truncate_and_restart_sequence(Contact)

        filename: Path = kwargs['filepath']

        if not filename:
            filename = Path('catalog/data/test_data.json')

        category_mapping: dict = {}
        product_list: List[dict] = []
        contact_list: List[dict] = []
        products_to_create: List[Product] = []

        with open(filename, 'r') as f:
            data: dict = json.load(f)

        for item in data:
            if item['model'] == 'catalog.category':
                try:
                    category = Category(**item['fields'])
                    category.save()
                    category_mapping[item['pk']] = category
                except IntegrityError:
                    print(
                        {
                            'error': "IntegrityError",
                            'message': "Duplicate value"
                        }
                    )

            if item['model'] == 'catalog.product':
                product_list.append(item['fields'])

            if item['model'] == 'catalog.contact':
                contact_list.append(item['fields'])

        for product in product_list:
            try:
                category_id = product.pop('category')
                product['category'] = category_mapping[category_id]
                products_to_create.append(Product(**product))
            except KeyError as e:
                print(
                    {
                        'error': "KeyError",
                        'message': str(e)
                    }
                )
        try:
            Product.objects.bulk_create(products_to_create)
        except IntegrityError:
            print(
                {
                    'error': "IntegrityError",
                    'message': "Duplicate value"
                }
            )

        for contact in contact_list:
            Contact.objects.create(**contact)
