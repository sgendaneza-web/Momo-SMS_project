TEAM GROK   

Project Description: 
Building on our Week 1 team setup, this project focuses on designing and implementing the database foundation for a MoMo SMS data processing system.

The system is designed to store, process, and analyze mobile money transactions while maintaining data integrity, efficient querying, and future scalability. The project covers ERD design, MySQL implementation, JSON data modeling, testing, and team collaboration.

Team Members
- Elsie Glenna Ineza
- Hillary Kayinababo
- Sonia Keza Gendaneza
- Ines Ingabire

Our project aims to:

- Analyze the MoMo XML structure and identify key entities, attributes, and relationships.
- Design a comprehensive Entity Relationship Diagram (ERD).
- Implement the database using MySQL and SQL.
- Apply primary keys, foreign keys, constraints, indexes, and appropriate data types.
- Insert test data and perform CRUD operations.
- Represent relational data using JSON.
- Document the database design and demonstrate team collaboration through GitHub and Scrum.
  
1. Entity Relationship Diagram

The ERD was designed based on the MoMo XML structure and business requirements.

The core entities are:

Transactions
Users/Customers
Transaction_Categories
System_Logs

The ERD includes primary keys, foreign keys, appropriate attributes and data types, relationship cardinalities, and a junction table to resolve a many-to-many relationship.

ERD: docs/erd_diagram.png

Design Rationale

The database separates users, transactions, categories, and system logs to reduce duplication and maintain data integrity. Users can participate in multiple transactions, while transactions are classified through the Transaction_Categories table. System logs are stored separately to track processing activities and errors.

Foreign keys establish relationships between entities, while constraints help prevent invalid data. A junction table resolves the many-to-many relationship identified during the analysis. Indexes and appropriate data types are included to improve query performance and support future scalability.

2. SQL Database Implementation

The ERD was transformed into a working MySQL database.

The SQL implementation includes:

- DDL statements for all tables
- Primary and foreign key constraints
- CHECK constraints where appropriate
- Appropriate MySQL data types
- Performance indexes
- Column comments
- Sample DML statements
- Test data
- CRUD operations

SQL Script: database/database_setup.sql

The database was tested using basic INSERT, SELECT, UPDATE, and DELETE operations. Query results and screenshots are included in the Database Design Document.

3. JSON Data Modeling

JSON examples were created to demonstrate how the relational database entities can be serialized for API responses.

The examples include:

- Users/Customers
- Transactions
- Transaction Categories
- System Logs
- A complete transaction object containing related user and category information

JSON Examples: examples/json_schemas.json

The JSON documentation also explains how the SQL tables and their relationships map to the JSON structures.

4. Database Security and Accuracy

The database includes rules designed to improve data accuracy and integrity, including:

- Primary keys
- Foreign keys
- CHECK constraints
- NOT NULL constraints where required
- Unique constraints where applicable
- Appropriate data types
- Indexed columns

Screenshots demonstrating these rules are included in the Database Design Document.

5. Team Collaboration

The project continues the collaborative practices established in Week 1.

The GitHub repository contains the ERD, SQL script, JSON examples, and project documentation. Team contributions are demonstrated through GitHub commits.

The Scrum board has also been updated with completed Week 1 tasks and the new Week 2 sprint tasks.

Team Participation Sheet
Link: https://docs.google.com/spreadsheets/d/1gl_vX1CCEraUrOGmpLTPhHD2sr1nROxf8aGF37MW0eE/edit?gid=0#gid=0)

ERD
Link: https://lucid.app/lucidchart/2053b87c-b7ec-4ab9-826e-d79c89421447/edit?invitationId=inv_c4eeb7a2-aec9-481a-a07a-a7f2ef774123&page=0_0#

Architecture diagram
Link: https://miro.com/app/board/uXjVHpCTTTc=/?share_link_id=949621607941

Scrum Board
Link: https://github.com/users/gineza1-hash/projects/1/views/1

Project Structure

├── README.md  
├── Docs/ 
│   ├── Screenshots
│   └── ERD_Diagram.png/ 
├── database 
│   └── database_setup.sql 
├── examples  
│   ├── category.json
│   └── user.json 
├── .gitignore
├── Architecture diagram.jpg  
├── .env.example                      
├── requirements.txt                  
├── index.html                        
├── web/
│   ├── styles.css                    
│   ├── chart_handler.js              
│   └── assets/                       
├── data/
│   ├── raw/                          
│   │   └── momo.xml
│   ├── processed/                    
│   │   └── dashboard.json            
│   ├── db.sqlite3                    
│   └── logs/
│       ├── etl.log                   
│       └── dead_letter/              
├── etl/
│   ├── __init__.py
│   ├── config.py                     
│   ├── parse_xml.py                  
│   ├── clean_normalize.py            
│   ├── categorize.py                
│   ├── load_db.py                   
│   └── run.py                        
├── api/                              
│   ├── __init__.py
│   ├── app.py                        
│   ├── db.py                         
│   └── schemas.py                    
├── scripts/
│   ├── run_etl.sh                   
│   ├── export_json.sh                
│   └── serve_frontend.sh             
└── tests/
    ├── test_parse_xml.py             
    ├── test_clean_normalize.py
    └── test_categorize.py 
