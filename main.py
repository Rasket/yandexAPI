from fastapi import FastAPI, Request, HTTPException
import sqlalchemy
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, DateTime, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
import json
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
meta = MetaData()
app = FastAPI()
#for i in data:
	#print(i)
class Courier(Base):
	__tablename__ = 'courier'

	courier_id = Column(Integer, primary_key=True, autoincrement=True)
	courier_type = Column(String)
	regions = Column(String)
	working_hours = Column(String)

Cour = Table(
	'courier', meta,
	Column('courier_id', Integer, primary_key = True),
	Column('courier_type', String),
	Column('regions', String),
	Column('working_hours', String)
	)

meta.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()


@app.get("/couriers")
async def root(request: Request):
	data = await request.json()
	mass = data['data']
	ret_urn = []
	for i in mass:
		if len(i) > 4:
			key_s = list(i.keys())
			for k in key_s:
				if k not in ['courier_id', 'courier_type', 'regions', 'working_hours']:					
					raise HTTPException(status_code=400, 
					detail = {"validation_error"
					:{k:i[k]}
					}
					)
		if isinstance(i["courier_id"], int):
			pass
		else:
			raise HTTPException(status_code=400, 
				detail = {"validation_error"
				:{"courier_id":i['courier_id']}
				}
				)
		if isinstance(i['courier_type'], str):
			pass
		else:
			raise HTTPException(status_code=400, 
				detail = {"validation_error"
				:{"courier_type":i['courier_type']}
				}
				)
		if isinstance(i['regions'], list):
			pass
		else:
			raise HTTPException(status_code=400, 
				detail = {"validation_error"
				:{"regions":i['regions']}
				}
				)
		if isinstance(i['working_hours'], list):
			pass
		else:
			raise HTTPException(status_code=400, 
				detail = {"validation_error"
				:{"working_hours":i['working_hours']}
				}
				)
		ret_urn.append({'id' : i['courier_id']})
		print(i['working_hours'])
		record = Courier(courier_id = i['courier_id'], courier_type = i['courier_type'], 
			regions = ' '.join(str(e) for e in i['regions']), working_hours = ' '.join(str(e) for e in i['working_hours']))
		session.add(record)
	session.commit()
	return {"couriers" : ret_urn}


@app.patch("/couriers/{courier_id}")
async def patch_courier(courier_id: int, request: Request):
	data = await request.json()
	courier = session.query(Courier).filter_by(courier_id = courier_id).first()
	try:
		regions = data["regions"]
		courier.regions = ' '.join(str(e) for e in regions)
	except:
		raise HTTPException(status_code=400)
	try:
		working_hours = data["working_hours"]
		courier.working_hours = ' '.join(str(e) for e in working_hours)
	except:
		raise HTTPException(status_code=400)
	try:
		courier_type = data["courier_type"]
		courier.courier_type = courier_type
	except:
		raise HTTPException(status_code=400)
	return courier