from dataclasses import dataclass


@dataclass
class ArtystaFixtures:
    """Dataclass do grupowania fixtures w testach artystów"""
    create_artist: callable
    create_engineer: callable
    create_session: callable
    create_song: callable
    client: object
    db_session: object


@dataclass
class SesjaFixtures:
    """Dataclass dla testów sesji"""
    create_artist: callable
    create_engineer: callable
    create_equipment: callable
    create_session: callable
    client: object
    db_session: object


@dataclass
class MonkeyPatchFixtures:
    """Dataclass dla testów z monkeypatch"""
    create_artist: callable
    create_engineer: callable
    create_session: callable
    client: object
    monkeypatch: object


@dataclass
class SimpleMonkeyPatchFixtures:
    """Dataclass dla prostych testów z monkeypatch"""
    client: object
    monkeypatch: object
