CREATE TABLE REVIEWS(
    ID_MEDIC     int NOT NULL,
    ID_REVIEW    int AUTO_INCREMENT,
    REVIEW       TEXT,
    RATING       FLOAT,
    PRIMARY KEY (ID_REVIEW)
);
CREATE TABLE PATIENT_DATA(
    ID          int NOT NULL,
    FIRST_NAME    varchar(255),
    LAST_NAME   varchar(255),
    CNP         varchar(20),
    BIRTHDATE   DATE,
    SEX         varchar(1),
    HEIGHT      FLOAT,
    SGROUP      varchar(2),
    RH          varchar(2),
    PRIMARY KEY (ID)
);
CREATE TABLE WEIGHT_HISTORY(
    ID              int NOT NULL,
    WEIGHT_VALUE    FLOAT,
    PRIMARY KEY (ID)
);
CREATE TABLE ALERGY_LIST(
    ID              int NOT NULL,
    ALERGY          varchar(20),
    PRIMARY KEY (ID)
);
CREATE TABLE CONSULTATION_LIST(
    ID_CONSULT      int AUTO_INCREMENT,
    ID_MEDIC        int NOT NULL,
    ID_PATIENT      int NOT NULL,
    CONSULTATION    DATE,
    TREATMENT       TEXT,
    PRIMARY KEY (ID_CONSULT)
);
CREATE TABLE BLOOD_DONATION(
    ID              int NOT NULL,
    DONATION_DATE   DATE,
    PRIMARY KEY (ID)
);
