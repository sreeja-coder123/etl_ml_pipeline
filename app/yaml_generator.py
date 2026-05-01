import yaml
from datetime import datetime

SCHEDULES = {
    "batch_daily": "0 2 * * *",
    "batch_hourly": "0 * * * *",
    "stream": "@continuous",
    "micro_batch": "*/15 * * * *",
    "weekly_snapshot": "0 3 * * 0",
}

def generate_yaml(schema: dict, pipeline_type: str) -> str:
    config = {
        "pipeline": {
            "name": f"{schema.get('table_name','table')}_pipeline",
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "generated_by": "ETL-ML-AutoConfig",
            "source": {
                "type": schema.get("source_type","mysql"),
                "table": schema.get("table_name","raw_table"),
                "volume_gb": schema.get("volume_gb", 1.0),
            },
            "pipeline_type": pipeline_type,
            "schedule": SCHEDULES.get(pipeline_type,"0 2 * * *"),
            "transform": {
                "deduplicate": True,
                "validate_nulls": True,
                "partition_by": "ingestion_date",
            },
            "destination": {
                "type": "data_warehouse",
                "schema": "processed",
                "table": schema.get("table_name","raw_table") + "_clean",
                "write_mode": "append" if pipeline_type == "stream" else "overwrite",
            },
            "monitoring": {
                "alert_on_failure": True,
                "sla_minutes": 60,
                "row_count_check": True,
            }
        }
    }
    return yaml.dump(config, default_flow_style=False, sort_keys=False)