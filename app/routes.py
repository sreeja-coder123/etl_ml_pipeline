from flask import Blueprint, request, jsonify, current_app
from .ml_model import predict_pipeline
from .yaml_generator import generate_yaml
from .db import log_pipeline, rollback_pipeline, get_lineage

bp = Blueprint("main", __name__)

@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@bp.route("/generate-pipeline", methods=["POST"])
def generate_pipeline():
    schema = request.get_json(silent=True)   # ✅ FIXED HERE
    if not schema:
        return jsonify({"error": "No JSON body provided"}), 400

    required = ["table_name", "source_type", "volume_gb", "update_frequency_hrs"]
    missing = [f for f in required if f not in schema]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    pipeline_type = predict_pipeline(schema)
    yaml_config = generate_yaml(schema, pipeline_type)

    run_id = log_pipeline(
        current_app._get_current_object(),
        schema,
        pipeline_type,
        yaml_config
    )

    return jsonify({
        "run_id": run_id,
        "pipeline_type": pipeline_type,
        "yaml_config": yaml_config
    }), 200


@bp.route("/rollback/<int:run_id>", methods=["POST"])
def rollback(run_id):
    rollback_pipeline(current_app._get_current_object(), run_id)
    return jsonify({"message": f"Run {run_id} rolled back"}), 200


@bp.route("/lineage", methods=["GET"])
def lineage():
    return jsonify(get_lineage(current_app._get_current_object())), 200