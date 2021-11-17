from simple_ddl_parser import DDLParser

ddl =  """
   CREATE TABLE foo
        (
            bar_timestamp  bigint DEFAULT 1002 * extract(epoch from now()) * 1000,
            bar_timestamp2  bigint DEFAULT (1002 * extract(epoch from now()) * 1000)
        );"""
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)
