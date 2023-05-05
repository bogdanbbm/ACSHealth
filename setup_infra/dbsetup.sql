-- CREATE TABLE LOGIN_DETAILS(
--     ID          int NOT NULL AUTO_INCREMENT,
--     USERNAME    varchar(255),
--     PASS_HASH   varchar(255),
--     IS_MEDIC    varchar(1) DEFAULT 'N',
--     MAIL_CHECK  varchar(1) DEFAULT 'N',
--     MAIL_UUID   varchar(255) DEFAULT 'N',
--     PRIMARY KEY (ID)
-- );
-- CREATE TABLE MEDIC_DETAILS(
--     ID          int NOT NULL,
--     SNAME       varchar(255),
--     LNAME       varchar(255),
--     RATING      FLOAT(2,2),
--     PRIMARY KEY (ID),
--     FOREIGN KEY (ID) REFERENCES LOGIN_DETAILS(ID)
-- );
-- CREATE TABLE REVIEWS(
--     ID          int NOT NULL,
--     REVIEW      TEXT,
--     PHOTO       LONGBLOB,
--     PRIMARY KEY (ID),
--     FOREIGN KEY (ID) REFERENCES LOGIN_DETAILS(ID)
-- );

DROP TABLE DEPT;
DROP TABLE EMP;
DROP TABLE SALGRADE;

CREATE TABLE DEPT
 ( DEPTNO NUMBER(2) CONSTRAINT PK_DEPT PRIMARY KEY,
   DNAME VARCHAR2(14) ,
   LOC VARCHAR2(13)  );

INSERT INTO DEPT VALUES (10,'ACCOUNTING','NEW YORK');
INSERT INTO DEPT VALUES (20,'RESEARCH','DALLAS');
INSERT INTO DEPT VALUES (30,'SALES','CHICAGO');
INSERT INTO DEPT VALUES (40,'OPERATIONS','BOSTON');

CREATE TABLE EMP
 ( EMPNO  NUMBER(4) CONSTRAINT PK_EMP PRIMARY KEY,
   ENAME  VARCHAR2(10),
   JOB  VARCHAR2(9),
   MGR  NUMBER(4),
   HIREDATE  DATE,
   SAL  NUMBER(7,2),
   COMM  NUMBER(7,2),
   DEPTNO  NUMBER(2) CONSTRAINT FK_DEPTNO REFERENCES DEPT );

INSERT INTO EMP VALUES
(7369,'SMITH','CLERK',7902,to_date('17-12-1980','dd-mm-yyyy'),800,NULL,20);
INSERT INTO EMP VALUES
(7499,'ALLEN','SALESMAN',7698,to_date('20-2-1981','dd-mm-yyyy'),1600,300,30);
INSERT INTO EMP VALUES
(7521,'WARD','SALESMAN',7698,to_date('22-2-1981','dd-mm-yyyy'),1250,500,30);
INSERT INTO EMP VALUES
(7566,'JONES','MANAGER',7839,to_date('2-4-1981','dd-mm-yyyy'),2975,NULL,20);
INSERT INTO EMP VALUES
(7654,'MARTIN','SALESMAN',7698,to_date('28-9-1981','dd-mm-yyyy'),1250,1400,30);
INSERT INTO EMP VALUES
(7698,'BLAKE','MANAGER',7839,to_date('1-5-1981','dd-mm-yyyy'),2850,NULL,30);
INSERT INTO EMP VALUES
(7782,'CLARK','MANAGER',7839,to_date('9-6-1981','dd-mm-yyyy'),2450,NULL,10);
INSERT INTO EMP VALUES
(7788,'SCOTT','ANALYST',7566,to_date('19-4-1987', 'dd-mm-yyyy'),3000,NULL,20);
INSERT INTO EMP VALUES
(7839,'KING','PRESIDENT',NULL,to_date('17-11-1981','dd-mm-yyyy'),5000,NULL,10);
INSERT INTO EMP VALUES
(7844,'TURNER','SALESMAN',7698,to_date('8-9-1981','dd-mm-yyyy'),1500,0,30);
INSERT INTO EMP VALUES
(7876,'ADAMS','CLERK',7788,to_date('23-5-1987','dd-mm-yyyy'),1100,NULL,20);
INSERT INTO EMP VALUES
(7900,'JAMES','CLERK',7698,to_date('3-12-1981','dd-mm-yyyy'),950,NULL,30);
INSERT INTO EMP VALUES
(7902,'FORD','ANALYST',7566,to_date('3-12-1981','dd-mm-yyyy'),3000,NULL,20);
INSERT INTO EMP VALUES
(7934,'MILLER','CLERK',7782,to_date('23-1-1982','dd-mm-yyyy'),1300,NULL,10);

CREATE TABLE SALGRADE
 ( GRADE NUMBER,
   LOSAL NUMBER,
   HISAL NUMBER );

INSERT INTO SALGRADE VALUES (1,700,1200);
INSERT INTO SALGRADE VALUES (2,1201,1400);
INSERT INTO SALGRADE VALUES (3,1401,2000);
INSERT INTO SALGRADE VALUES (4,2001,3000);
INSERT INTO SALGRADE VALUES (5,3001,9999);



DROP TABLE BONUS;
CREATE TABLE BONUS
 ( ENAME VARCHAR2(10),
   JOB VARCHAR2(9),
   SAL NUMBER,
   COMM NUMBER ) ;

COMMIT;



SELECT ENAME, DNAME, SAL + NVL(COMM,0) VENIT
FROM EMP A, DEPT B
WHERE
 A.DEPTNO = B.DEPTNO
 AND
 B.LOC NOT LIKE 'CHICAGO'
 AND
 A.HIREDATE > TO_DATE('01-01-1981', 'DD-MM-YYYY');

/*

Sau: TO_CHAR(A.HIREDATE, 'YYYYMMDD') > '19810101'

*/

SELECT ENAME, DNAME, SAL + NVL(COMM,0) VENIT
FROM EMP A JOIN DEPT D USING (DEPTNO)
WHERE
 D.LOC NOT LIKE 'CHICAGO';

SELECT ENAME, DNAME, SAL + NVL(COMM,0) VENIT
FROM EMP A NATURAL JOIN DEPT D
WHERE
 D.LOC != 'CHICAGO';

/*

Sa se selecteze toti angajatii care nu fac 
parte din dept accounting afisand nume angajat, denumire dept si comision.


SA SE SELECTEZE TOTI ANGAJATII CARE NU FAC PARTE DIN DEPT ACCOUNTING SI CARE NU AU COMISION AFISAND 
NUME ANGAJAT DENUMIRE DEPT SI VAL COMISION VEZI REZ PRIN TOATE CLE 4 METODE

*/


SELECT ENAME, DNAME, COMM
FROM EMP A JOIN DEPT D USING (DEPTNO)
WHERE
 D.DNAME != 'ACCOUNTING'
 AND
 NVL(A.COMM, 0) = 0;


SELECT ENAME, DNAME, COMM
FROM EMP A NATURAL JOIN DEPT D
WHERE
 D.DNAME != 'ACCOUNTING'
 AND
 NVL(A.COMM, 0) = 0;

SELECT A.ENAME, A.SAL + NVL(A.COMM, 0) VENIT_ANG, S.ENAME, S.SAL + NVL(S.COMM, 0) VENIT_SEF
FROM EMP A, EMP S
WHERE
 A.MGR = S.EMPNO
 AND
 A.SAL + NVL(A.COMM, 0) > S.SAL + NVL(S.COMM, 0);

/*

Cu join on

*/

SELECT A.ENAME, A.SAL + NVL(A.COMM, 0) VENIT_ANG, S.ENAME, S.SAL + NVL(S.COMM, 0) VENIT_SEF
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO
WHERE
 A.SAL + NVL(A.COMM, 0) > S.SAL + NVL(S.COMM, 0);

-- Toti care castiga mai putin decat sefii lor si castiga mai mult decat scott

SELECT A.ENAME, A.SAL + NVL(A.COMM, 0) VENIT_ANG, S.ENAME, S.SAL + NVL(S.COMM, 0) VENIT_SEF
FROM EMP A, EMP S, EMP SCOTT
WHERE
 A.MGR = S.EMPNO
 AND
 A.SAL + NVL(A.COMM, 0) < S.SAL + NVL(S.COMM, 0)
 AND
 A.SAL + NVL(A.COMM, 0) > SCOTT.SAL + NVL(SCOTT.COMM, 0)
 AND
 SCOTT.ENAME = 'SCOTT';


SELECT A.ENAME, A.SAL + NVL(A.COMM, 0) VENIT_ANG, S.ENAME, S.SAL + NVL(S.COMM, 0) VENIT_SEF
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO, EMP SCOTT
WHERE
 A.SAL + NVL(A.COMM, 0) < S.SAL + NVL(S.COMM, 0)
 AND
 A.SAL + NVL(A.COMM, 0) > SCOTT.SAL + NVL(SCOTT.COMM, 0)
 AND
 SCOTT.ENAME = 'SCOTT';

/*
Creati o lista in care sa fie calculata o prima pt angajatii care nu primesc comision, nu au functia de manager si s-au angajat inainte de Ellen.
Prima: 23% din venitul lunar al angajatului in valoare rotunjita la intregi. Veti afisa: angajatul, functia, comisionul, data de angajare, data de angajare a lui Ellen
si prima calculata.
*/
/*
SELECT A.ENAME, A.JOB, A.COMM, A.HIREDATE, E.HIREDATE, ROUND(SAL / 23 * 100, -2) PRIMA
FROM EMP A, EMP E,
WHERE
 NVL(A.COMM, 0) = 0
 AND
 A.JOB != "MANAGER"
 AND
 E.ENAME = "ELLEN";
*/


/*

Functii utile: CONCAT (a, b)
LIKE '____'
LENGTH(a)
SUBSTR(SIRNAME, NRCAR, [POZ]) // poz e optional
REPLACE('FACULTATE', 'TA', 'XY') => 'FACULXYTE'
TRANSLATE('FACULTATE, 'TA', 'XY') => 'FACULXYXE' , t va fi inlocuit cu X si A cu Y, mereu
REPLACE('ADAMS', 'DA', '') => 'AMS'
TRANSLATE('ADAMS', 'DA', 'X') => 'XMS', practic pe A il sterge

SUBSTR(ENAME, 2) // 2 char de la inceput
SUBSTR(ENAME, -2) // 2 char de la final

Selectati toti ang din dep cu den citita de la tast, angajatii care contin C si care nu primesc comision. 
Numele angajatului se va concatena cu denumirea departamentului
intr-un sir in forma: angajatul Ename e in dep dname, afisandu-se alaturi de sal si comision in valori rotunjite la zeci.

*/

/*
SELECT CONCAT(A.ENAME, 'e in ' || B.DNAME) STATUS, A.SAL, ROUND(A.COMM , -2)
FROM EMP A JOIN DEPT B ON DEPTNO
WHERE
 B.DNAME = '&DEP'
 AND
 A.ENAME LIKE '%C%';

*/

/*

Sa se calculeze nr de aparitii in jobul angajatului al grupului format din ultimele 2 litere din numele angajatului.
Se vor afisa nr de aparitii si numele angajatului si jobul.

*/

SELECT ENAME, JOB, SUBSTR(ENAME, -2) ULTIMELE, REPLACE(JOB, SUBSTR(ENAME, -2), '') JOBMIC,
 (LENGTH(JOB) - LENGTH(REPLACE(JOB, SUBSTR(ENAME, -2), '')))/2 "NR APARITII"
FROM EMP
 WHERE (LENGTH(JOB) - LENGTH(REPLACE(JOB, SUBSTR(ENAME, -2), '')))/2 != 0;


/*
SYSDATE

D1 + n = D2
D1 - D2 = nrzile


Alte functii faine:
LAST_DAY(D) -> D
NEXT_DAY(D, 'MONDAY') -> urm zi de luni
EXTRACT(DAY FROM SYSDATE)
    Sau MONTH FROM SYSDATE
ADD_MONTHS(D, n) -> D

Care e ultima zi din luna, data de azi, data ultimei zile din luna, data urm zile de joi, numarul zilei de azi


*/


SELECT SYSDATE
FROM SYS.DUAL;



SELECT SYSDATE, LAST_DAY(SYSDATE),
 NEXT_DAY(SYSDATE, 'THURSDAY'),
 EXTRACT(DAY FROM SYSDATE) NR_ZI,
 TO_CHAR(SYSDATE, 'DD') CHAR_ZI
FROM SYS.DUAL;


/*


Faceti o lista cu data testarii ang din dep SALES. Testarea va avea loc dupa cel putin 2 luni de la angajare, in
ultima zi din saptamana respectiva. Se va afisa ename, den dep, data angajarii si data testarii.

*/


SELECT A.ENAME, D.DNAME, A.HIREDATE, NEXT_DAY(SYSDATE, 'SUNDAY') DATA_TESTARE
FROM EMP A JOIN DEPT D USING (DEPTNO);




/*

Sa se selecteze pentru fiecare angajat numele, anii vechimii sale, afisandu-se si salariul sau 
completat cu litera X la stanga pana la 6 caractere.

Functii utile:

LPAD -> left pad
DISTINCT -> elimina duplicatele din afisare

*/


SELECT  ENAME,
 TRUNC(MONTHS_BETWEEN(SYSDATE, HIREDATE)/12) ANI_VECHIME,
 LPAD(SAL, 6, 'X') SALM
FROM EMP;



/*

Sa se afiseze pentru fiecare angajat numele sefului sau.

*/


SELECT DISTINCT S.ENAME
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO;


/*

Sa se afiseze pentru fiecare angajat, numele lui, denumirea departamentului din care face parte,
venitul lui si o apreciere a venitului lui. Aprecierea: Venit < 1500 -> SLABUT
       Venit >= 1500 -> Ok
Functii utile:
 Union,
 Intersect

*/

SELECT A.ENAME, B.DNAME, A.SAL + NVL(A.COMM, 0) VENIT, 'SLABUT'
FROM EMP A, DEPT B
WHERE
 A.DEPTNO = B.DEPTNO
 AND
 A.SAL + NVL(A.COMM, 0) < 1500
UNION
SELECT A.ENAME, B.DNAME, A.SAL + NVL(A.COMM, 0) VENIT, 'OK'
FROM EMP A, DEPT B
WHERE
 A.DEPTNO = B.DEPTNO
 AND
 A.SAL + NVL(A.COMM, 0) >= 1500
ORDER BY 1;
-- a cata coloana din union
 

/*


Selectati numele sefilor, tuturor angajatiilor care nu fac parte dintr-un departament citit de la tastatura
si care au un venit mai mare decat Blake. Veti afisa si o valoare medie dintre salariu si comision. Pentru
fiecare angajat media e rotunjita la zeci. NU afisati duplicate.
Se va rezolva in 2 moduri.

*/

SELECT DISTINCT S.ENAME, D.DNAME, ROUND((S.SAL + NVL(S.COMM, 0))/2, -2) MEDIE, BLAKE.SAL SAL_BLAKE, S.SAL SAL_MANAGER
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO, DEPT D, EMP BLAKE
WHERE
 D.DEPTNO = A.DEPTNO
 AND
 BLAKE.ENAME = 'BLAKE'
 AND
 D.DNAME != '&DEP'
 AND
 S.SAL > BLAKE.SAL;


SELECT DISTINCT S.ENAME, D.DNAME, ROUND((S.SAL + NVL(S.COMM, 0))/2, -2) MEDIE
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO, DEPT D, EMP BLAKE
WHERE
 D.DEPTNO = A.DEPTNO
 AND
 BLAKE.ENAME = 'BLAKE'
 AND
 D.DNAME != '&DEP'
 AND
 S.SAL > BLAKE.SAL;


 SELECT A.JOB, EXTRACT(MONTH FROM A.HIREDATE) LUNA, COUNT(EMPNO)
 FROM EMP A
 WHERE A.MGR != (SELECT EMPNO FROM EMP WHERE ENAME = "KING")
 HAVING COUNT(*) = (SELECT MAX(COUNT(*)) FROM EMP
                    WHERE MGR != (SELECT EMPNO FROM EMP WHERE ENAME = "KING")
                    GROUP BY EXTRACT(MONTH FROM HIREDATE), JOB);



SELECT A.ENAME, COUNT(S.EMPNO)
FROM EMP A JOIN EMP S ON A.MGR = S.EMPNO JOIN DEPT B ON A.DEPTNO = B.DEPTNO
WHERE B.DNAME != "RESEARCH"
GROUP BY A.ENAME
HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                    FROM EMP A JOIN EMP B ON A.MGR = B.EMPNO JOIN DEPT D ON A.DEPTNO = D.DEPTNO
                    WHERE D.DNAME != 'RESEARCH'
                    GROUP BY EMPNO);

SELECT A.DNAME, B.JOB, COUNT(A.DEPTNO)
FROM DEPT A JOIN EMP B ON A.DEPTNO = B.DEPTNO
GROUP BY A.DNAME, B.JOB
HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                    FROM EMP
                    GROUP BY DEPTNO, JOB);
