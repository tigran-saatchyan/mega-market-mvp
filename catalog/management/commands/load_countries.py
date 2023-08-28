import json
from pathlib import Path

from django.core.management import BaseCommand

from users.models import Country


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        filename: Path = Path('catalog/data/countries.json')
        with open(filename, 'r') as json_file:
            countries_data = json.load(json_file)
            for country_data in countries_data:
                Country.objects.create(
                    name=country_data['name'],
                    code=country_data['code']
                )
