CREATE TABLE association (
    associationId TEXT PRIMARY KEY
)

CREATE TABLE term (
    termId TEXT PRIMARY KEY
)

CREATE TABLE term_association (
    termId TEXT,
    associationId TEXT,
    PRIMARY KEY (termId, associationId),
    FOREIGN KEY (termId) REFERENCES term (termId),
    FOREIGN KEY (associationId) REFERENCES association (associationId)
)

CREATE TABLE body_part (
    body_partId TEXT PRIMARY KEY,
    FOREIGN KEY (body_partId) REFERENCES term (termId)
)

CREATE TABLE substance (
    substanceId TEXT PRIMARY KEY,
    FOREIGN KEY (substanceId) REFERENCES term (termId)
)

CREATE TABLE physical_examination (
    precedentId TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    aquisition TEXT NOT NULL,
    question TEXT NOT NULL,
    FOREIGN KEY (precedentId) REFERENCES term (termId)
)

CREATE TABLE circumstance (
    circumstanceId TEXT PRIMARY KEY,
    FOREIGN KEY (circumstanceId) REFERENCES term (termId)
)

CREATE TABLE trauma (
    traumaId TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    treatment TEXT NOT NULL,
    specifies TEXT,
    FOREIGN KEY (traumaId) REFERENCES term (termId)
)

CREATE TABLE prescription (
    traumaId TEXT,
    substanceId TEXT,
    PRIMARY KEY (traumaId, substanceId),
    FOREIGN KEY (traumaId) REFERENCES trauma (traumaId),
    FOREIGN KEY (substanceId) REFERENCES substance (substanceId)
)

CREATE TABLE trauma_precedent (
    traumaId TEXT,
    precedentId TEXT,
    PRIMARY KEY (traumaId, precedentId),
    FOREIGN KEY (traumaId) REFERENCES trauma (traumaId),
    FOREIGN KEY (precedentId) REFERENCES physical_examination (precedentId)
)

CREATE TABLE trauma_circumstnce (
    traumaId TEXT,
    circumstanceId TEXT,
    PRIMARY KEY (traumaId, circumstanceId),
    FOREIGN KEY (traumaId) REFERENCES trauma (traumaId),
    FOREIGN KEY (circumstanceId) REFERENCES circumstance (circumstanceId)
)

CREATE TABLE trauma_body_part (
    traumaId TEXT,
    body_partId TEXT,
    PRIMARY KEY (traumaId, body_partId),
    FOREIGN KEY (traumaId) REFERENCES trauma (traumaId),
    FOREIGN KEY (body_partId) REFERENCES body_part (body_partId)
)
