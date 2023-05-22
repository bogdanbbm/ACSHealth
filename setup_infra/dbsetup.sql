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

CREATE TABLE BLOOD_DONATION(
    ID              int NOT NULL,
    DONATION_DATE   DATE,
    PRIMARY KEY (ID)
);