from app.ml_model import train_and_save_model, predict_pipeline

def test_train_model():
    acc = train_and_save_model()
    assert acc > 0.85

def test_predict_returns_valid_type():
    schema = {"source_type":"postgres","volume_gb":5,
              "update_frequency_hrs":24,"num_columns":40,
              "has_joins":0,"priority":2}
    result = predict_pipeline(schema)
    valid = ["batch_daily","batch_hourly","stream","micro_batch","weekly_snapshot"]
    assert result in valid

def test_predict_stream_for_hourly():
    schema = {"source_type":"api","volume_gb":0.5,
              "update_frequency_hrs":1,"num_columns":10,
              "has_joins":0,"priority":1}
    result = predict_pipeline(schema)
    assert result == "stream"