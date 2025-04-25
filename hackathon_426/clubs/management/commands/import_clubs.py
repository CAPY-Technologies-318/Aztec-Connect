import csv
from django.core.management.base import BaseCommand
from clubs.models import Club

class Command(BaseCommand):
    help = 'Import SDSU clubs from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to your CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        created_count = 0

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = self.clean(row.get('Name'))
                if not name:
                    continue

                category = self.clean(row.get('Type'))
                if category not in dict(Club.CATEGORY_CHOICES):
                    category = 'Other'  # fallback for unrecognized categories

                club, created = Club.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'description': self.clean(row.get('Purpose')),
                        'meeting_time': self.clean(row.get('Meeting Day')),
                        'meeting_location': self.clean(row.get('Meeting Location')),
                        'website': self.clean(row.get('Website')),
                        # logo and banner use model defaults
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Created: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"• Skipped (already exists): {name}"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete. {created_count} clubs created."))

    def clean(self, text):
        return ' '.join(text.split()) if text else ''
