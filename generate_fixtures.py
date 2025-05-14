import json
import random

def generate_fixtures():
    # Default password for all users: password123
    fixtures = []
    user_id = 1
    profile_id = 1

    # Indian names
    male_first_names = [
        "Rajesh", "Amit", "Rohit", "Suresh", "Kunal", "Anil", "Ravi", "Vikram", "Sanjay", "Manoj",
        "Mahesh", "Arjun", "Karan", "Ashok", "Sunil"
    ]

    male_last_names = [
        "Sharma", "Verma", "Gupta", "Mehta", "Reddy", "Iyer", "Singh", "Chauhan", "Malhotra", "Kapoor",
        "Jain", "Bansal", "Agarwal", "Patel", "Thakur"
    ]

    female_first_names = [
        "Pooja", "Nisha", "Anita", "Kavita", "Neha", "Ritu", "Sneha", "Priya", "Alka", "Megha",
        "Radhika", "Anjali", "Sunita", "Geeta", "Komal"
    ]

    female_last_names = [
        "Sharma", "Verma", "Gupta", "Mehta", "Reddy", "Iyer", "Singh", "Chauhan", "Malhotra", "Kapoor",
        "Jain", "Bansal", "Agarwal", "Patel", "Thakur"
    ]

    specializations = ["Dermatologist Specialist"]

    cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
    ]

    states = [
        "Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal","Maharashtra", "Gujarat", "Rajasthan", "Uttar Pradesh"
    ]

    # Generate 15 doctors
    for i in range(1, 16):
        # Randomly choose gender for doctor
        gender = random.choice(["male", "female"])
        if gender == "male":
            first_name = random.choice(male_first_names)
            last_name = random.choice(male_last_names)
        else:
            first_name = random.choice(female_first_names)
            last_name = random.choice(female_last_names)

        doctor_username = f"doctor{i}"
        doctor = {
            "model": "accounts.user",
            "fields": {
                "password": "pbkdf2_sha256$260000$HQyGxzxfOxv6nLKI8zF$w9Nmz1Rxm1fPY1HzJ2MU7MgKBfTJ1RfF3q9M1wJvXvQ=",  # "password123"
                "username": doctor_username,
                "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
                "first_name": first_name,
                "last_name": last_name,
                "role": "doctor",
                "is_active": True,
                "date_joined": "2023-01-01T00:00:00Z",
            },
        }
        fixtures.append(doctor)
        
        r = random.randint(0,len(cities)-1)
        # Doctor Profile
        doctor_profile = {
            "model": "accounts.profile",
            "pk": profile_id,
            "fields": {
                "user": user_id,
                "phone": f"+91-98{random.randint(10000000, 99999999)}",
                "dob": f"{random.randint(1960, 1990)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "about": f"MBBS from {random.choice(['AIIMS Delhi', 'CMC Vellore', 'Grant Medical College', 'JIPMER'])}. {random.randint(5, 20)} years of experience in {random.choice(specializations)}.",
                "specialization": random.choice(specializations),
                "gender": gender,
                "address": f"House {random.randint(1, 99)}, Road {random.randint(1, 15)}, {random.choice(['Gandhinagar', 'Indiranagar', 'Jayanagar', 'Connaught Place'])}",
                "city": cities[r],
                "state": states[r],
                "postal_code": f"{random.randint(100000, 999999)}",
                "country": "India",
                "price_per_consultation": random.randint(500, 2000),
                "is_available": True,
            },
        }
        fixtures.append(doctor_profile)
        user_id += 1
        profile_id += 1

    # Write fixtures to file
    with open("fixtures/initial_data.json", "w") as f:
        json.dump(fixtures, f, indent=2)

if __name__ == "__main__":
    generate_fixtures()
