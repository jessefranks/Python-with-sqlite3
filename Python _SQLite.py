# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:48:54 2019

@author: Jesse Franks
"""

import sqlite3
from datetime import datetime
import re

def connect_to_db():   
    """Connect to db. RETURN connection to db and cursor object."""
  
    db = input("Enter name of Database you want to connect to: ")
    print('')
    con = sqlite3.connect(db)
    cur = con.cursor()
    return con, cur

def c_ARRIVEDATE(record): 
    """CONVERTS SQLITE TEXT DATATYPE TO PYTHON DATETIME."""
    
    old_ARRIVEDATE = record[1]
    split_ARRIVEDATE = re.split("/", old_ARRIVEDATE)
    new_ARRIVEDATE = datetime(int('20' + split_ARRIVEDATE[2]), int(split_ARRIVEDATE[0]), int(split_ARRIVEDATE[1]))
    return new_ARRIVEDATE

def c_SHIPDATE(record): 
    """CONVERTS SQLITE TEXT DATATYPE TO PYTHON DATETIME."""
    
    old_SHIPDATE = record[2]  
    split_SHIPDATE = re.split("/", old_SHIPDATE)
    new_SHIPDATE = datetime(int('20' + split_SHIPDATE[2]), int(split_SHIPDATE[0]), int(split_SHIPDATE[1]))
    return new_SHIPDATE

def QUESTION_1(cur):
    """With a single query, display the average number of days that each part spent in transit. 
     Round the answers to a whole day."""

    cur.execute( 
             """SELECT PARTS.PNAME, SHIPMENTS.ARRIVEDATE, SHIPMENTS.SHIPDATE
             FROM SHIPMENTS 
             INNER JOIN PARTS 
             ON SHIPMENTS.PARTNO = PARTS.PARTNO
             ;""" 
             )
 
    x = 0
    y = 0
    t = 0
    c = 0
    a = 0
    w = 0
    NUT = 0 
    SCREW = 0 
    WRENCH = 0
    BOLT = 0
    CAMERA = 0 
    COG = 0

    for record in cur:
    
         ARRIVEDATE = c_ARRIVEDATE(record) # convert to timedate type
         SHIPDATE = c_SHIPDATE(record) # convert to timedate type
  
        # Sum num days of each part type in transit. 
         if record[0] == 'NUT':
            x = x + 1
            NUT = (ARRIVEDATE - SHIPDATE).days  + NUT
        
         elif record[0] == 'SCREW':
            y = y + 1
            SCREW = (ARRIVEDATE - SHIPDATE).days  + SCREW
        
         elif record[0] == 'WRENCH':
            t = t + 1
            WRENCH = (ARRIVEDATE - SHIPDATE).days  + WRENCH 
        
         elif record[0] == 'BOLT':
            c = c + 1
            BOLT = (ARRIVEDATE - SHIPDATE).days  + BOLT
        
         elif record[0] == 'CAMERA':
             a = a + 1
             CAMERA = (ARRIVEDATE - SHIPDATE).days  + CAMERA
        
         else:
            w = w + 1
            COG = (ARRIVEDATE - SHIPDATE).days  + COG

     # Find avg num of days each part spent in transit. 
    avg_NUT = round( NUT / x)
    avg_SCREW = round(SCREW / y)
    avg_WRENCH = round(WRENCH / t)
    avg_BOLT = round(BOLT / c)
    avg_CAMERA = round(CAMERA / a)
    avg_COG = round(COG / w)


    print('') 
    print('Question 1:') 
    print('')

    print('NUT: ' + str(avg_NUT))
    print('SCREW: ' + str(avg_SCREW))
    print('WRENCH: ' + str(avg_WRENCH))
    print('BOLT: ' + str(avg_BOLT))
    print('CAMERA: ' + str(avg_CAMERA))
    print('COG: ' + str(avg_COG))



def QUESTION_2(cur):
    """With a single query, for each project, display the number of parts delivered in 2017."""
    cur.execute( 
            """SELECT SHIPMENTS.PROJECTNO, COUNT(SHIPMENTS.ARRIVEDATE)
            FROM SHIPMENTS 
            WHERE SHIPMENTS.ARRIVEDATE LIKE '%17' AND (SHIPMENTS.PROJECTNO = 'J1' OR SHIPMENTS.PROJECTNO = 'J2' OR
                                                       SHIPMENTS.PROJECTNO = 'J3' OR SHIPMENTS.PROJECTNO = 'J4' OR
                                                       SHIPMENTS.PROJECTNO = 'J5' OR SHIPMENTS.PROJECTNO = 'J6' OR
                                                       SHIPMENTS.PROJECTNO = 'J7' OR SHIPMENTS.PROJECTNO = 'J8')
                                                       GROUP BY SHIPMENTS.PROJECTNO;"""
                                                       )

    print('') 
    print('Question 2:') 
    print('') 
    for record in cur:
        print('Project: ' + record[0] + '   /    Number of parts delivered in 2017: ' + str(record[1]))      
    print('') 
    

def drop_tables(cur): 
    """drop all tables IF EXIST. """
    
    cur.execute("DROP TABLE IF EXISTS SUPPLIERS")
    cur.execute("DROP TABLE IF EXISTS PARTS")
    cur.execute("DROP TABLE IF EXISTS PROJECTS")
    cur.execute("DROP TABLE IF EXISTS SHIPMENTS")
 
def create_tables(con, cur): 
    """Creates all the database tables for the assignment. """
    
    cur.execute("""CREATE TABLE SUPPLIERS 
            (
            SUPPLIERNO TEXT PRIMARY KEY NOT NULL,
            SNAME TEXT, 
            STATUS TEXT, 
            CITY TEXT
            );
            """)
                    
    cur.execute("""CREATE TABLE PARTS
            ( 
            PARTNO TEXT PRIMARY KEY NOT NULL, 
            PNAME TEXT, 
            COLOR TEXT, 
            WEIGHT INTEGER,
            CITY TEXT
            );
            """)

    cur.execute("""CREATE TABLE PROJECTS
            ( 
            PROJECTNO TEXT PRIMARY KEY NOT NULL, 
            PONAME TEXT, 
            CITY TEXT
            );
            """)

    cur.execute("""CREATE TABLE SHIPMENTS
            ( 
            SUPPLIERNO TEXT NOT NULL, 
            PARTNO TEXT NOT NULL, 
            PROJECTNO TEXT NOT NULL,
            QUANTITY INTEGER,
            ShipDate TEXT,      
            ArriveDate  TEXT,
            
            PRIMARY KEY (SUPPLIERNO, PARTNO, PROJECTNO)
            );
            """)
    con.commit()


def insert_into_SUPPLIERS(cur): 
    """Insert into SUPPLIERS."""

    cur.execute("INSERT INTO SUPPLIERS VALUES('S1', 'SMITH', '20', 'LONDON');")
    cur.execute("INSERT INTO SUPPLIERS VALUES('S2', 'JONES', '10', 'PARIS');")
    cur.execute("INSERT INTO SUPPLIERS VALUES('S3', 'BLAKE', '30', 'PARIS');")
    cur.execute("INSERT INTO SUPPLIERS VALUES('S4', 'CLARK', '20', 'LONDON');")
    cur.execute("INSERT INTO SUPPLIERS VALUES('S5', 'ADAMS', '30', 'ATHENS');")
    con.commit()
 
def insert_into_PARTS(cur): 
    """Insert into PARTS."""
    
    cur.execute("INSERT INTO PARTS VALUES('P1', 'NUT', 'RED', 12, 'LONDON');")
    cur.execute("INSERT INTO PARTS VALUES('P2', 'BOLT', 'GREEN', 17,'PARIS');")
    cur.execute("INSERT INTO PARTS VALUES('P3', 'SCREW', 'BLUE', 17, 'ROME');")
    cur.execute("INSERT INTO PARTS VALUES('P4', 'SCREW', 'RED', 14, 'LONDON');")
    cur.execute("INSERT INTO PARTS VALUES('P5', 'CAMERA', 'BLUE', 32, 'PARIS');")
    cur.execute("INSERT INTO PARTS VALUES('P6', 'WRENCH', 'RED', 19, 'LONDON');")
    cur.execute("INSERT INTO PARTS VALUES('P7', 'C-O-G', 'GREEN', 12, 'ROME');")
    con.commit()
    
def insert_into_PROJECTS(cur):  
    """Insert into PROJECTS."""

    cur.execute("INSERT INTO PROJECTS VALUES('J1', 'SORTER', 'PARIS');")
    cur.execute("INSERT INTO PROJECTS VALUES('J2', 'PUNCH', 'ROME');")
    cur.execute("INSERT INTO PROJECTS VALUES('J3', 'READER', 'ATHENS');")
    cur.execute("INSERT INTO PROJECTS VALUES('J4', 'CONSOLE', 'ATHENS');")
    cur.execute("INSERT INTO PROJECTS VALUES('J5', 'COLLATOR', 'LONDON');")
    cur.execute("INSERT INTO PROJECTS VALUES('J6', 'TERMINAL', 'OSLO');")
    cur.execute("INSERT INTO PROJECTS VALUES('J7', 'TAPE', 'LONDON');")
    cur.execute("INSERT INTO PROJECTS VALUES('J8', 'DRUM', 'LONDON');")
    con.commit()

def insert_into_SHIPMENTS(cur): 
    """Insert into SHIPMENTS."""

    cur.execute("INSERT INTO SHIPMENTS VALUES('S1', 'P1', 'J1', 200, '1/5/18', '1/25/19');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S1', 'P1', 'J4', 700, '2/1/18', '2/4/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S1', 'P3', 'J1', 450, '12/15/17', '1/8/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S1', 'P3', 'J2', 210, '11/2/17', '11/18/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S1', 'P3', 'J3', 700, '8/5/17', '9/1/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S2', 'P3', 'J4', 509, '8/5/17', '8/9/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S2', 'P3', 'J5', 600, '7/3/17', '7/29/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S2', 'P3', 'J6', 400, '9/3/17', '9/10/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S2', 'P3', 'J7', 812, '2/5/18', '2/15/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S3', 'P5', 'J6', 750, '1/6/18', '1/14/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S3', 'P3', 'J2', 215, '3/5/18', '3/15/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S3', 'P4', 'J1', 512, '2/27/18', '3/6/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S3', 'P6', 'J2', 313, '6/15/17', '6/27/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S4', 'P6', 'J3', 314, '6/17/17', '6/30/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S4', 'P2', 'J6', 250, '5/2/17', '6/2/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S4', 'P5', 'J5', 179, '5/5/17', '5/10/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S4', 'P5', 'J2', 513, '9/15/17', '10/1/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P7', 'J4', 145, '10/2/17', '10/23/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P1', 'J5', 269, '11/5/17', '11/17/17');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P3', 'J7', 874, '12/12/17', '1/4/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P4', 'J4', 476, '12/22/17', '1/16/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P5', 'J4', 529, '5/7/18', '6/1/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P6', 'J4', 318, '4/23/18', '5/2/18');")
    cur.execute("INSERT INTO SHIPMENTS VALUES('S5', 'P2', 'J4', 619, '4/20/18', '5/2/18');")
 
    con.commit()


###############################################################################
####################### MAIN BLOCK ############################################

con, cur = connect_to_db() # connect to db.
drop_tables(cur) # drop all tables IF EXIST.
create_tables(con,cur) # create all db tables.

###################### INSERT BLOCK ###########################################
insert_into_SUPPLIERS(cur)
insert_into_PARTS(cur)
insert_into_PROJECTS(cur)
insert_into_SHIPMENTS(cur)
##################### END INSERT BLOCK ########################################

QUESTION_1(cur) # H Q1
QUESTION_2(cur) #  Q2

con.commit()
con.close()

###############################################################################
###################### END MAIN BLOCK #########################################
###############################################################################   




             








    
    
    
    
    
    
    
    
    
    
    