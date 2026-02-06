import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing Health...")
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✅ Health OK")

def test_decks():
    print("Testing Decks CRUD...")
    # Create
    r = requests.post(f"{BASE_URL}/decks", json={"name": "Test Deck", "description": "A test deck"})
    assert r.status_code == 200
    deck = r.json()
    deck_id = deck['id']
    print(f"✅ Created Deck: {deck_id}")

    # Get All
    r = requests.get(f"{BASE_URL}/decks")
    assert r.status_code == 200
    assert len(r.json()) >= 1
    print("✅ Get Decks OK")

    # Update
    r = requests.put(f"{BASE_URL}/decks/{deck_id}", json={"name": "Updated Deck"})
    assert r.status_code == 200
    assert r.json()['name'] == "Updated Deck"
    print("✅ Update Deck OK")

    return deck_id

def test_cards(deck_id):
    print("Testing Cards CRUD...")
    # Create
    r = requests.post(f"{BASE_URL}/cards", json={
        "deck_id": deck_id,
        "front_title": "Test Card",
        "back_content": "This is a test prompt."
    })
    assert r.status_code == 200
    card = r.json()
    card_id = card['id']
    print(f"✅ Created Card: {card_id}")

    # Duplicate
    r = requests.post(f"{BASE_URL}/cards/{card_id}/duplicate")
    assert r.status_code == 200
    assert "(Copy)" in r.json()['front_title']
    print("✅ Duplicate Card OK")

    # Delete
    r = requests.delete(f"{BASE_URL}/cards/{card_id}")
    assert r.status_code == 204
    print("✅ Delete Card OK")

if __name__ == "__main__":
    try:
        test_health()
        d_id = test_decks()
        test_cards(d_id)
        print("\n🎉 ALL BACKEND TESTS PASSED")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
