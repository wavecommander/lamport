from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg
from psycopg import Error
import json
from datetime import datetime

# Initialize FastAPI application
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection settings
DB_HOST = "localhost"
DB_NAME = "benw"
DB_USER = "postgres"
DB_PASSWORD = ""

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    async def connect(self):
        try:
            self.connection = await psycopg.AsyncConnection.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST
            )
            self.cursor = await self.connection.cursor()
        except Error as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    
    async def disconnect(self):
        if self.cursor:
            await self.cursor.close()
        if self.connection:
            await self.connection.close()

# Pydantic models for request/response validation
class TeamMember(BaseModel):
    given_name: str
    surname: str
    full_name: str
    preferred_name: Optional[str]
    preferred_system_username: str
    preferred_pronouns: Optional[str]
    public_visibility: Optional[int]

class PersonalInfoFragment(BaseModel):
    team_member_id: int
    personal_info_type: str
    personal_info_value: str
    public_visibility: Optional[int]

class FormSubmission(BaseModel):
    submitter: int
    status: Optional[int]
    reviewer: Optional[int]
    datetime_creation: Optional[datetime]
    datetime_modified: Optional[datetime]

# Dependency for database connection
async def get_db():
    db = Database()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

# Team Member Endpoints
@app.post("/team-members", response_model=TeamMember)
async def create_team_member(team_member: TeamMember, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            INSERT INTO team_member (
                given_name, surname, full_name, preferred_name,
                preferred_system_username, preferred_pronouns, public_visibility
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            team_member.given_name, team_member.surname, team_member.full_name,
            team_member.preferred_name, team_member.preferred_system_username,
            team_member.preferred_pronouns, team_member.public_visibility
        ))
        await db.connection.commit()
        team_member_id = await db.cursor.fetchone()[0]
        return {**team_member.dict(), "id": team_member_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create team member: {str(e)}")

@app.get("/team-members/{team_member_id}", response_model=TeamMember)
async def get_team_member(team_member_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            SELECT * FROM team_member WHERE id = %s
        """, (team_member_id,))
        result = await db.cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Team member not found")
        return {
            "id": result[0],
            "given_name": result[1],
            "surname": result[2],
            "full_name": result[3],
            "preferred_name": result[4],
            "preferred_system_username": result[5],
            "preferred_pronouns": result[6],
            "public_visibility": result[7]
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/team-members/{team_member_id}", response_model=TeamMember)
async def update_team_member(team_member_id: int, team_member: TeamMember, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            UPDATE team_member SET
                given_name = %s,
                surname = %s,
                full_name = %s,
                preferred_name = %s,
                preferred_system_username = %s,
                preferred_pronouns = %s,
                public_visibility = %s
            WHERE id = %s RETURNING id
        """, (
            team_member.given_name, team_member.surname, team_member.full_name,
            team_member.preferred_name, team_member.preferred_system_username,
            team_member.preferred_pronouns, team_member.public_visibility,
            team_member_id
        ))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        return {**team_member.dict(), "id": team_member_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update team member: {str(e)}")

@app.delete("/team-members/{team_member_id}")
async def delete_team_member(team_member_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("DELETE FROM team_member WHERE id = %s", (team_member_id,))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        return JSONResponse(status_code=200, content={"message": "Team member deleted successfully"})
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete team member: {str(e)}")

# Personal Info Fragment Endpoints
@app.post("/personal-info-fragments", response_model=PersonalInfoFragment)
async def create_personal_info_fragment(fragment: PersonalInfoFragment, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            INSERT INTO personal_info_fragment (
                team_member_id, personal_info_type, personal_info_value, public_visibility
            ) VALUES (
                %s, %s, %s, %s
            ) RETURNING id
        """, (
            fragment.team_member_id,
            fragment.personal_info_type,
            fragment.personal_info_value,
            fragment.public_visibility
        ))
        await db.connection.commit()
        fragment_id = await db.cursor.fetchone()[0]
        return {**fragment.dict(), "id": fragment_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create personal info fragment: {str(e)}")

@app.get("/personal-info-fragments/{fragment_id}", response_model=PersonalInfoFragment)
async def get_personal_info_fragment(fragment_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            SELECT * FROM personal_info_fragment WHERE id = %s
        """, (fragment_id,))
        result = await db.cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Personal info fragment not found")
        return {
            "id": result[0],
            "team_member_id": result[1],
            "personal_info_type": result[2],
            "personal_info_value": result[3],
            "public_visibility": result[4]
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/personal-info-fragments/{fragment_id}", response_model=PersonalInfoFragment)
async def update_personal_info_fragment(fragment_id: int, fragment: PersonalInfoFragment, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            UPDATE personal_info_fragment SET
                team_member_id = %s,
                personal_info_type = %s,
                personal_info_value = %s,
                public_visibility = %s
            WHERE id = %s RETURNING id
        """, (
            fragment.team_member_id,
            fragment.personal_info_type,
            fragment.personal_info_value,
            fragment.public_visibility,
            fragment_id
        ))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Personal info fragment not found")
        return {**fragment.dict(), "id": fragment_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update personal info fragment: {str(e)}")

@app.delete("/personal-info-fragments/{fragment_id}")
async def delete_personal_info_fragment(fragment_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("DELETE FROM personal_info_fragment WHERE id = %s", (fragment_id,))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Personal info fragment not found")
        return JSONResponse(status_code=200, content={"message": "Personal info fragment deleted successfully"})
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete personal info fragment: {str(e)}")

# Form Submission Endpoints
@app.post("/form-submissions", response_model=FormSubmission)
async def create_form_submission(submission: FormSubmission, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            INSERT INTO form_submission (
                submitter, status, reviewer, datetime_creation, datetime_modified
            ) VALUES (
                %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            submission.submitter,
            submission.status,
            submission.reviewer,
            submission.datetime_creation,
            submission.datetime_modified
        ))
        await db.connection.commit()
        submission_id = await db.cursor.fetchone()[0]
        return {**submission.dict(), "id": submission_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create form submission: {str(e)}")

@app.get("/form-submissions/{submission_id}", response_model=FormSubmission)
async def get_form_submission(submission_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            SELECT * FROM form_submission WHERE id = %s
        """, (submission_id,))
        result = await db.cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Form submission not found")
        return {
            "id": result[0],
            "submitter": result[1],
            "status": result[2],
            "reviewer": result[3],
            "datetime_creation": result[4],
            "datetime_modified": result[5]
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/form-submissions/{submission_id}", response_model=FormSubmission)
async def update_form_submission(submission_id: int, submission: FormSubmission, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("""
            UPDATE form_submission SET
                submitter = %s,
                status = %s,
                reviewer = %s,
                datetime_creation = %s,
                datetime_modified = %s
            WHERE id = %s RETURNING id
        """, (
            submission.submitter,
            submission.status,
            submission.reviewer,
            submission.datetime_creation,
            submission.datetime_modified,
            submission_id
        ))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Form submission not found")
        return {**submission.dict(), "id": submission_id}
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update form submission: {str(e)}")

@app.delete("/form-submissions/{submission_id}")
async def delete_form_submission(submission_id: int, db: Database = Depends(get_db)):
    try:
        await db.cursor.execute("DELETE FROM form_submission WHERE id = %s", (submission_id,))
        await db.connection.commit()
        if await db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Form submission not found")
        return JSONResponse(status_code=200, content={"message": "Form submission deleted successfully"})
    except Error as e:
        await db.connection.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete form submission: {str(e)}")