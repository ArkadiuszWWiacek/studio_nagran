from unittest.mock import Mock, patch, MagicMock
from datetime import datetime as dt
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.services import get_all_sorted, create_record, get_by_id, update_record, safe_date_parse
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

class TestSafeDateParse:
    def test_valid_datetime_space(self):
        date = '2026-01-25 14:30'
        
        result = safe_date_parse(date)
        
        assert isinstance(result, dt)
        assert result == dt(2026, 1, 25, 14, 30)

    def test_valid_datetime_iso_format(self):
        date = '2026-01-25T14:30'
        
        result = safe_date_parse(date)
        
        assert isinstance(result, dt)
        assert result == dt(2026, 1, 25, 14, 30)

    def test_valid_midnight_explicit(self):
        date = '2026-01-25 00:00'
        
        result = safe_date_parse(date)
        
        assert result == dt(2026, 1, 25, 0, 0)

    def test_empty_string(self):
        bad_input = ''
        
        with pytest.raises(ValueError, match='Pusta data'):
            safe_date_parse(bad_input)

    def test_none_input(self):
        bad_input = None
        
        with pytest.raises(ValueError, match='Pusta data'):
            safe_date_parse(bad_input)

    def test_whitespace_only(self):
        bad_input = '   '
        
        with pytest.raises(ValueError, match='Pusta data'):
            safe_date_parse(bad_input)

    def test_bad_date_part_length(self):
        bad_input = '2026-01-2 14:30'
        
        with pytest.raises(ValueError, match='Zly format daty'):
            safe_date_parse(bad_input)

    def test_bad_date_part_dashes(self):
        bad_input = '2026/01/25 14:30'
        
        with pytest.raises(ValueError, match='Zly format daty'):
            safe_date_parse(bad_input)

    def test_bad_time_format(self):
        bad_input = '2026-01-25 14.30'
        
        with pytest.raises(ValueError, match='Zly format daty'):
            safe_date_parse(bad_input)

    def test_bad_date_order(self):
        bad_input = '25-01-2026 14:30'
        
        with pytest.raises(ValueError, match='Zly format daty'):
            safe_date_parse(bad_input)
