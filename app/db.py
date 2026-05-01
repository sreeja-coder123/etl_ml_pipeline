import sqlite3, json
from datetime import datetime
from flask import g

def get_db(app):
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                pipeline_type TEXT NOT NULL,
                yaml_config TEXT NOT NULL,
                schema_input TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'generated',
                rolled_back INTEGER DEFAULT 0
            )
        """)
        db.commit()
        db.close()

def log_pipeline(app, schema, pipeline_type, yaml_config):
    db = sqlite3.connect(app.config["DATABASE"])
    cursor = db.execute(
        """INSERT INTO pipeline_runs
           (table_name, source_type, pipeline_type, yaml_config, schema_input)
           VALUES (?,?,?,?,?)""",
        (schema.get("table_name","unknown"),
         schema.get("source_type","unknown"),
         pipeline_type, yaml_config,
         json.dumps(schema))
    )
    run_id = cursor.lastrowid
    db.commit()
    db.close()
    return run_id

def rollback_pipeline(app, run_id):
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute("UPDATE pipeline_runs SET rolled_back=1, status='rolled_back' WHERE id=?",
               (run_id,))
    db.commit()
    db.close()

def get_lineage(app):
    db = sqlite3.connect(app.config["DATABASE"])
    rows = db.execute(
        "SELECT id, table_name, pipeline_type, created_at, status FROM pipeline_runs ORDER BY id DESC LIMIT 50"
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]