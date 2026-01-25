from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.services import get_all_sorted, create_record, get_by_id, update_record
from app.models import Artysci, Inzynierowie

class TestServices:
    @pytest.fixture
    def mock_session(self):
        session = Mock(spec=Session)
        session.execute.return_value.scalars.return_value.all.return_value = []
        session.query.return_value.filter.return_value.first.return_value = None
        return session

    @patch('app.services.get_db_session')
    def test_get_all_sorted_asc(self, mock_get_db_session, mock_session):
        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock

        result = get_all_sorted(Artysci, 'Nazwa', 'asc')
        mock_session.execute.assert_called_once()
        assert result == []

    @patch('app.services.get_db_session')
    def test_get_all_sorted_desc(self, mock_get_db_session, mock_session):
        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock

        result = get_all_sorted(Artysci, 'Nazwa', 'desc')
        mock_session.execute.assert_called_once()
        assert result == []

    @patch('app.services.get_db_session')
    def test_create_record(self, mock_get_db_session, mock_session):
        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock

        instance = create_record(Artysci, Nazwa='Test')
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        assert instance.Nazwa == 'Test'

    @patch('app.services.get_db_session')
    def test_get_by_id_found(self, mock_get_db_session, mock_session):
        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock
        mock_model = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_model

        result = get_by_id(Artysci, 1)
        assert result == mock_model

    @patch('app.services.get_db_session')
    def test_get_by_id_not_found(self, mock_get_db_session, mock_session):
        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock

        result = get_by_id(Artysci, 999)
        assert result is None

    @patch('app.services.get_db_session')
    def test_update_record(self, mock_get_db_session, mock_session):
        instance = Artysci(Nazwa='Old')

        ctx_mock = MagicMock()
        ctx_mock.__enter__.return_value = mock_session
        mock_get_db_session.return_value = ctx_mock

        update_record(instance, Nazwa='Updated')
        mock_session.merge.assert_called_once_with(instance)
        assert instance.Nazwa == 'Updated'

class TestModels:
    def test_artysci_tablename(self):
        assert Artysci.__tablename__ == 'artysci'

    def test_artysci_columns(self):
        insp = inspect(Artysci)
        columns = [col.name for col in insp.c]
        assert 'IdArtysty' in columns
        assert 'Nazwa' in columns

    def test_inzynierowie_tablename(self):
        assert Inzynierowie.__tablename__ == 'inzynierowie'

class TestSesjeLogic:
    def test_parse_terminstart_valid(self):
        terminstart_str = '2026-01-25'
        terminstart = datetime.strptime(terminstart_str, '%Y-%m-%d')
        assert terminstart.year == 2026

    def test_parse_terminstop_none(self):
        terminstop_str = None
        terminstop = datetime.strptime(terminstop_str, '%Y-%m-%d') if terminstop_str else None
        assert terminstop is None
