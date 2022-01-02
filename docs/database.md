## decryption of database

#### ``` /models.py ``` this file represent the tables in the database
have two classes ``` VLAN ``` and ``` Subnet ```

```
sql> describe VLAN

+------------+------------------+------+-----+---------+----------------+
|  Field     | Type             | Null | Key | Default | Extra          |
+------------+------------------+------+-----+---------+----------------+
| id         | int     unsigned | NO   | PRI | NULL    | auto_increment |
| name       | char(255)        | YES  |     | NULL    |                |
| descrition | char(255)        | YES  |     | NULL    |                |
+------------+------------------+------+-----+---------+----------------+
```

```
sql> describe Subnets
    
+--------------------+------------------+------+-----+---------+----------------+
| Field              | Type             | Null | Key | Default | Extra          |
+--------------------+------------------+------+-----+---------+----------------+
| id                 | int     unsigned | NO   | PRI | NULL    | auto_increment |
| ip                 | int     unsigned | NO   |     |         |                |
| mask               | int     unsigned | NO   |     | 0       |                |
| name               | char(255)        | YES  |     | NULL    |                |
| descrition         | char(255)        | YES  |     | NULL    |                |
| reserved_ips_count | int              | YES  |     | NULL    |                |
| vlan_id            | char(255)        | YES  |     | NULL    |                |
+--------------------+------------------+------+-----+---------+----------------+
```

#### ``` /database.py ``` this file create a database and represent operations with database

have a ``` DataBase ``` classe

and this class have method that represent the operations with database like (insert, select, update and delete)
