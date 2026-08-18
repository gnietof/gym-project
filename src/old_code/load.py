"""
This module includes pieces of code which where used to move data from JSON files
into the Postgres database
"""

import calendar
import json
import os

import psycopg2
from dotenv import load_dotenv
from pydantic import BaseModel


class RawActivity(BaseModel):
    activity_name: str
    category: str
    sub_category: str
    description: str
    intensity_level: str
    target_age_group: str
    weights_used: bool
    primary_benefit: str
    skill_level: str
    impact_level: str
    social_dynamic: str
    caloric_burn: str
    mental_focus: str
    contraindications: str
    interesting_fact: str


class Description(BaseModel):
    activity_name: str
    category: str
    sub_category: str
    description: str
    intensity_level: list[str]
    target_age_group: str
    weights_used: bool
    primary_benefit: str
    skill_level: list[str]
    impact_level: str
    social_dynamic: str
    caloric_burn: str
    mental_focus: str
    contraindications: str
    interesting_fact: str


def update_activities(path: str, connection: any):
    if not connection:
        print("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append((activity["code"].upper(), activity["name"]))

    try:
        query = """
          UPDATE GYM.ACTIVITIES260812 
          SET ACTIVITY_CODE = %s
          WHERE ACTIVITY_NAME = %s;
        """

        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        print(f"Successfully update {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        print(f"Database error: {e}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")


def insert_activities(path: str, connection: any):
    if not connection:
        print("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append(
            (
                activity["activity_name"],
                activity["category"],
                activity["sub_category"],
                activity["description"],
                activity["intensity_level"],
                activity["target_age_group"],
                activity["weights_used"],
                activity["primary_benefit"],
                activity["skill_level"],
                activity["impact_level"],
                activity["social_dynamic"],
                activity["caloric_burn"],
                activity["mental_focus"],
                activity["contraindications"],
                activity["interesting_fact"],
            )
        )

    cursor = True

    try:
        query = """
          INSERT INTO GYM.RAW_ACTIVITIES(ACTIVITY_NAME,CATEGORY,SUB_CATEGORY,
          DESCRIPTION,INTENSITY_LEVEL,TARGET_AGE_GROUP,WEIGHTS_USED,
          PRIMARY_BENEFIT,SKILL_LEVEL,IMPACT_LEVEL,SOCIAL_DYNAMIC,
          CALORIC_BURN,MENTAL_FOCUS,CONTRAINDICATIONS,INTERESTING_FACT)
          VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        print(f"Successfully inserted {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        print(f"Database error: {e}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")


def connect_database() -> any:
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASSWORD")
    db_database = os.environ.get("DB_DATABASE")
    db_port = os.environ.get("DB_PORT", "5432")

    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_database,
            user=db_user,
            password=db_pass,
            port=db_port,
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")


def insert_sessions(path: str, connection: any):
    if not connection:
        print("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        sessions = json.load(file)

    days = [calendar.day_name[-1]] + list(calendar.day_name[:-1])

    records = []
    for session in sessions:
        records.append(
            (
                session["code"].upper(),
                session["time"],
                session["day"],
                days.index(session["day"].title()),
            )
        )

    cursor = True

    try:
        query = """
          INSERT INTO GYM.SESSIONS(ACTIVITY_CODE,TIME,DOW,DAY)
          VALUES(%s,%s,%s,%s);
        """
        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        print(f"Successfully inserted {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        print(f"Database error: {e}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")


def update_sessions(path: str, connection: any):
    if not connection:
        print("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append((activity["duration"], activity["code"].upper()))

    try:
        query = """
          UPDATE GYM.SESSIONS 
          SET DURATION = %s
          WHERE ACTIVITY_CODE = %s;
        """

        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        print(f"Successfully updated {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        print(f"Database error: {e}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")


def new_activities(path: str, connection: any):
    if not connection:
        print("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append(
            ("TRUE" if activity["new"] else "FALSE", activity["code"].upper())
        )

    try:
        query = """
          UPDATE GYM.ACTIVITIES 
          SET IS_NEW = %s
          WHERE ACTIVITY_CODE = %s;
        """

        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        print(f"Successfully updated {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        print(f"Database error: {e}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")


load_dotenv()
connection = connect_database()
# insert_activities("resources/GymActivities.json", connection)
# update_activities("resources/activities.json", connection)
# insert_sessions("resources/sessions.json", connection)
# update_sessions("resources/activities.json", connection)

new_activities("resources/activities.json", connection)
