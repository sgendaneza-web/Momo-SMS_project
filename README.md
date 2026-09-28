# TEAM GROK — MoMo SMS Data Processing System

A system that stores, processes, and analyzes mobile money (MoMo) transactions from SMS data, built with a focus on data integrity, efficient querying, and future scalability.

## Team

| Name |
|------|
| Elsie Glenna Ineza |
| Hillary Kayinababo |
| Sonia Keza Gendaneza |
| Ines Ingabire |

## About the Project

MoMo SMS records arrive as XML. Our system parses that data, cleans and categorizes it, stores it in a relational database, and makes it available to clients through a REST API and a dashboard.

**Project goals**

- Analyze the MoMo XML structure and identify key entities, attributes, and relationships
- Design a comprehensive Entity Relationship Diagram (ERD)
- Implement the database in MySQL, with keys, constraints, indexes, and suitable data types
- Insert test data and perform CRUD operations
- Represent relational data as JSON
- Expose the data through a secure, documented REST API
- Compare search approaches (DSA) to show efficiency trade-offs
- Document the work and show team collaboration through GitHub and Scrum

## Project Progress

| Stage | What we did | Status |
|-------|-------------|--------|
| **Week 1** | Formed the team, set up the GitHub repo and Scrum board, drew the architecture diagram, and planned the ETL and dashboard structure | Done |
| **Week 2** | Analyzed the MoMo XML, designed the ERD, built the MySQL database (constraints, indexes, test data, CRUD), and modeled the data as JSON | Done |
| **Week 3** | Built the REST API with Basic Auth, wrote the API docs, compared linear search vs dictionary lookup, and tested with curl/Postman | Done |

Each section below is tagged with the week it was built.

---

## 1. Database Design *(Week 2)*

### Entity Relationship Diagram

The ERD is based on the MoMo XML structure and business requirements.

**Core entities:** Transactions, Users/Customers, Transaction_Categories, System_Logs

The ERD includes primary keys, foreign keys, attributes with data types, relationship cardinalities, and a junction table that resolves a many-to-many relationship.

ERD: `docs/ERD_Diagram.png`

### Design Rationale

Users, transactions, categories, and system logs are kept in separate tables to reduce duplication and protect data integrity. Users can take part in many transactions, and transactions are classified through the Transaction_Categories table. System logs are stored separately to track processing activity and errors. Foreign keys define the relationships, constraints prevent invalid data, and indexes plus well-chosen data types support query performance and scalability.

### SQL Implementation

The ERD was turned into a working MySQL database that includes:

- DDL for all tables
- Primary and foreign key constraints
- CHECK, NOT NULL, and UNIQUE constraints
- Appropriate MySQL data types
- Performance indexes and column comments
- Sample DML, test data, and CRUD operations

SQL script: `database/database_setup.sql`

The database was tested with INSERT, SELECT, UPDATE, and DELETE operations. Results and screenshots are in the Database Design Document.

### Data Accuracy & Integrity

Rules that keep the data accurate: primary keys, foreign keys, CHECK constraints, NOT NULL constraints, unique constraints, suitable data types, and indexed columns. Screenshots demonstrating them are in the Database Design Document.

## 2. JSON Data Modeling *(Week 2)*

JSON examples show how relational entities can be serialized for API responses:

- Users/Customers
- Transactions
- Transaction Categories
- System Logs
- A complete transaction object containing related user and category information

The JSON documentation also explains how SQL tables and relationships map to the JSON structures. Examples are in `examples/`.

## 3. REST API *(Week 3)*

Built to let clients (web and mobile apps) securely access the SMS data from `modified_sms_v2.xml`.

- **Data parsing:** the XML file is parsed in Python and converted into a list of JSON objects
- **Server:** plain Python using `http.server`
- **Security:** Basic Authentication, returning `401 Unauthorized` for invalid credentials

| Method | Endpoint             | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/transactions`      | List all SMS transactions      |
| GET    | `/transactions/{id}` | View one transaction           |
| POST   | `/transactions`      | Add a new transaction          |
| PUT    | `/transactions/{id}` | Update an existing transaction |
| DELETE | `/transactions/{id}` | Delete a transaction           |

Full request/response examples and error codes: `docs/api_docs.md`

**A note on security:** Basic Auth only Base64-encodes credentials (it does not encrypt them) and sends them with every request, so it is weak without HTTPS. Stronger alternatives are JWT and OAuth2, discussed in our PDF report.

### Data Structures & Algorithms

We compare two ways to find a transaction by ID on 20+ records:

- **Linear search:** scans the list, O(n)
- **Dictionary lookup:** maps `id → transaction`, O(1) on average

Code is in `dsa/`. Results and reflection are in the PDF report.

### Testing

The API is tested with curl/Postman. Screenshots (successful authenticated GET, unauthorized request, successful POST/PUT/DELETE) are in `screenshots/`.

## Setup & Running

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone <your-repo-url>
cd <repo-folder>

# Add the dataset
# Place modified_sms_v2.xml in data/raw/

# Configure environment (optional)
cp .env.example .env

# Start the API
python api/server.py

# Run the DSA comparison
python dsa/search_comparison.py
```

Example request:

```bash
curl -u admin:password http://localhost:8000/transactions
```

## Repository Structure

Week tags show when each part was added.

```
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── Architecture diagram.jpg   # Week 1
├── index.html                 # Week 1
├── docs/
│   ├── ERD_Diagram.png        # Week 2
│   ├── api_docs.md            # Week 3
│   └── Screenshots/           # Week 2
├── screenshots/               # Week 3: API test screenshots
├── database/                  # Week 2
│   ├── indexes.sql
│   └── database_setup.sql
├── examples/                  # Week 2
│   ├── category.json
│   ├── complete_transaction.json
│   ├── system_log.json
│   ├── transaction.json
│   ├── transaction_participant.json
│   └── user.json
├── data/                      # Week 1 (modified_sms_v2.xml added in Week 3)
│   ├── raw/
│   │   ├── momo.xml
│   │   └── modified_sms_v2.xml
│   ├── processed/
│   │   └── dashboard.json
│   └── logs/
│       ├── etl.log
│       └── dead_letter/
├── etl/                       # Week 1
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/                       # Week 3
│   ├── server.py
│   └── auth.py
schemas.py
├── dsa/                       # Week 3
│   ├── parse_xml.py
│   ├── modified_sms_v2.xml
│   ├── transactions.json
│   └── search_comparison.py
├── web/                       # Week 1
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── scripts/                   # Week 1
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
```

## Team Collaboration *(Week 1 onward)*

We set up Scrum and the GitHub repo in Week 1 and have kept both going every week since. The GitHub repository holds the ERD, SQL script, JSON examples, API code, and documentation, and team contributions are tracked through GitHub commits. The Scrum board is updated each sprint with completed and new tasks.

## Links

- **ERD:** https://lucid.app/lucidchart/2053b87c-b7ec-4ab9-826e-d79c89421447/edit?invitationId=inv_c4eeb7a2-aec9-481a-a07a-a7f2ef774123&page=0_0#
- **Architecture Diagram:** https://miro.com/app/board/uXjVHpCTTTc=/?share_link_id=949621607941
- **Scrum Board:** https://github.com/users/gineza1-hash/projects/1/views/1
