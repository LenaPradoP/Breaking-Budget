from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Create initial users for Breaking Budget'

    def handle(self, *args, **options):
        # List of users to create
        users_data = [
            {
                'username': 'ana.martinez',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'email': 'ana.martinez@breakingbudget.com',
                'password': 'password123',
                'role': 'traveler'
            },
            {
                'username': 'john.smith',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@breakingbudget.com',
                'password': 'password123',
                'role': 'traveler'
            },
            {
                'username': 'sofia.rodriguez',
                'first_name': 'Sofia',
                'last_name': 'Rodríguez',
                'email': 'sofia.rodriguez@breakingbudget.com',
                'password': 'password123',
                'role': 'traveler'
            },
            {
                'username': 'emily.johnson',
                'first_name': 'Emily',
                'last_name': 'Johnson',
                'email': 'emily.johnson@breakingbudget.com',
                'password': 'password123',
                'role': 'traveler'
            },
            {
                'username': 'elena.fernandez',
                'first_name': 'Elena',
                'last_name': 'Fernández',
                'email': 'elena.fernandez@breakingbudget.com',
                'password': 'password123',
                'role': 'traveler'
            },
            {
                'username': 'roberto.sanchez',
                'first_name': 'Roberto',
                'last_name': 'Sánchez',
                'email': 'roberto.sanchez@breakingbudget.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'sarah.williams',
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'email': 'sarah.williams@breakingbudget.com',
                'password': 'admin123',
                'role': 'admin'
            }
        ]

        # Create each user
        for user_data in users_data:
            # Check if user already exists
            if CustomUser.objects.filter(username=user_data['username']).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {user_data["username"]} already exists, skipping...')
                )
                continue

            # Create the user
            user = CustomUser.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'User {user.username} created successfully')
            )

        self.stdout.write(
            self.style.SUCCESS('All initial users have been created successfully!')
        )