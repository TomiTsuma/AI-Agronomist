# This is a conceptual reference, not actual model code if using raw SQL

SAMPLERESULTS_TABLE = {
    "name": "SampleResults",
    "columns": {
        "batch_date": "DATETIME",
        "sample_code": "VARCHAR(255)",
        "chemical_name": "VARCHAR(255)",
        "result": "DOUBLE",
        "client_name": "VARCHAR(255)",
        "farm_name": "VARCHAR(255)"
    }
}

CLIENTS_TABLE = {
    "name": "Clients",
    "columns": {
        "client_id": "INT AUTO_INCREMENT PRIMARY KEY",
        "client_name": "VARCHAR(255)",
    }
}


FARMS_TABLE = {
    "name": "Clients",
    "columns": {
        "client_id": "INT FOREIGN KEY",
        "farm_code": "INT AUTO_INCREMENT PRIMARY KEY",
        "farm_name": "VARCHAR(255)",
    }
}