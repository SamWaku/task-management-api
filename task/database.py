from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:wagwan2002@5432/taskmanagement', echo=True)