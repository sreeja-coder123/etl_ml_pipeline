import pytest, json
from app import create_app

@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test.db")
    from app.db import init_db
    init_db(app)
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_generate_pipeline_valid(client):
    payload = {
        "table_name": "orders",
        "source_type": "postgres",
        "volume_gb": 2.5,
        "update_frequency_hrs": 24,
        "num_columns": 30,
        "has_joins": 1,
        "priority": 2
    }
    r = client.post("/generate-pipeline",
        data=json.dumps(payload),
        content_type="application/json")
    assert r.status_code == 200
    data = r.get_json()
    assert "yaml_config" in data
    assert "pipeline_type" in data
    assert "run_id" in data

def test_generate_pipeline_missing_fields(client):
    r = client.post("/generate-pipeline",
        data=json.dumps({"table_name": "t1"}),
        content_type="application/json")
    assert r.status_code == 400

def test_generate_pipeline_no_body(client):
    r = client.post("/generate-pipeline")
    assert r.status_code == 400

def test_lineage(client):
    r = client.get("/lineage")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_rollback(client):
    payload = {"table_name":"x","source_type":"mysql",
               "volume_gb":1,"update_frequency_hrs":24}
    r1 = client.post("/generate-pipeline",
        data=json.dumps(payload), content_type="application/json")
    run_id = r1.get_json()["run_id"]
    r2 = client.post(f"/rollback/{run_id}")
    assert r2.status_code == 200