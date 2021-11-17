from simple_ddl_parser import DDLParser

ddl =  """
DROP TABLE IF EXISTS demo

create TABLE demo
(
     foo                             char(1),
     CREATE_date                     DATETIME2,
     create                    VARCHAR (20),
     ALTER_date                     DATETIME2,
     alter                    VARCHAR (20),
     DROP_date                    VARCHAR (20),
     drop VARCHAR (20),
)

"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
