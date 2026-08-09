import json
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
import os

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

class Activity(BaseModel):
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

def insert_json(path:str, connection: any):
  if not connection:
    print("No DB connection provided!")
    return

  with open(path,"r",encoding="utf-8") as file:
    activities = json.load(file)

  records = []
  for activity in activities:
    records.append((activity["activity_name"],activity["category"],activity["sub_category"],
                   activity["description"],activity["intensity_level"],activity["target_age_group"],
                   activity["weights_used"],activity["primary_benefit"],activity["skill_level"],
                   activity["impact_level"],activity["social_dynamic"],activity["caloric_burn"],
                   activity["mental_focus"],activity["contraindications"],activity["interesting_fact"]))

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
    cursor.executemany(query,records)
    connection.commit()
    print(f"Successfully inserted {len(records)} records.")

  except Exception as e:
    print(f"Database error: {e}")


def connect_database() -> any:
  db_host = os.environ.get("DB_HOST")
  db_user = os.environ.get("DB_USER")
  db_pass = os.environ.get("DB_PASSWORD")
  db_database = os.environ.get("DB_DATABASE")
  db_port = os.environ.get("DB_PORT","5432") 

  try: 
    connection = psycopg2.connect(
      host=db_host,
      database=db_database,
      user=db_user,
      password=db_pass,
      port=db_port
    )  
    return connection
  except Exception as e:
    print(f"Database connection error: {e}")


load_dotenv()
connection = connect_database()
insert_json("resources/GymActivities.json",connection)
