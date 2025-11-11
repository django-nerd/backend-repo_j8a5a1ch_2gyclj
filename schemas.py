"""
Database Schemas for School Website

Each Pydantic model below maps to a MongoDB collection with the lowercase
of the class name as the collection name.

Examples:
- SchoolInfo -> "schoolinfo"
- Department -> "department"
- OsisMember -> "osismember"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class SchoolInfo(BaseModel):
    name: str = Field(..., description="School name")
    tagline: Optional[str] = Field(None, description="Short tagline")
    description: str = Field(..., description="About the school")
    address: str = Field(..., description="School address")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Public contact email")
    hero_image: Optional[str] = Field(None, description="Hero image URL")


class Department(BaseModel):
    name: str = Field(..., description="Department name")
    head: Optional[str] = Field(None, description="Head of department")
    description: Optional[str] = Field(None, description="Department details")


class Teacher(BaseModel):
    name: str = Field(..., description="Teacher full name")
    subject: str = Field(..., description="Primary subject")
    department: Optional[str] = Field(None, description="Department name")
    photo: Optional[str] = Field(None, description="Photo URL")
    bio: Optional[str] = Field(None, description="Short bio")


class ClassRoom(BaseModel):
    name: str = Field(..., description="Class identifier, e.g., X IPA 1")
    level: int = Field(..., ge=7, le=12, description="Grade level")
    homeroom_teacher: Optional[str] = Field(None, description="Homeroom teacher name")


class Extracurricular(BaseModel):
    name: str = Field(..., description="Club or extracurricular name")
    mentor: Optional[str] = Field(None, description="Mentor/coach")
    schedule: Optional[str] = Field(None, description="Meeting schedule")
    description: Optional[str] = Field(None, description="Activity details")
    icon: Optional[str] = Field(None, description="Icon name for UI")


class OsisMember(BaseModel):
    name: str = Field(..., description="Member name")
    role: str = Field(..., description="Position in OSIS")
    class_name: Optional[str] = Field(None, description="Class, e.g., XI IPA 2")
    photo: Optional[str] = Field(None, description="Photo URL")
    bio: Optional[str] = Field(None, description="Short bio or vision")


class Event(BaseModel):
    title: str = Field(..., description="Event title")
    date: str = Field(..., description="Date string for simplicity")
    location: Optional[str] = Field(None, description="Event location")
    description: Optional[str] = Field(None, description="Event details")
    category: Optional[str] = Field(None, description="Category: school/osis/academic/sport")


class News(BaseModel):
    title: str = Field(..., description="News headline")
    summary: Optional[str] = Field(None, description="Short summary")
    content: str = Field(..., description="Full content")
    image: Optional[str] = Field(None, description="Cover image URL")
    author: Optional[str] = Field(None, description="Author name")


class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr
    message: str = Field(..., min_length=5, description="Message body")
