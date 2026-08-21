"""
This module includes the code required to create all the tables needed, initializing
them with data and inserting all the activity information as well as generating the
required embeddings.
"""

import json
import logging
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import MinTimeLoggingConnection, execute_values
from sqlalchemy import select

from ai_services.gemini import embed
from common.db.database import SessionLocal
from config_log import setup_logging
from schemas.activity import Embedding


def execute_sql(connection: PgConnection, path: str):
    if not connection:
        logger.error("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        sql = file.read()
        statements = [s.strip() for s in sql.split(";") if s.strip()]

    with connection.cursor() as cursor:
        try:
            for statement in statements:
                cursor.execute(statement + ";")
            connection.commit()

        except psycopg2.ProgrammingError as e:
            connection.rollback()
            print(f"Database error: {e}")

        except psycopg2.Error as e:
            connection.rollback()
            print(f"Database error: {e}")


def insert_descriptions(connection: PgConnection, path: str):
    if not connection:
        logger.error("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        descriptions = json.load(file)

    records = []
    for description in descriptions:
        records.append(
            (
                description["activity_name"],
                description["category"],
                description["sub_category"],
                description["description"],
                description["intensity_level"],
                description["target_age_group"],
                description["weights_used"],
                description["primary_benefit"],
                description["skill_level"],
                description["impact_level"],
                description["social_dynamic"],
                description["caloric_burn"],
                description["mental_focus"],
                description["contraindications"],
                description["interesting_fact"],
            )
        )

    cursor = True

    try:
        query = """
          INSERT INTO GYM.TMP_DESCRIPTIONS(ACTIVITY_NAME,CATEGORY,SUB_CATEGORY,
          DESCRIPTION,INTENSITY_LEVEL,TARGET_AGE_GROUP,WEIGHTS_USED,
          PRIMARY_BENEFIT,SKILL_LEVEL,IMPACT_LEVEL,SOCIAL_DYNAMIC,
          CALORIC_BURN,MENTAL_FOCUS,CONTRAINDICATIONS,INTERESTING_FACT)
          VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        logger.info(f"Successfully inserted {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        connection.rollback()
        logger.error(f"Database programming error: {e}")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Database error: {e}")


def insert_activities(connection: PgConnection, path: str):
    if not connection:
        logger.error("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append(
            (
                activity["code"].upper(),
                activity["name"],
                activity["duration"],
                activity["new"],
            )
        )

    cursor = True

    try:
        delete = """
          TRUNCATE GYM.TMP_ACTIVITIES
        """
        insert = """
          INSERT INTO GYM.TMP_ACTIVITIES(CODE,NAME,DURATION,NEW)
          VALUES %s;
        """
        cursor = connection.cursor()
        cursor.execute(delete)
        execute_values(cursor, insert, records)
        connection.commit()
        print(f"Successfully inserted {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        connection.rollback()
        logger.error(f"Database programming error: {e}")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Database error: {e}")


def insert_sessions(connection: PgConnection, path: str):
    if not connection:
        logger.error("No DB connection provided!")
        return

    with open(path, "r", encoding="utf-8") as file:
        activities = json.load(file)

    records = []
    for activity in activities:
        records.append(
            (
                activity["time"],
                activity["day"],
                activity["code"].upper(),
            )
        )

    cursor = True

    try:
        delete = """
          TRUNCATE GYM.TMP_SESSIONS
        """
        insert = """
          INSERT INTO GYM.TMP_SESSIONS(TIME,DAY,CODE)
          VALUES %s;
        """
        cursor = connection.cursor()
        cursor.execute(delete)
        execute_values(cursor, insert, records)
        connection.commit()
        logger.info(f"Successfully inserted {len(records)} records.")

    except psycopg2.ProgrammingError as e:
        connection.rollback()
        logger.error(f"Database programming error: {e}")

    except psycopg2.Error as e:
        connection.rollback()
        logger.error(f"Database error: {e}")


def generate_emebddings():

    logger.info("Starting embeddings generation.")

    with SessionLocal() as db:
        query = select(Embedding).where(Embedding.embedding == None)

        descriptions = db.scalars(query).all()

        if not descriptions:
            logger.info("All activities already have embeddings")
            return

    updated_count = 0
    for description in descriptions:
        response = embed(description.content, "gemini-embedding-001")
        description.embedding = response.embeddings[0].values
        updated_count += 1

    connection.commit()
    logger.info(f"{updated_count} documents embedded.")


def connect_database() -> PgConnection | None:
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
            connection_factory=MinTimeLoggingConnection,
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        return None


setup_logging(logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
connection = connect_database()
connection.initialize(logger)

# # CAUTION: This script deletes all tables.
# --->execute_sql(connection, "init/clean.sql")

# # 1. Create the required tables
# execute_sql(connection, "init/create.sql")
# # 2.1 Ingest all the description for all the activities in a temporary table
# insert_descriptions(connection, "resources/GymActivities.json")
# # 2.2 Ingest all the activities details in this gym
# insert_activities(connection, "resources/activities.json")
# # 2.3 Ingest all the session details in this gym
# insert_sessions(connection, "resources/sessions.json")
# # 3. Initialize the contents of the auxiliary tables
# execute_sql(connection, "init/init.sql")
# # 4. Initialize the contents of the auxiliary tables
# execute_sql(connection, "init/fill.sql")
# # 5. Embeddings are being added to the embeddings table
# generate_emebddings()
# # 6. Add basic prompts
execute_sql(connection, "init/prompts.sql")
# 7. Add test questions
# execute_sql(connection, "init/questions.sql")
