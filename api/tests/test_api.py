import httpx

BASE_URL = "http://localhost:8000"
API_KEY = "supersecret123"


def test_get_members_returns_200():
    response = httpx.get(f"{BASE_URL}/members")
    assert response.status_code == 200


def test_get_classes_returns_200_and_has_booking_count():
    response = httpx.get(f"{BASE_URL}/classes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "booking_count" in data[0]


def test_post_member_without_api_key_is_rejected():
    response = httpx.post(
        f"{BASE_URL}/members",
        params={
            "name": "Test User",
            "phone": "0000000000",
            "membership_type": "Monthly",
            "membership_end_date": "2026-12-31",
        },
    )
    assert response.status_code == 401


def test_post_member_with_valid_api_key_succeeds():
    response = httpx.post(
        f"{BASE_URL}/members",
        params={
            "name": "Test User",
            "phone": "0000000000",
            "membership_type": "Monthly",
            "membership_end_date": "2026-12-31",
        },
        headers={"x-api-key": API_KEY},
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_booking_rejected_when_class_is_full():
    
    class_response = httpx.post(
        f"{BASE_URL}/classes",
        params={
            "name": "Tiny Class",
            "trainer_name": "Test Trainer",
            "day_time": "Mon 10:00",
            "capacity": 1,
        },
        headers={"x-api-key": API_KEY},
    )
    class_id = class_response.json()["id"]

    member_response = httpx.post(
        f"{BASE_URL}/members",
        params={
            "name": "Member One",
            "phone": "111",
            "membership_type": "Monthly",
            "membership_end_date": "2026-12-31",
        },
        headers={"x-api-key": API_KEY},
    )
    member1_id = member_response.json()["id"]

    member2_response = httpx.post(
        f"{BASE_URL}/members",
        params={
            "name": "Member Two",
            "phone": "222",
            "membership_type": "Monthly",
            "membership_end_date": "2026-12-31",
        },
        headers={"x-api-key": API_KEY},
    )
    member2_id = member2_response.json()["id"]

    
    first_booking = httpx.post(
        f"{BASE_URL}/bookings",
        params={"member_id": member1_id, "class_id": class_id, "booking_date": "2026-08-20"},
        headers={"x-api-key": API_KEY},
    )
    assert first_booking.status_code == 200

    
    second_booking = httpx.post(
        f"{BASE_URL}/bookings",
        params={"member_id": member2_id, "class_id": class_id, "booking_date": "2026-08-20"},
        headers={"x-api-key": API_KEY},
    )
    assert second_booking.status_code == 409
