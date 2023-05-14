CREATE TABLE LOGIN_DETAILS(
    ID          int NOT NULL AUTO_INCREMENT,
    USERNAME    varchar(255),
    PASS_HASH   varchar(255),
    IS_MEDIC    varchar(1) DEFAULT 'N',
    MAIL_CHECK  varchar(1) DEFAULT 'N',
    MAIL_UUID   varchar(255) DEFAULT 'N',
    PRIMARY KEY (ID)
);
CREATE TABLE MEDIC_DETAILS(
    ID          int NOT NULL,
    SNAME       varchar(255),
    LNAME       varchar(255),
    RATING      FLOAT,
    PRIMARY KEY (ID)
);
CREATE TABLE REVIEWS(
    MEDIC_ID     int NOT NULL,
    ID_REVIEW    int NOT NULL AUTO_INCREMENT,
    REVIEW       TEXT,
    IMAGE_STAMP  TIMESTAMP,
    PRIMARY KEY (ID_REVIEW)
);
CREATE TABLE IMAGES(
    ID_REVIEW    int NOT NULL,
    IMAGE_STAMP  TIMESTAMP NOT NULL,
    PHOTO        LONGBLOB NOT NULL,
    PRIMARY KEY (ID_REVIEW)
);
CREATE TABLE PERSONAL_DATA(
    ID          int NOT NULL,
    SUR_NAME    varchar(255),
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
