from database import SessionLocal
from models import DbDoctor

doctors_data = [
    {
        "name": "Dr. Richard James",
        "about": "Dr. James is dedicated to providing high-quality healthcare with a focus on preventative care and early diagnosis.",
        "address": {
            "line1": "24 Main Street",
            "line2": "10 Clause Road"
        },
        "degree": "MBBS",
        "experience": "4 Years",
        "fees": 50,
        "image": "https://mighty.tools/mockmind-api/content/human/65.jpg",
        "speciality": {
            "title": "Cardiology",
            "icon": "faHeartPulse"
        },
        "available": True
    },
    {
        "name": "Dr. Sarah White",
        "about": "Dr. White specializes in cardiovascular health and is committed to patient education and prevention.",
        "address": {
            "line1": "100 Health Blvd",
            "line2": "Suite 20"
        },
        "degree": "MD, Cardiology",
        "experience": "8 Years",
        "fees": 75,
        "image": "https://mighty.tools/mockmind-api/content/human/44.jpg",
        "speciality": {
            "title": "Urology",
            "icon": "faUserMd"
        },
        "available": True
    },
    {
        "name": "Dr. Emma Brown",
        "about": "Dr. Brown is an expert in skin care, specializing in treatments for common and complex skin issues.",
        "address": {
            "line1": "50 Maple Ave",
            "line2": "2nd Floor"
        },
        "degree": "MD, Dermatology",
        "experience": "6 Years",
        "fees": 60,
        "image": "https://mighty.tools/mockmind-api/content/human/57.jpg",
        "speciality": {
            "title": "Dental Care",
            "icon": "faTooth"
        },
        "available": False
    },
    {
        "name": "Dr. John Smith",
        "about": "Dr. Smith has extensive experience in treating musculoskeletal issues and focuses on minimally invasive techniques.",
        "address": {
            "line1": "1 Recovery Rd",
            "line2": "Room 305"
        },
        "degree": "MBBS, MS (Ortho)",
        "experience": "10 Years",
        "fees": 100,
        "image": "https://mighty.tools/mockmind-api/content/human/5.jpg",
        "speciality": {
            "title": "Neurology",
            "icon": "faBrain"
        },
        "available": True
    },
    {
        "name": "Dr. Alice Grey",
        "about": "Dr. Grey is passionate about children's health, providing preventive care and treatment for young patients.",
        "address": {
            "line1": "76 Kids Care Lane",
            "line2": ""
        },
        "degree": "MBBS, MD (Pediatrics)",
        "experience": "7 Years",
        "fees": 55,
        "image": "https://mighty.tools/mockmind-api/content/human/7.jpg",
        "speciality": {
            "title": "Eye Care",
            "icon": "faEye"
        },
        "available": True
    },
    {
        "name": "Dr. Kevin Lee",
        "about": "Dr. Lee specializes in neurological disorders and is dedicated to comprehensive patient care.",
        "address": {
            "line1": "123 Neuro Street",
            "line2": "Suite 45"
        },
        "degree": "MD, Neurology",
        "experience": "12 Years",
        "fees": 120,
        "image": "https://mighty.tools/mockmind-api/content/human/68.jpg",
        "speciality": {
            "title": "Cardiology",
            "icon": "faHeartPulse"
        },
        "available": True
    },
    {
        "name": "Dr. Lisa Ray",
        "about": "Dr. Ray provides expert care in eye health, focusing on both treatment and preventive measures.",
        "address": {
            "line1": "88 Vision Road",
            "line2": "Office 101"
        },
        "degree": "MBBS, MD (Ophthalmology)",
        "experience": "9 Years",
        "fees": 70,
        "image": "https://mighty.tools/mockmind-api/content/human/60.jpg",
        "speciality": {
            "title": "Eye Care",
            "icon": "faEye"
        },
        "available": False
    },
    {
        "name": "Dr. Mark Liu",
        "about": "Dr. Liu treats hormonal imbalances and is committed to helping patients achieve a balanced life.",
        "address": {
            "line1": "3 Wellness Ave",
            "line2": "Building B"
        },
        "degree": "MD, Endocrinology",
        "experience": "5 Years",
        "fees": 80,
        "image": "https://mighty.tools/mockmind-api/content/human/49.jpg",
        "speciality": {
            "title": "Urology",
            "icon": "faUserMd"
        },
        "available": True
    },
    {
        "name": "Dr. Nora Williams",
        "about": "Dr. Williams is dedicated to women's health, providing a range of treatments and preventive care.",
        "address": {
            "line1": "200 Women's Health Road",
            "line2": "Floor 3"
        },
        "degree": "MBBS, MD (Gynecology)",
        "experience": "11 Years",
        "fees": 90,
        "image": "https://mighty.tools/mockmind-api/content/human/43.jpg",
        "speciality": {
            "title": "Neurology",
            "icon": "faBrain"
        },
        "available": True
    },
    {
        "name": "Dr. Robert King",
        "about": "Dr. King specializes in cancer treatment, offering personalized care and comprehensive support.",
        "address": {
            "line1": "500 Hope Blvd",
            "line2": "Room 21A"
        },
        "degree": "MD, Oncology",
        "experience": "15 Years",
        "fees": 150,
        "image": "https://mighty.tools/mockmind-api/content/human/41.jpg",
        "speciality": {
            "title": "Plastic Surgery",
            "icon": "faSyringe"
        },
        "available": False
    }
]


def seed_doctors():
    db = SessionLocal()
    try:
        # Check if doctors already exist
        existing_doctors = db.query(DbDoctor).count()
        if existing_doctors > 0:
            print("Doctors data already exists. Skipping seeding.")
            return

        # Create doctor instances
        for doctor_data in doctors_data:
            db_doctor = DbDoctor(**doctor_data)
            db.add(db_doctor)

        db.commit()
        print("Successfully seeded doctors data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding doctors: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_doctors()
