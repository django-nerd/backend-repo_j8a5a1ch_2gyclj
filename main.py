import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import (
    SchoolInfo, Department, Teacher, ClassRoom,
    Extracurricular, OsisMember, Event, News, ContactMessage
)

app = FastAPI(title="School Website API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "School API ready"}


# Helper to seed demo data if empty
@app.post("/seed")
def seed_data():
    try:
        # Seed SchoolInfo
        if len(get_documents("schoolinfo")) == 0:
            create_document("schoolinfo", SchoolInfo(
                name="SMA Negeri Nusantara",
                tagline="Berkarakter, Berprestasi, Berbudaya",
                description=(
                    "Sekolah menengah atas dengan fokus pada pengembangan karakter, "
                    "literasi, numerasi, dan prestasi akademik maupun non-akademik."
                ),
                address="Jl. Merdeka No. 123, Kota Harmoni",
                phone="(021) 555-1234",
                email="info@sman-nusantara.sch.id",
                hero_image="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=80&w=1200&auto=format&fit=crop"
            ))
        # Departments
        if len(get_documents("department")) == 0:
            for d in [
                Department(name="IPA", head="Drs. Budi Santoso", description="Ilmu Pengetahuan Alam"),
                Department(name="IPS", head="Dra. Sari Wulandari", description="Ilmu Pengetahuan Sosial"),
                Department(name="Bahasa", head="Drs. Rudi Hartono", description="Bahasa dan Sastra"),
            ]:
                create_document("department", d)
        # Extracurriculars
        if len(get_documents("extracurricular")) == 0:
            for ex in [
                Extracurricular(name="Paskibra", mentor="Pak Andi", schedule="Selasa & Kamis", description="Pasukan Pengibar Bendera", icon="flag"),
                Extracurricular(name="Pramuka", mentor="Bu Rina", schedule="Jumat", description="Gerakan Pramuka", icon="tent"),
                Extracurricular(name="Basket", mentor="Coach Dimas", schedule="Rabu", description="Tim Basket Sekolah", icon="basketball"),
                Extracurricular(name="Karya Ilmiah Remaja", mentor="Bu Maya", schedule="Senin", description="Penelitian Sains", icon="beaker"),
            ]:
                create_document("extracurricular", ex)
        # OSIS
        if len(get_documents("osismember")) == 0:
            for m in [
                OsisMember(name="Nadia Putri", role="Ketua OSIS", class_name="XI IPA 2", photo=None, bio="Mewujudkan OSIS yang aktif dan inspiratif."),
                OsisMember(name="Rafi Akbar", role="Wakil Ketua", class_name="XI IPS 1", photo=None, bio="Kolaboratif, kreatif, dan peduli."),
                OsisMember(name="Siti Rahma", role="Sekretaris", class_name="X IPA 3", photo=None, bio="Tertib administrasi, solid dalam aksi."),
                OsisMember(name="Dimas Arya", role="Bendahara", class_name="XII IPA 1", photo=None, bio="Transparan dan akuntabel."),
            ]:
                create_document("osismember", m)
        # Events
        if len(get_documents("event")) == 0:
            for e in [
                Event(title="Penerimaan Peserta Didik Baru", date="2025-06-10", location="Aula Utama", description="Sosialisasi PPDB 2025", category="school"),
                Event(title="Lomba Sains", date="2025-08-01", location="Lab IPA", description="Kompetisi KIR tingkat kota", category="academic"),
                Event(title="Class Meeting", date="2025-12-15", location="Lapangan", description="Turnamen olahraga antar kelas", category="sport"),
            ]:
                create_document("event", e)
        # News
        if len(get_documents("news")) == 0:
            for n in [
                News(title="Tim Basket Juara I", summary="Prestasi gemilang di kejuaraan daerah.", content="Tim basket SMA Negeri Nusantara meraih juara I...", image=None, author="Humas"),
                News(title="Webinar Literasi Digital", summary="Meningkatkan literasi bagi siswa.", content="Bekerja sama dengan Kominfo...", image=None, author="Humas"),
            ]:
                create_document("news", n)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Public API endpoints
@app.get("/school", response_model=List[SchoolInfo])
def get_school_info():
    return get_documents("schoolinfo")


@app.get("/departments", response_model=List[Department])
def get_departments():
    return get_documents("department")


@app.get("/extracurriculars", response_model=List[Extracurricular])
def get_extracurriculars():
    return get_documents("extracurricular")


@app.get("/osis", response_model=List[OsisMember])
def get_osis_members():
    return get_documents("osismember")


@app.get("/events", response_model=List[Event])
def get_events():
    return get_documents("event")


@app.get("/news", response_model=List[News])
def get_news():
    return get_documents("news")


class ContactIn(ContactMessage):
    pass


@app.post("/contact")
def send_contact(message: ContactIn):
    try:
        create_document("contactmessage", message)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
