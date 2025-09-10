from datetime import date as dt_date
from decimal import Decimal

from django.core.management.base import BaseCommand
from users.models import CustomUser
from expenses.models import Expense

class Command(BaseCommand):
    help = "Create initial expenses for Breaking Budget (DateField, using 'user' as user PK)."

    def handle(self, *args, **options):
        # List of dicts: 'user' is the USER PK (1..7); 'date' is YYYY-MM-DD
        expenses_data = [
            {"user": 1, "date": "2025-09-01", "status": "pending",  "category": "flight",         "amount": "350.00", "description": "Flight BCN→LHR"},
            {"user": 1, "date": "2025-09-03", "status": "approved", "category": "food",           "amount": "24.50",  "description": "Lunch at airport"},
            {"user": 2, "date": "2025-09-02", "status": "pending",  "category": "hotel",          "amount": "189.00", "description": "1 night hotel"},
            {"user": 2, "date": "2025-09-05", "status": "rejected", "category": "transportation", "amount": "18.00",  "description": "Taxi to office"},
            {"user": 3, "date": "2025-09-01", "status": "approved", "category": "train",          "amount": "42.00",  "description": "Train to city"},
            {"user": 3, "date": "2025-09-06", "status": "pending",  "category": "food",           "amount": "12.00",  "description": "Coffee & snack"},
            {"user": 4, "date": "2025-09-04", "status": "approved", "category": "car",            "amount": "75.00",  "description": "Car rental fuel"},
            {"user": 4, "date": "2025-09-07", "status": "pending",  "category": "other",          "amount": "9.99",   "description": "SIM card"},
            {"user": 5, "date": "2025-09-02", "status": "approved", "category": "transportation", "amount": "3.20",   "description": "Metro ticket"},
            {"user": 5, "date": "2025-09-05", "status": "pending",  "category": "hotel",          "amount": "210.00", "description": "2 nights hotel"},
            {"user": 6, "date": "2025-09-03", "status": "rejected", "category": "food",           "amount": "55.00",  "description": "Team dinner"},
            {"user": 6, "date": "2025-09-06", "status": "approved", "category": "car",            "amount": "40.00",  "description": "Parking"},
            {"user": 7, "date": "2025-09-01", "status": "pending",  "category": "train",          "amount": "28.00",  "description": "Regional train"},
            {"user": 7, "date": "2025-09-07", "status": "approved", "category": "flight",         "amount": "420.00", "description": "Return flight"},
            {"user": 7, "date": "2025-09-07", "status": "rejected", "category": "hotel",         "amount": "220.00", "description": "3 nights hotel"},
            {"user": 9, "date": "2025-09-07", "status": "pending", "category": "flight",         "amount": "50.00", "description": "BCN - MAD"},
            {"user": 9, "date": "2025-09-07", "status": "approved", "category": "hotel",         "amount": "20.00", "description": "2 nights hotel"},
            {"user": 9, "date": "2025-09-07", "status": "rejected", "category": "car",         "amount": "100.00", "description": "2 days car"},
        ]

        created = 0
        skipped = 0

        for row in expenses_data:
            # fetch CustomUser instance by PK stored in 'user'
            uid = row["user"]
            user = CustomUser.objects.filter(pk=uid).first()
            if not user:
                self.stdout.write(self.style.WARNING(f"User {uid} not found, skipping: {row}"))
                skipped += 1
                continue

            # parse date (YYYY-MM-DD for DateField)
            date_obj = dt_date.fromisoformat(row["date"])

            amount = Decimal(row["amount"])
            status = row["status"]
            category = row["category"]
            desc = row.get("description", "")

            # skip if an identical record already exists
            if Expense.objects.filter(user=user, date=date_obj, amount=amount, description=desc).exists():
                self.stdout.write(self.style.WARNING(
                    f'Skipping duplicate for user {uid}: {date_obj} {amount} "{desc}"'
                ))
                skipped += 1
                continue

            Expense.objects.create(
                user=user,
                date=date_obj,
                status=status,
                category=category,
                amount=amount,
                description=desc,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(
                f"Created expense for user {uid}: {date_obj} {category} {amount}"
            ))

        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Skipped: {skipped}"))
