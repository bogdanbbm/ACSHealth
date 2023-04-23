CREATE TABLE LOGIN_DETAILS(
    ID          int NOT NULL,
    USERNAME    varchar(255),
    PASS_HASH   varchar(255),
    IS_MEDIC    varchar(1) DEFAULT 'N',
    MAIL_CHECK  varchar(1) DEFAULT 'N',
    PRIMARY KEY (ID)
);
CREATE TABLE MEDIC_DETAILS(
    ID          int NOT NULL,
    SNAME       varchar(255),
    LNAME       varchar(255),
    RATING      FLOAT(2,2),
    PRIMARY KEY (ID)
);