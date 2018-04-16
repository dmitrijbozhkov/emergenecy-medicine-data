CREATE TABLE symptom_group (
    name TEXT PRIMARY KEY
)

CREATE TABLE symptom (
    name TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    FOREIGN KEY (group_name) REFERENCES symptom_group (name)
)

CREATE TABLE diagnosis (
    name TEXT PRIMARY KEY,
    description TEXT
)

CREATE TABLE symptom_diagnosis (
    symptom_name TEXT,
    diagnosis_name TEXT,
    symptom_group_name TEXT,
    probability REAL NOT NULL,
    PRIMARY KEY (symptom_name, diagnosis_name, symptom_group_name),
    FOREIGN KEY (symptom_name) REFERENCES symptom (name) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (diagnosis_name) REFERENCES diagnosis (name) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (symptom_group_name) REFERENCES symptom_group (name) ON DELETE CASCADE ON UPDATE NO ACTION
)