from fastapi import FastAPI, HTTPException, Header, Depends
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="Gym Management API")

API_KEY = os.environ.get("API_KEY", "supersecret123")

DB_CONFIG = {
    "host": "postgres",
    "dbname": "gymdb",
    "user": "gymuser",
    "password": "gympassword",
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def check_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")

@app.get("/members")
def list_members():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM member ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/classes")
def list_classes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT c.id, c.name, c.trainer_name, c.day_time, c.capacity,
               COUNT(b.id) AS booking_count
        FROM class c
        LEFT JOIN booking b ON b.class_id = c.id
        GROUP BY c.id
        ORDER BY c.id;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/members/{member_id}/bookings")
def member_bookings(member_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT b.id, b.booking_date, c.name AS class_name, c.day_time
        FROM booking b
        JOIN class c ON c.id = b.class_id
        WHERE b.member_id = %s;
    """, (member_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.post("/members", dependencies=[Depends(check_api_key)])
def create_member(name: str, phone: str, membership_type: str, membership_end_date: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO member (name, phone, membership_type, membership_end_date) VALUES (%s, %s, %s, %s) RETURNING id;",
        (name, phone, membership_type, membership_end_date)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Member created"}

@app.post("/classes", dependencies=[Depends(check_api_key)])
def create_class(name: str, trainer_name: str, day_time: str, capacity: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO class (name, trainer_name, day_time, capacity) VALUES (%s, %s, %s, %s) RETURNING id;",
        (name, trainer_name, day_time, capacity)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Class created"}

@app.post("/bookings", dependencies=[Depends(check_api_key)])
def create_booking(member_id: int, class_id: int, booking_date: str):
    conn = get_connection()
    cur = conn.cursor()

    # Check capacity
    cur.execute("SELECT capacity FROM class WHERE id = %s;", (class_id,))
    class_row = cur.fetchone()
    if class_row is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Class not found")
    capacity = class_row[0]

    cur.execute("SELECT COUNT(*) FROM booking WHERE class_id = %s;", (class_id,))
    current_count = cur.fetchone()[0]

    if current_count >= capacity:
        cur.close()
        conn.close()
        raise HTTPException(status_code=409, detail="Class is fully booked")

    cur.execute(
        "INSERT INTO booking (member_id, class_id, booking_date) VALUES (%s, %s, %s) RETURNING id;",
        (member_id, class_id, booking_date)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Booking created"}

@app.delete("/bookings/{booking_id}", dependencies=[Depends(check_api_key)])
def cancel_booking(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM booking WHERE id = %s;", (booking_id,))
    conn.commit()
    deleted = cur.rowcount
    cur.close()
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking cancelled"}
