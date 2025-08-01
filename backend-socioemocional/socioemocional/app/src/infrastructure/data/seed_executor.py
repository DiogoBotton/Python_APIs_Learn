from fastapi import HTTPException, Response, Depends
from src.infrastructure.data.seed.db_seeder import DbSeeder

class SeedExecutor:
    def __init__(self, db_seeder: DbSeeder = Depends()):
        self.db_seeder = db_seeder

    def execute(self):
        try:
            self.db_seeder.clean_db()
            self.db_seeder.seed_users()

            return Response(status_code=200)
        except:
            raise HTTPException(status_code=500, detail="Houve algum erro ao realizar o seed da aplicação.")