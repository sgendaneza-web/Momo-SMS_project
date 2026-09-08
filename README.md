TEAM GROK   

Project Description: 
This project processes MoMo SMS transaction data (in XML format), cleans and
categorizes it, stores it in a relational database, and presents it through
a frontend dashboard for analysis.

Team Members
- Elsie Glenna Ineza
- Hillary Kayinababo
- Sonia Keza Gendaneza
- Ines Ingabire
 
Architecture Diagram: 
[Link — added once Person 2 finishes it]

Scrum Board: 
https://github.com/users/gineza1-hash/projects/1/views/1 

Project Structure

├── README.md                         
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
