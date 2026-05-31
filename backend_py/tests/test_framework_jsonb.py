from app.api.frameworks_shared import coerce_json_value, save_framework_to_db


class FakeSession:
    def __init__(self):
        self.added = None

    def add(self, obj):
        self.added = obj

    def commit(self):
        pass

    def refresh(self, obj):
        pass


def test_coerce_json_value_accepts_jsonb_and_legacy_text():
    assert coerce_json_value({"title": "Native"}, {}) == {"title": "Native"}
    assert coerce_json_value('[{"id": "step-1"}]', []) == [{"id": "step-1"}]
    assert coerce_json_value(None, []) == []
    assert coerce_json_value("not-json", {}) == {}


def test_save_framework_to_db_assigns_native_json_values():
    db = FakeSession()
    framework_data = {
        "metadata": {"title": "JSONB Framework", "version": "1.0.0"},
        "steps": [{"id": "step-1"}],
        "artefacts": {"additional": [{"name": "Brief"}]},
        "risks": [],
        "escalation": [],
        "raw": {"kept": True},
        "family": "Technology",
        "confidence": 91.0,
        "pov": "operator",
    }

    saved = save_framework_to_db(
        framework_data=framework_data,
        metadata_dict={"source": "unit"},
        creator_id="user_test",
        db=db,
    )

    assert saved is db.added
    assert saved.metadata_json == framework_data["metadata"]
    assert saved.steps_json == framework_data["steps"]
    assert saved.artefacts_json == framework_data["artefacts"]
    assert saved.risks_json == []
    assert saved.escalation_json == []
    assert saved.raw_framework_json == framework_data
    assert saved.raw_metadata_json == {"source": "unit"}
