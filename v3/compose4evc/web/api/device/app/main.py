# $ python -m uvicorn app.main:app --reload --host=0.0.0.0 --port 8004

# fastapi
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

# sqlite
import sqlite3

# datetime
from datetime import datetime

# os
from os import environ
import json
from typing import Optional

# access token
import secrets

# config
import configparser



#--------------------------------------------------------------
# Edge Device
#--------------------------------------------------------------

class EdgeBase(BaseModel):
    name: str    
    host: str    
    port: int
    description: str
    access_token: str
    done: bool
    
class EdgeUpdate(BaseModel):
    name: str  
    host: str    
    port: int
    description: str
    access_token: str
    done: bool
    updated_at: str

class EdgeListup(BaseModel):
    id : str
    name: str  
    host: str    
    port: int
    description: str
    access_token: str
    done: bool
    created_at: str
    updated_at: str

class EdgeDatabase:
    def __init__(self): 
        
        # 사용자 config 파라미터를 해석합니다.
        self.fpath_config = 'config.cfg' # hard coding
        config = configparser.ConfigParser()
        config.read(self.fpath_config)
        sections = config.sections()
        self.sqlite3_edge_db = config['default']['sqlite3_edge_db']
        self.access_token_size = config['default']['access_token_size']
            
        # DB파일을 연결합니다.
        self.conn = sqlite3.connect(self.sqlite3_edge_db)
        self.create_table()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS edges 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL, 
                     host TEXT NOT NULL, 
                     port INTEGER NOT NULL,
                     description TEXT NOT NULL, 
                     access_token TEXT NOT NULL, 
                     done BOOLEAN NOT NULL DEFAULT False,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
        self.conn.execute(query)

        
    def get_all_edges(self):
        query = "SELECT * FROM edges"
        cursor = self.conn.execute(query)
        edges = []
        for row in cursor:
            edge = {'id': row[0], 'name': row[1], 'host': row[2],  'port': row[3], 'description': row[4], 'access_token': row[5], 'done': row[6], 'created_at': row[7], 'updated_at': row[8]}
            edges.append(edge)
        return edges

    
    def get_edge_by_id(self, edge_id):
        query = f"SELECT * FROM edges WHERE id = {edge_id}"
        cursor = self.conn.execute(query)
        row = cursor.fetchone()
        if row:
            edge = {'id': row[0], 'name': row[1], 'host': row[2],  'port': row[3], 'description': row[4], 'access_token': row[5], 'done': row[6], 'created_at': row[7], 'updated_at': row[8]}
            return edge
        else:
            raise HTTPException(status_code=404, detail="Edge not found")

            
    def get_edge_by_access_token(self, edge_access_token):
        query = f"SELECT * FROM edges WHERE access_token = '{edge_access_token}'"
        cursor = self.conn.execute(query)
        edges = []
        try:
            for row in cursor:
                edge = {'id': row[0], 'name': row[1], 'host': row[2],  'port': row[3], 'description': row[4], 'access_token': row[5], 'done': row[6], 'created_at': row[7], 'updated_at': row[8]}
                edges.append(edge)
            return edges
    
        except:
            raise HTTPException(status_code=404, detail="Edge not found")

            
    def create_edge(self, edge):     
        created_at = datetime.now()
        updated_at = datetime.now()
        access_token = secrets.token_hex(nbytes=int(self.access_token_size))
        query = f"INSERT INTO edges (name, host, port, description, access_token, done, created_at, updated_at) VALUES ('{edge.name}', '{edge.host}', {edge.port}, '{edge.description}', '{access_token}', {edge.done}, '{created_at}', '{updated_at}')"
        cursor = self.conn.execute(query)
        self.conn.commit()
        return self.get_edge_by_id(cursor.lastrowid)

    
    def update_edge_by_id(self, edge_id, edge):
        updated_at = datetime.now()
        
        print(f'updated_at = {updated_at}')
        
        query = f"UPDATE edges SET name = '{edge.name}', host = '{edge.host}', port = {edge.port}, description = '{edge.description}',  access_token = '{edge.access_token}', done = {edge.done}, updated_at = '{updated_at}' WHERE id = {edge_id}"
        
        print(f'query = {query}')
        cursor = self.conn.execute(query)
        self.conn.commit()
        return self.get_edge_by_id(edge_id)

    
    def delete_edge_by_id(self, edge_id):
        query = f"DELETE FROM edges WHERE id = {edge_id}"
        cursor = self.conn.execute(query)
        self.conn.commit()
        if cursor.rowcount > 0:
            return JSONResponse(status_code=204)
        else:
            raise HTTPException(status_code=404, detail="Edge not found")



#--------------------------------------------------------------
# Time Series Data Source
#--------------------------------------------------------------

class TimeSeriesBase(BaseModel):
    created_at: str
    json_data: str
    done: bool
    
class TimeSeriesAll(BaseModel):
    access_token: str
    created_at: str
    json_data: str
    done: bool

class TimeSeriesDatabase:
    def __init__(self): 
        
        # 사용자 config 파라미터를 해석합니다.
        self.fpath_config = 'config.cfg' # hard coding
        config = configparser.ConfigParser()
        config.read(self.fpath_config)
        sections = config.sections()
        self.sqlite3_ts_db = config['timeseries']['sqlite3_ts_db']
            
        # DB파일을 연결합니다.
        self.conn = sqlite3.connect(self.sqlite3_ts_db)
        self.create_table()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS ts 
                    (access_token TEXT NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     json_data TEXT NOT NULL, 
                     done BOOLEAN NOT NULL DEFAULT False)'''
        self.conn.execute(query)

    def get_all_ts(self):
        query = "SELECT * FROM ts"
        cursor = self.conn.execute(query)
        tss = []
        for row in cursor:
            ts = {'created_at': row[1], 'json_data': row[2], 'done': row[3]}
            tss.append(ts)
        return tss


    def get_all_ts_debug(self):
        query = "SELECT * FROM ts"
        cursor = self.conn.execute(query)
        tss = []
        for row in cursor:
            ts = {'access_token': row[0], 'created_at': row[1], 'json_data': row[2], 'done': row[3]}
            tss.append(ts)
        return tss
    
    def get_ts_by_access_token(self, ts_access_token):
        query = f"SELECT * FROM ts WHERE access_token = '{ts_access_token}'"
        cursor = self.conn.execute(query)
        tss = []
        try:
            for row in cursor:
                ts = {'created_at': row[1], 'json_data': row[2], 'done': row[3]}
                tss.append(ts)
            return tss
    
        except:
            raise HTTPException(status_code=404, detail="Edge not found")

    def create_ts(self, ts):     
        created_at = datetime.now()
        query = f"INSERT INTO ts (access_token, created_at, json_data, done) VALUES ('{ts.access_token}', '{created_at}', '{ts.json_data}', {ts.done})"
        cursor = self.conn.execute(query)
        self.conn.commit()
        return {'status' : 'ok'}

    
    
    
#--------------------------------------------------------------
# API for Edge
#--------------------------------------------------------------
app = FastAPI()
db_edge = EdgeDatabase()
db_ts = TimeSeriesDatabase()

# Redirection
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/')

@app.get("/api/edges", response_model=List[EdgeListup])
async def get_all_edges():
    print('hi')
    try:
        edges = db_edge.get_all_edges()
        return edges
    except HTTPException as ex:
        raise ex
        
@app.get("/api/edges/id/{edge_id}", response_model=EdgeListup)
async def get_edge_by_id(edge_id: int):
    try:
        edge = db_edge.get_edge_by_id(edge_id)
        return edge
    except HTTPException as ex:
        raise ex
        
@app.get("/api/edges/token/{access_token}", response_model=List[EdgeListup])
async def get_edge_by_access_token(access_token: str):
    try:
        edges = db_edge.get_edge_by_access_token(access_token)
        return edges
    except HTTPException as ex:
        raise ex

@app.post("/api/edges/create", response_model=EdgeListup)
async def create_edge(edge: EdgeBase):
    try:
        new_edge = db_edge.create_edge(edge)
        return new_edge
    except HTTPException as ex:
        raise ex

@app.put("/api/edges/update/{edge_id}", response_model=EdgeListup)
async def update_edge_by_id(edge_id: int, edge: EdgeBase):
    try:
        updated_edge = db_edge.update_edge_by_id(edge_id, edge)
        return updated_edge
    except HTTPException as ex:
        raise ex
        
@app.delete("/api/edges/delete/{edge_id}")
async def delete_edge_by_id(edge_id: int):
    try:
        response = db_edge.delete_edge_by_id(edge_id)
        return response
    except HTTPException as ex:
        raise ex

# Reserved
'''
@app.get("/get_api_key")
def get_api_key():
    api_key = ""    
    
    try:
        with open('appconfig.conf') as f:
            js = json.load(f)
            api_key = js["api_key"]
            return {"api_key": api_key}

    except IOError:
        print("appconfig.conf not accessible")

    return {"API_KEY: {}".format(api_key)}
'''

#--------------------------------------------------------------
# API for TimeSeries DataSource
#--------------------------------------------------------------
@app.post("/api/ts/create")
async def create_ts(ts: TimeSeriesAll):
    try:
        new_ts = db_ts.create_ts(ts)
        return new_ts
    except HTTPException as ex:
        raise ex
        
@app.get("/api/ts", response_model=List[TimeSeriesBase])
async def get_all_ts():
    try:
        tss = db_ts.get_all_ts()
        return tss
    except HTTPException as ex:
        raise ex
        
@app.get("/api/ts/debug", response_model=List[TimeSeriesAll])
async def get_all_ts_debug():
    try:
        tss = db_ts.get_all_ts_debug()
        return tss
    except HTTPException as ex:
        raise ex

@app.get("/api/ts/token/{access_token}", response_model=List[TimeSeriesBase])
async def get_ts_by_access_token(access_token: str):
    try:
        tss = db_ts.get_ts_by_access_token(access_token)
        return tss
    except HTTPException as ex:
        raise ex

#--------------------------------------------------------------
# Entry point
#--------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)