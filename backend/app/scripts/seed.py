"""Database seed script for demo data."""

import asyncio
import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory, engine
from app.models import Base
from app.models.organization import Organization
from app.models.user import Role, Permission, RolePermission, User
from app.models.department import Department
from app.models.challenge import Challenge, ChallengeParticipation
from app.models.event import Event
from app.models.reward import Reward, Achievement
from app.models.wellness import WellnessProgram, WellnessGoal
from app.models.activity import ActivityLog
from app.utils.security import hash_password


async def seed():
    """Seed the database with sample data."""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        try:
            # ── Roles ──
            roles_data = [
                {"name": "super_admin", "display_name": "Super Admin", "description": "Full system access", "is_system": True},
                {"name": "hr_admin", "display_name": "HR Admin", "description": "HR management access", "is_system": True},
                {"name": "department_manager", "display_name": "Department Manager", "description": "Department-level access", "is_system": True},
                {"name": "employee", "display_name": "Employee", "description": "Standard employee access", "is_system": True},
            ]
            roles = {}
            for rd in roles_data:
                role = Role(**rd)
                db.add(role)
                roles[rd["name"]] = role
            await db.flush()

            # ── Organization ──
            org = Organization(
                name="Acme Corporation",
                domain="acme.com",
                industry="Technology",
                size_tier="enterprise",
                description="Leading enterprise technology company",
                is_active=True,
                settings={"theme": "default", "timezone": "US/Eastern"},
            )
            db.add(org)
            await db.flush()

            # ── Departments ──
            dept_data = [
                {"name": "Engineering", "code": "ENG"},
                {"name": "Human Resources", "code": "HR"},
                {"name": "Marketing", "code": "MKT"},
                {"name": "Sales", "code": "SLS"},
                {"name": "Finance", "code": "FIN"},
                {"name": "Product", "code": "PRD"},
            ]
            departments = {}
            for dd in dept_data:
                dept = Department(organization_id=org.id, **dd)
                db.add(dept)
                departments[dd["code"]] = dept
            await db.flush()

            # ── Users ──
            users_data = [
                {"email": "admin@acme.com", "first_name": "Sarah", "last_name": "Chen", "role": "super_admin", "dept": "HR", "title": "Platform Administrator", "wellness_score": 92, "reward_points": 1250},
                {"email": "hr@acme.com", "first_name": "Michael", "last_name": "Thompson", "role": "hr_admin", "dept": "HR", "title": "HR Director", "wellness_score": 88, "reward_points": 980},
                {"email": "manager@acme.com", "first_name": "Jessica", "last_name": "Park", "role": "department_manager", "dept": "ENG", "title": "Engineering Manager", "wellness_score": 85, "reward_points": 750},
                {"email": "employee@acme.com", "first_name": "David", "last_name": "Rodriguez", "role": "employee", "dept": "ENG", "title": "Software Engineer", "wellness_score": 78, "reward_points": 620},
                {"email": "alex.wright@acme.com", "first_name": "Alex", "last_name": "Wright", "role": "employee", "dept": "MKT", "title": "Marketing Specialist", "wellness_score": 82, "reward_points": 540},
                {"email": "emma.davis@acme.com", "first_name": "Emma", "last_name": "Davis", "role": "employee", "dept": "SLS", "title": "Sales Representative", "wellness_score": 91, "reward_points": 890},
                {"email": "james.wilson@acme.com", "first_name": "James", "last_name": "Wilson", "role": "employee", "dept": "FIN", "title": "Financial Analyst", "wellness_score": 73, "reward_points": 420},
                {"email": "olivia.martin@acme.com", "first_name": "Olivia", "last_name": "Martin", "role": "employee", "dept": "PRD", "title": "Product Designer", "wellness_score": 87, "reward_points": 710},
                {"email": "ryan.lee@acme.com", "first_name": "Ryan", "last_name": "Lee", "role": "department_manager", "dept": "MKT", "title": "Marketing Director", "wellness_score": 80, "reward_points": 660},
                {"email": "sophia.chen@acme.com", "first_name": "Sophia", "last_name": "Chen", "role": "employee", "dept": "ENG", "title": "Senior Developer", "wellness_score": 95, "reward_points": 1100},
            ]
            users = {}
            for i, ud in enumerate(users_data):
                user = User(
                    email=ud["email"],
                    password_hash=hash_password("Password123!"),
                    first_name=ud["first_name"],
                    last_name=ud["last_name"],
                    employee_id=f"EMP-{1000 + i}",
                    title=ud["title"],
                    wellness_score=ud["wellness_score"],
                    reward_points=ud["reward_points"],
                    organization_id=org.id,
                    department_id=departments[ud["dept"]].id,
                    role_id=roles[ud["role"]].id,
                    is_active=True,
                    is_email_verified=True,
                )
                db.add(user)
                users[ud["email"]] = user
            await db.flush()

            # Set department managers
            departments["ENG"].manager_id = users["manager@acme.com"].id
            departments["MKT"].manager_id = users["ryan.lee@acme.com"].id
            await db.flush()

            # ── Challenges ──
            today = date.today()
            challenges_data = [
                {
                    "title": "10K Steps Challenge",
                    "description": "Walk 10,000 steps every day for 30 days. Track your daily step count and compete with colleagues.",
                    "type": "steps", "status": "active",
                    "start_date": today - timedelta(days=10),
                    "end_date": today + timedelta(days=20),
                    "target_value": 300000, "metric_unit": "steps",
                    "reward_points": 500, "max_participants": 50,
                },
                {
                    "title": "Mindfulness Marathon",
                    "description": "Practice meditation or mindfulness for at least 15 minutes daily for 21 days.",
                    "type": "mindfulness", "status": "active",
                    "start_date": today - timedelta(days=5),
                    "end_date": today + timedelta(days=16),
                    "target_value": 315, "metric_unit": "minutes",
                    "reward_points": 300, "max_participants": 100,
                },
                {
                    "title": "Nutrition Tracker",
                    "description": "Log your meals and maintain a balanced diet for 14 days.",
                    "type": "nutrition", "status": "active",
                    "start_date": today, "end_date": today + timedelta(days=14),
                    "target_value": 42, "metric_unit": "meals",
                    "reward_points": 200,
                },
                {
                    "title": "Team Fitness Sprint",
                    "description": "Team-based exercise challenge. Log at least 150 minutes of exercise per week as a team.",
                    "type": "exercise", "status": "draft",
                    "start_date": today + timedelta(days=7),
                    "end_date": today + timedelta(days=37),
                    "target_value": 600, "metric_unit": "minutes",
                    "reward_points": 400, "is_team_challenge": True,
                },
            ]
            challenges = []
            for cd in challenges_data:
                is_team = cd.pop("is_team_challenge", False)
                challenge = Challenge(
                    organization_id=org.id,
                    created_by=users["hr@acme.com"].id,
                    is_team_challenge=is_team,
                    **cd,
                )
                db.add(challenge)
                challenges.append(challenge)
            await db.flush()

            # ── Challenge Participations ──
            import random
            for challenge in challenges[:3]:  # Active challenges
                participants = random.sample(list(users.values()), min(6, len(users)))
                for user in participants:
                    progress = random.uniform(0, challenge.target_value * 0.8)
                    cp = ChallengeParticipation(
                        user_id=user.id,
                        challenge_id=challenge.id,
                        progress_value=round(progress, 1),
                        status="active",
                        points_earned=int(progress / challenge.target_value * challenge.reward_points) if challenge.target_value > 0 else 0,
                    )
                    db.add(cp)
            await db.flush()

            # ── Events ──
            now = datetime.now(timezone.utc)
            events_data = [
                {
                    "title": "Yoga and Stretching Workshop",
                    "description": "Join our certified yoga instructor for a rejuvenating session focused on flexibility and stress relief.",
                    "type": "fitness_class",
                    "status": "upcoming",
                    "start_time": now + timedelta(days=3, hours=10),
                    "end_time": now + timedelta(days=3, hours=11),
                    "location": "Wellness Room, Floor 2",
                    "capacity": 30,
                    "reward_points": 50,
                },
                {
                    "title": "Nutrition Masterclass: Meal Prep",
                    "description": "Learn efficient meal preparation techniques for a healthier work week from our nutrition expert.",
                    "type": "workshop",
                    "status": "upcoming",
                    "start_time": now + timedelta(days=7, hours=12),
                    "end_time": now + timedelta(days=7, hours=13, minutes=30),
                    "location": "Conference Room A",
                    "capacity": 25,
                    "reward_points": 40,
                },
                {
                    "title": "Annual Health Screening",
                    "description": "Comprehensive health screening including blood pressure, cholesterol, and BMI assessment.",
                    "type": "health_screening",
                    "status": "upcoming",
                    "start_time": now + timedelta(days=14, hours=9),
                    "end_time": now + timedelta(days=14, hours=17),
                    "location": "Medical Suite, Floor 1",
                    "capacity": 100,
                    "reward_points": 100,
                },
                {
                    "title": "Stress Management Webinar",
                    "description": "Online session on managing workplace stress, building resilience, and maintaining work-life balance.",
                    "type": "webinar",
                    "status": "upcoming",
                    "start_time": now + timedelta(days=5, hours=14),
                    "end_time": now + timedelta(days=5, hours=15),
                    "virtual_link": "https://meet.nutritrack360.in/stress-mgmt",
                    "capacity": 200,
                    "reward_points": 30,
                },
            ]
            for ed in events_data:
                event = Event(
                    organization_id=org.id,
                    created_by=users["hr@acme.com"].id,
                    registered_count=0,
                    **ed,
                )
                db.add(event)
            await db.flush()

            # ── Rewards ──
            rewards_data = [
                {"name": "Premium Gym Membership (1 Month)", "description": "One month pass to any partner gym facility.", "category": "experience", "points_required": 500, "quantity_available": 20},
                {"name": "Wellness Gift Box", "description": "Curated gift box with aromatherapy, healthy snacks, and fitness accessories.", "category": "merchandise", "points_required": 300, "quantity_available": 50},
                {"name": "Charity Donation", "description": "Donate your points to a health-related charity of your choice.", "category": "donation", "points_required": 100},
                {"name": "Extra PTO Day", "description": "Earn an additional paid time off day.", "category": "experience", "points_required": 1000, "quantity_available": 10},
                {"name": "Healthy Meal Delivery (1 Week)", "description": "One week of healthy meal deliveries to your office or home.", "category": "gift_card", "points_required": 400, "quantity_available": 30},
                {"name": "Fitness Tracker Device", "description": "Premium fitness tracking wristband.", "category": "merchandise", "points_required": 800, "quantity_available": 15},
            ]
            for rd in rewards_data:
                reward = Reward(organization_id=org.id, **rd)
                db.add(reward)
            await db.flush()

            # ── Wellness Programs ──
            programs_data = [
                {"name": "Corporate Fitness Initiative", "description": "Comprehensive fitness program including gym access, group classes, and personal training.", "category": "fitness", "status": "active"},
                {"name": "Mental Wellness Support", "description": "Access to counseling, meditation apps, and stress management resources.", "category": "mental_health", "status": "active"},
                {"name": "Nutrition Advisory Program", "description": "Personalized nutrition guidance, meal planning, and dietary assessments.", "category": "nutrition", "status": "active"},
            ]
            for pd in programs_data:
                program = WellnessProgram(organization_id=org.id, **pd)
                db.add(program)
            await db.flush()

            # ── Sample Activities ──
            for user in list(users.values())[:5]:
                for day_offset in range(14):
                    activity_date = today - timedelta(days=day_offset)
                    steps = random.randint(3000, 15000)
                    activity = ActivityLog(
                        user_id=user.id,
                        activity_type="steps",
                        activity_date=activity_date,
                        value=float(steps),
                        unit="steps",
                        points_earned=steps // 1000,
                    )
                    db.add(activity)

                    if random.random() > 0.5:
                        exercise_mins = random.randint(15, 60)
                        exercise = ActivityLog(
                            user_id=user.id,
                            activity_type="exercise",
                            activity_date=activity_date,
                            value=float(exercise_mins),
                            unit="minutes",
                            duration_minutes=exercise_mins,
                            calories_burned=exercise_mins * random.randint(5, 10),
                            points_earned=exercise_mins // 30 * 5,
                        )
                        db.add(exercise)
            await db.flush()

            # ── Achievements ──
            achievements_data = [
                {"name": "First Steps", "description": "Complete your first activity log", "icon": "footprints", "category": "fitness", "criteria_type": "challenge_count", "criteria_value": 1, "points_reward": 10},
                {"name": "Week Warrior", "description": "Log activities for 7 consecutive days", "icon": "flame", "category": "consistency", "criteria_type": "streak_days", "criteria_value": 7, "points_reward": 50},
                {"name": "Challenge Champion", "description": "Complete 5 challenges", "icon": "trophy", "category": "fitness", "criteria_type": "challenge_count", "criteria_value": 5, "points_reward": 100},
                {"name": "Social Butterfly", "description": "Attend 3 wellness events", "icon": "users", "category": "social", "criteria_type": "challenge_count", "criteria_value": 3, "points_reward": 75},
                {"name": "Point Master", "description": "Earn 1000 reward points", "icon": "star", "category": "consistency", "criteria_type": "points_earned", "criteria_value": 1000, "points_reward": 200},
            ]
            for ad in achievements_data:
                achievement = Achievement(**ad)
                db.add(achievement)
            await db.flush()

            await db.commit()
            print("Database seeded successfully!")
            print("\nDemo credentials:")
            print("  Super Admin:  admin@acme.com / Password123!")
            print("  HR Admin:     hr@acme.com / Password123!")
            print("  Manager:      manager@acme.com / Password123!")
            print("  Employee:     employee@acme.com / Password123!")

        except Exception as e:
            await db.rollback()
            print(f"Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
