from click.testing import CliRunner
from app import seed_database, create_app

def test_seed_database(mock_db_seed):
    mock_conn, mock_file = mock_db_seed
    seed_database()
    assert mock_conn.executescript_called
    assert mock_file.read_called
    assert mock_conn.commit_called
    assert mock_conn.close_called

def test_seed_cli_calls_database(mock_db_seed):
    mock_conn, mock_file = mock_db_seed # pylint: disable=W0612

    app = create_app()
    runner = CliRunner()

    result = runner.invoke(app.cli, ['seed'])

    assert result.exit_code == 0
    assert 'Baza zaseedowana!' in result.stdout
