from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
from system.globals import APPS_FOLDER, WORKSPACE
from datetime import datetime

#class Hero(SQLModel, table=True):
#    id          : int | None = Field(default=None, primary_key=True)
#    name        : str
#    secret_name : str
#    age         : int | None = None #optional


class logs_rec(SQLModel, table=True):
    date : datetime  | None = Field(default_factory = datetime.now, primary_key = True)
    type : str = Field(max_length=12  , default = 'notype') 
    text : str = Field(max_length=4096, default = 'notext') 

    def to_json(self):
        return {
            "date": str(self.date).split('.')[0], 
            "type": self.type,                    
            "text": self.text,              
        }


class logic_palette_rec(SQLModel, table=True):
    #date : datetime  | None = Field(default_factory = datetime.now, primary_key = True)
    #type : str = Field(max_length=12  , default = 'notype') 
    #text : str = Field(max_length=4096, default = 'notext') 

    id           : str = 
    name         : str = 
    description  : str = 
    group        : str = 
    libimport    : str = 
    type         : str = 
    function     : str = 
    io           : str = 



    #def to_json(self):
    #    return {
    #        "date": str(self.date).split('.')[0], 
    #        "type": self.type,                    
    #        "text": self.text,              
    #    }

#		 id            :       PrimaryKey( str, 64,  default = 'Funck BLK',                ),
#        name          :       Required ( str, 32,   default = 'name here',                 ),
#        description   :       Optional ( str, 64,  default = 'description'                ),
#        group         :       Optional ( str, 24,   default = 'New Group'                  ),
#        libimport     :       Optional ( str, 128,  default = ''                           ),
#        type          :       Optional ( str, 16,   default = 'block'                      ),
#        function      :       Optional ( str, 128,  default = 'print(\'Empty Call\')'      ),
#        io            :       Optional ( Json,      default = []                           ),


#sqlite:///:memory: (or, sqlite://)
#sqlite:///relative/path/to/file.db
#sqlite:////absolute/path/to/file.db
#json_deserializer: Callable[..., Any] = ...,
#json_serializer: Callable[..., Any] = ...,        


class __workspace_db:
    def __init__(self):
        self.engine = None


    def initialize(self):
        self.engine = create_engine(f"sqlite:///{WORKSPACE}/workspace.db")
        SQLModel.metadata.create_all(self.engine)

        if __debug__:
            print("Workspace Data Base Initilized")  


    async def add_record(self, record):
        with Session(self.engine) as session:
            session.add(record)
            session.commit()


    async def load_all_records(self, model, to_json = False):
        with Session(self.engine) as session:
            statement = select(model)                  #.where(model.name == "param")
            records   = session.exec(statement).all()  #.first()

        if (to_json):
            return [rec.to_json() for rec in records]
        
        return records
    

    async def delete_all_records(self, model):
        with Session(self.engine) as session:
            statement = delete(model)
            session.exec(statement)
            session.commit() 


    def terminate(self):
        self.engine.dispose()


workspace_db  = __workspace_db()




