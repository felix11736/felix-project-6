import os
import connection
import sqlparse
import pandas as pd


if __name__ == '__main__':
    print('[INFO] Service ETL is Starting ...')
    
    # connection data source
    conf = connection.config('marketplace_prod')
    conn, engine = connection.psql_conn(conf, 'DataSource')
    cursor = conn.cursor()

    # connection dwh
    conf_dwh = connection.config('dwh')
    conn_dwh, engine_dwh = connection.psql_conn(conf_dwh, 'DataWarehouse')
    cursor_dwh = conn_dwh.cursor()

    #connection hadoop 
    conf_hadoop = connection.config('hadoop')
    client = connection.hadoop_conn(conf_hadoop)
     
    # get query string
    path_query = os.getcwd()+'/query/'
    query = sqlparse.format(
        open(path_query+'query.sql', 'r').read(), strip_comments=True
    ).strip()

    # get schema dwh design
    path_dwh_design = os.getcwd()+'/query/'
    dwh_design = sqlparse.format(
        open(path_dwh_design+'dwh_design.sql', 'r').read(), strip_comments=True
    ).strip()

    try:
        # get data
        print('[INFO] Service ETL is Running ...')
        df = pd.read_sql(query, engine)

        # # create schema dwh
        # cursor_dwh.execute(dwh_design)
        # conn_dwh.commit()

        # # ingest data to dwh
        # df.to_sql('dim_orders', engine_dwh, if_exists='append', index=False)
        
        #ingst data to hadoop
        with client.write(
            '/digitalskola/project/dim_orders_felix.csv',
             encoding='utf-8'
             ) as writer:
                  df.to_csv(writer, index=False)

        print('[INFO] Service ETL is Success ...')
    except Exception as e:
        print('[INFO] Service ETL is Failed ...')
        print(e)