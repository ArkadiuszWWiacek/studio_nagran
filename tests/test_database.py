from app import database


def test_init_db_creates_tables():
    database.init_db()

def test_init_db_cli_command_calls_init_db_and_echoes_message(client, monkeypatch):
    app = client.application

    database.init_app(app)

    called = {"n": 0}

    def fake_init_db():
        called["n"] += 1

    monkeypatch.setattr(database, "init_db", fake_init_db)

    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])

    assert result.exit_code == 0
    assert called["n"] == 1
    assert "Initialized the database." in result.output
