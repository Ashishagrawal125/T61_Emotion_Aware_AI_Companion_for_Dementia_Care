from services.memory_service import MemoryService

def test_memory_service_roundtrip(tmp_path):
    db_path = tmp_path / "memory.db"
    service = MemoryService(str(db_path))
    service.save_memory("Aashi", "favorite_color", "blue")
    memories = service.get_memories("Aashi")
    assert len(memories) == 1
    assert memories[0]["key"] == "favorite_color"
