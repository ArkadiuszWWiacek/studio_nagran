BEGIN TRANSACTION;
CREATE TABLE artysci (
    IdArtysty INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa TEXT NOT NULL UNIQUE,
    Imie TEXT,
    Nazwisko TEXT
);
INSERT INTO "artysci" VALUES(1,'Echoes','Marek','Nowak');
INSERT INTO "artysci" VALUES(2,'The Soundmakers','Anna','Kowalska');
INSERT INTO "artysci" VALUES(3,'Deep Resonance','Piotr','Wiśniewski');
INSERT INTO "artysci" VALUES(4,'Aurora','Katarzyna','Lewandowska');
INSERT INTO "artysci" VALUES(5,'Lunar Pulse','Tomasz','Zieliński');
INSERT INTO "artysci" VALUES(6,'Velvet Tones','Magdalena','Wójcik');
INSERT INTO "artysci" VALUES(7,'Analog Dreams','Jakub','Kamińczyk');
INSERT INTO "artysci" VALUES(8,'Solaris','Paweł','Dąbrowski');
INSERT INTO "artysci" VALUES(9,'The Frequencies','Monika','Kaczmarek');
INSERT INTO "artysci" VALUES(10,'Silent Motion','Adrian','Nowicki');
INSERT INTO "artysci" VALUES(11,'O''Reiley','Harry','O''Railey McDonald');
INSERT INTO "artysci" VALUES(12,'Hauas','Rafał','Wierzbicki');
INSERT INTO "artysci" VALUES(13,'Ryza','Weronika','Racka');
INSERT INTO "artysci" VALUES(14,'Grooby','Abigail','Groobdotter');
INSERT INTO "artysci" VALUES(15,'Zepsuty Termostat','Zenon','Parawan');
INSERT INTO "artysci" VALUES(16,'Pralka w Fazie REM','Giuseppe','Skarpeta');
INSERT INTO "artysci" VALUES(17,'Elektryczny Kasztan','Wolfgang','Guzik');
INSERT INTO "artysci" VALUES(18,'TestBand','Jan','Kowalski');
INSERT INTO "artysci" VALUES(19,'Pink Froyd','Pink','Froyd');
INSERT INTO "artysci" VALUES(20,'Spring Heel Jack','Heel','Jack');
INSERT INTO "artysci" VALUES(21,'TestArtist',NULL,NULL);
INSERT INTO "artysci" VALUES(22,'IntBand','IntJan',NULL);
INSERT INTO "artysci" VALUES(23,'B',NULL,NULL);
INSERT INTO "artysci" VALUES(24,'A',NULL,NULL);
INSERT INTO "artysci" VALUES(25,'FindMe',NULL,NULL);
INSERT INTO "artysci" VALUES(26,'After','New',NULL);
INSERT INTO "artysci" VALUES(27,'Nowy Artysta','New','Artist');
CREATE TABLE inzynierowie (
    IdInzyniera INTEGER PRIMARY KEY AUTOINCREMENT,
    Imie TEXT NOT NULL,
    Nazwisko TEXT
);
INSERT INTO "inzynierowie" VALUES(1,'Michał','Kowal');
INSERT INTO "inzynierowie" VALUES(2,'Ewa','Błaszczyk');
INSERT INTO "inzynierowie" VALUES(3,'Rafał','Majewski');
INSERT INTO "inzynierowie" VALUES(4,'Kamil','Górecki');
INSERT INTO "inzynierowie" VALUES(5,'Natalia','Zając');
INSERT INTO "inzynierowie" VALUES(6,'Adam','Sobczak');
INSERT INTO "inzynierowie" VALUES(7,'Oliwia','Lis');
INSERT INTO "inzynierowie" VALUES(8,'Łukasz','Baran');
INSERT INTO "inzynierowie" VALUES(9,'Daria','Król');
INSERT INTO "inzynierowie" VALUES(10,'Marek','Nowakowski');
INSERT INTO "inzynierowie" VALUES(11,'Arkadiusz','Wiącek');
INSERT INTO "inzynierowie" VALUES(12,'Andrzej','Welling');
INSERT INTO "inzynierowie" VALUES(13,'Tomasz','Szybisz');
INSERT INTO "inzynierowie" VALUES(14,'Filip','Filipowicz');
INSERT INTO "inzynierowie" VALUES(15,'Lidia','Werenga');
INSERT INTO "inzynierowie" VALUES(16,'Feliks','Burza');
INSERT INTO "inzynierowie" VALUES(17,'Cyprian','Owad');
INSERT INTO "inzynierowie" VALUES(18,'Eustachy','Motyka');
INSERT INTO "inzynierowie" VALUES(19,'Jan','Kowalski');
INSERT INTO "inzynierowie" VALUES(20,'Adam','Nowak');
INSERT INTO "inzynierowie" VALUES(21,'Genowefa','Pigwowska');
CREATE TABLE sesje (
    IdSesji INTEGER PRIMARY KEY AUTOINCREMENT,
    IdArtysty INTEGER NOT NULL,
    IdInzyniera INTEGER NOT NULL,
    TerminStart TEXT NOT NULL,
    TerminStop TEXT,
    FOREIGN KEY (IdArtysty) REFERENCES artysci(IdArtysty),
    FOREIGN KEY (IdInzyniera) REFERENCES inzynierowie(IdInzyniera)
);
INSERT INTO "sesje" VALUES(1,1,1,'2025-01-10 10:00:00','2025-01-10 14:00:00');
INSERT INTO "sesje" VALUES(2,2,3,'2025-01-12 09:00:00','2025-01-12 17:00:00');
INSERT INTO "sesje" VALUES(3,3,5,'2025-01-15 11:00:00','2025-01-15 18:00:00');
INSERT INTO "sesje" VALUES(4,4,2,'2025-02-01 08:00:00','2025-02-01 16:00:00');
INSERT INTO "sesje" VALUES(5,5,4,'2025-02-05 10:30:00','2025-02-05 15:00:00');
INSERT INTO "sesje" VALUES(6,6,7,'2025-02-10 12:00:00','2025-02-10 18:30:00');
INSERT INTO "sesje" VALUES(7,7,6,'2025-02-12 09:00:00','2025-02-12 17:00:00');
INSERT INTO "sesje" VALUES(8,8,8,'2025-03-01 10:00:00','2025-03-01 14:00:00');
INSERT INTO "sesje" VALUES(9,9,9,'2025-03-10 13:00:00','2025-03-10 18:00:00');
INSERT INTO "sesje" VALUES(10,10,10,'2025-03-20 11:00:00','2025-03-20 17:00:00');
INSERT INTO "sesje" VALUES(11,1,5,'2025-11-12 11:20:17',NULL);
INSERT INTO "sesje" VALUES(12,2,3,'2025-11-12 11:20:18',NULL);
INSERT INTO "sesje" VALUES(13,1,1,'2025-04-01 10:00:00','2025-04-01 14:00:00');
INSERT INTO "sesje" VALUES(14,2,1,'2025-01-11 09:00:00','2025-01-11 13:00:00');
INSERT INTO "sesje" VALUES(15,12,11,'2025-12-01','2025-12-05');
INSERT INTO "sesje" VALUES(16,7,8,'2026-01-01','2026-02-01');
INSERT INTO "sesje" VALUES(17,6,5,'2025-12-01',NULL);
INSERT INTO "sesje" VALUES(18,11,9,'2025-12-31',NULL);
INSERT INTO "sesje" VALUES(19,13,11,'2025-12-20',NULL);
INSERT INTO "sesje" VALUES(20,15,18,'2025-11-30','2025-12-31');
INSERT INTO "sesje" VALUES(21,1,1,'2025-01-01',NULL);
INSERT INTO "sesje" VALUES(22,1,1,'2025-01-01',NULL);
INSERT INTO "sesje" VALUES(23,21,19,'2025-01-01',NULL);
CREATE TABLE sprzet (
    IdSprzetu INTEGER PRIMARY KEY AUTOINCREMENT,
    Producent TEXT,
    Model TEXT NOT NULL,
    Kategoria TEXT CHECK(Kategoria IN ('Mikrofony','Procesory','Przewody','Akcesoria'))
);
INSERT INTO "sprzet" VALUES(1,'Shure','SM7B','Mikrofony');
INSERT INTO "sprzet" VALUES(2,'Neumann','U87','Mikrofony');
INSERT INTO "sprzet" VALUES(3,'Rode','NT1-A','Mikrofony');
INSERT INTO "sprzet" VALUES(4,'Focusrite','Scarlett 18i20','Procesory');
INSERT INTO "sprzet" VALUES(5,'Universal Audio','Apollo Twin','Procesory');
INSERT INTO "sprzet" VALUES(6,'Behringer','Xenyx Q802USB','Procesory');
INSERT INTO "sprzet" VALUES(7,'Mogami','Gold XLR','Przewody');
INSERT INTO "sprzet" VALUES(8,'Hosa','Pro Series','Przewody');
INSERT INTO "sprzet" VALUES(9,'K&M','210/9','Akcesoria');
INSERT INTO "sprzet" VALUES(10,'On-Stage','MS7701B','Akcesoria');
INSERT INTO "sprzet" VALUES(11,'Shure','SM7B','Mikrofony');
INSERT INTO "sprzet" VALUES(12,'Rode','NT-USB+','Mikrofony');
INSERT INTO "sprzet" VALUES(13,'Blue','Yeti','Mikrofony');
INSERT INTO "sprzet" VALUES(14,'Audio-Technica','AT2020','Mikrofony');
INSERT INTO "sprzet" VALUES(15,'Focusrite','Scarlett 2i2','Procesory');
INSERT INTO "sprzet" VALUES(16,'Universal Audio','Apollo Twin','Procesory');
INSERT INTO "sprzet" VALUES(17,'Mogami','Gold Studio','Przewody');
INSERT INTO "sprzet" VALUES(18,'Neumann','KH 310 A (kabel)','Przewody');
INSERT INTO "sprzet" VALUES(19,'Sennheiser','GSX 1000','Akcesoria');
INSERT INTO "sprzet" VALUES(20,'Elgato','Wave Mic Arm','Akcesoria');
INSERT INTO "sprzet" VALUES(21,'Lexicon','MX200','Procesory');
INSERT INTO "sprzet" VALUES(22,'DBX','166XL','Procesory');
INSERT INTO "sprzet" VALUES(23,'Behringer','Tube Ultragain','Procesory');
INSERT INTO "sprzet" VALUES(24,'Motu','828MK2','Procesory');
INSERT INTO "sprzet" VALUES(25,'Boss','GT-8','Procesory');
CREATE TABLE sprzety_sesje (
    IdSprzetu INTEGER NOT NULL,
    IdSesji INTEGER NOT NULL,
    PRIMARY KEY (IdSprzetu, IdSesji),
    FOREIGN KEY (IdSprzetu) REFERENCES sprzet(IdSprzetu),
    FOREIGN KEY (IdSesji) REFERENCES sesje(IdSesji)
);
INSERT INTO "sprzety_sesje" VALUES(1,1);
INSERT INTO "sprzety_sesje" VALUES(2,2);
INSERT INTO "sprzety_sesje" VALUES(3,3);
INSERT INTO "sprzety_sesje" VALUES(4,4);
INSERT INTO "sprzety_sesje" VALUES(5,5);
INSERT INTO "sprzety_sesje" VALUES(6,6);
INSERT INTO "sprzety_sesje" VALUES(7,7);
INSERT INTO "sprzety_sesje" VALUES(8,8);
INSERT INTO "sprzety_sesje" VALUES(9,9);
INSERT INTO "sprzety_sesje" VALUES(10,10);
INSERT INTO "sprzety_sesje" VALUES(10,11);
INSERT INTO "sprzety_sesje" VALUES(4,11);
INSERT INTO "sprzety_sesje" VALUES(9,11);
INSERT INTO "sprzety_sesje" VALUES(11,15);
INSERT INTO "sprzety_sesje" VALUES(2,15);
INSERT INTO "sprzety_sesje" VALUES(22,15);
INSERT INTO "sprzety_sesje" VALUES(16,15);
INSERT INTO "sprzety_sesje" VALUES(21,15);
INSERT INTO "sprzety_sesje" VALUES(23,15);
INSERT INTO "sprzety_sesje" VALUES(9,16);
INSERT INTO "sprzety_sesje" VALUES(3,16);
INSERT INTO "sprzety_sesje" VALUES(17,16);
INSERT INTO "sprzety_sesje" VALUES(8,16);
INSERT INTO "sprzety_sesje" VALUES(1,17);
INSERT INTO "sprzety_sesje" VALUES(2,19);
INSERT INTO "sprzety_sesje" VALUES(16,19);
INSERT INTO "sprzety_sesje" VALUES(21,19);
INSERT INTO "sprzety_sesje" VALUES(3,20);
INSERT INTO "sprzety_sesje" VALUES(5,20);
INSERT INTO "sprzety_sesje" VALUES(21,20);
INSERT INTO "sprzety_sesje" VALUES(1,21);
INSERT INTO "sprzety_sesje" VALUES(2,21);
INSERT INTO "sprzety_sesje" VALUES(1,22);
INSERT INTO "sprzety_sesje" VALUES(2,22);
CREATE TABLE utwory (
    IdUtworu INTEGER PRIMARY KEY AUTOINCREMENT,
    IdArtysty INTEGER NOT NULL,
    IdSesji INTEGER NOT NULL,
    Tytul TEXT NOT NULL,
    FOREIGN KEY (IdArtysty) REFERENCES artysci(IdArtysty),
    FOREIGN KEY (IdSesji) REFERENCES sesje(IdSesji)
);
INSERT INTO "utwory" VALUES(1,1,1,'Fading Echo');
INSERT INTO "utwory" VALUES(2,2,2,'Light and Sound');
INSERT INTO "utwory" VALUES(3,3,3,'Deep Blue');
INSERT INTO "utwory" VALUES(4,4,4,'Northern Sky');
INSERT INTO "utwory" VALUES(5,5,5,'Moonlight');
INSERT INTO "utwory" VALUES(6,6,6,'Velvet Night');
INSERT INTO "utwory" VALUES(7,7,7,'Analog Dreams');
INSERT INTO "utwory" VALUES(8,8,8,'Solar Flare');
INSERT INTO "utwory" VALUES(9,9,9,'Frequency Shift');
INSERT INTO "utwory" VALUES(10,10,10,'Silent Steps');
INSERT INTO "utwory" VALUES(11,1,1,'Test Track 1');
INSERT INTO "utwory" VALUES(12,1,1,'Test Track 1');
INSERT INTO "utwory" VALUES(13,13,19,'Jesteś lekiem na całe zło');
INSERT INTO "utwory" VALUES(14,13,19,'Babę zesłał Bóg');
INSERT INTO "utwory" VALUES(15,13,19,'Kochana');
INSERT INTO "utwory" VALUES(16,1,11,'Byłaś serca biciem');
INSERT INTO "utwory" VALUES(17,12,15,'Aldebaran');
INSERT INTO "utwory" VALUES(18,4,4,'Czysty kod');
INSERT INTO "utwory" VALUES(19,15,20,'Beton Poziom -3');
INSERT INTO "utwory" VALUES(20,15,20,'Echo Forda Mondeo');
INSERT INTO "utwory" VALUES(21,15,20,'Mandat pod Wycieraczką');
INSERT INTO "utwory" VALUES(22,15,20,'Neonówka Migocze o 4:17');
INSERT INTO "utwory" VALUES(23,12,15,'Najs');
INSERT INTO "utwory" VALUES(24,12,15,'Ballada o Paramonowie');
CREATE VIEW v_raport_sesji AS
SELECT
  s.IdSesji AS IdSesji,
  a.Nazwa || ' ' || a.Imie || ' ' || a.Nazwisko AS Artysta,
  s.TerminStart AS "Rospoczęcie Sesji",
  sp.Model,
  sp.Kategoria
FROM sesje s
JOIN artysci a ON a.IdArtysty = s.IdArtysty
JOIN sprzety_sesje ss ON ss.IdSesji = s.IdSesji
JOIN sprzet sp ON sp.IdSprzetu = ss.IdSprzetu
GROUP BY s.IdSesji;
CREATE INDEX idx_sesje ON sesje(IdArtysty);
CREATE INDEX idx_utwory ON sesje(IdArtysty);
CREATE TRIGGER validate_sesja_time
BEFORE INSERT ON sesje
FOR EACH ROW
WHEN NEW.TerminStop IS NOT NULL AND NEW.TerminStop <= NEW.TerminStart
BEGIN
    SELECT RAISE(ABORT, 'TerminStop musi był póniejszy niż TerminStart');
END;
CREATE TRIGGER validate_sesja_time_update
BEFORE UPDATE ON sesje
FOR EACH ROW
WHEN NEW.TerminStop IS NOT NULL AND NEW.TerminStop <= NEW.TerminStart
BEGIN
    SELECT RAISE(ABORT, 'TerminStop musi był póniejszy niż TerminStart');
END;
CREATE TRIGGER check_inzynier_overlap
BEFORE INSERT ON sesje
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Inżynier jest już zajęty w tym terminie')
    WHERE EXISTS (
        SELECT 1 FROM sesje
        WHERE IdInzyniera = NEW.IdInzyniera
        AND IdSesji != NEW.IdSesji
        AND (
            (NEW.TerminStart >= TerminStart AND NEW.TerminStart < TerminStop)
            OR (NEW.TerminStop > TerminStart AND NEW.TerminStop <= TerminStop)
            OR (NEW.TerminStart <= TerminStart AND NEW.TerminStop >= TerminStop)
        )
    );
END;
CREATE TRIGGER validate_utwor_artist
BEFORE INSERT ON utwory
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'IdArtysty w utworze musi zgadzać się z IdArtysty w sesji')
    WHERE NOT EXISTS (
        SELECT 1 FROM sesje 
        WHERE IdSesji = NEW.IdSesji 
        AND IdArtysty = NEW.IdArtysty
    );
END;
CREATE TRIGGER validate_utwor_artist_update
BEFORE UPDATE ON utwory
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'IdArtysty w utworze musi zgadzać się z IdArtysty w sesji')
    WHERE NOT EXISTS (
        SELECT 1 FROM sesje 
        WHERE IdSesji = NEW.IdSesji 
        AND IdArtysty = NEW.IdArtysty
    );
END;
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('artysci',27);
INSERT INTO "sqlite_sequence" VALUES('inzynierowie',21);
INSERT INTO "sqlite_sequence" VALUES('sesje',23);
INSERT INTO "sqlite_sequence" VALUES('sprzet',25);
INSERT INTO "sqlite_sequence" VALUES('utwory',24);
COMMIT;
