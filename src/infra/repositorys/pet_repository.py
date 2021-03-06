# pylint: disable=E1101

from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.infra.entities import Pets as PetsEntity
from src.infra.configs import DBConnectionHandler
from src.domain.models import Pets
from src.data.interfaces import PetRepositoryInterface


class PetRepository(PetRepositoryInterface):
    """ Class to manage Pet Repository """

    @classmethod
    def insert_pet(cls, name: str, specie: str, age: int, user_id: int) -> Pets:
        """
        Insert data in PetsEntity entity
        :param  - name: person name
                - specie: Enum with species acepted
                - age: age of the pet
                - user_id: id of the owner (FK)
        :return - tuple with new pet inserted informations
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_pet = PetsEntity(name=name, specie=specie, age=age, user_id=user_id)
                db_connection.session.add(new_pet)
                db_connection.session.commit()

                return Pets(
                    id=new_pet.id,
                    name=new_pet.name,
                    specie=new_pet.specie.value,
                    age=new_pet.age,
                    user_id=new_pet.user_id,
                )

            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    @classmethod
    def select_pet(cls, pet_id: int = None, user_id: int = None) -> List[Pets]:
        """
        Select data in PetsEntity entity by id and/or user_id
        :param  - id: Id of the registry
                - name: User name in database
        :return - List with PetsEntity selected
        """

        try:
            query_data = None

            if pet_id and not user_id:
                # Select pet by id
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsEntity)
                        .filter_by(id=pet_id)
                        .one()
                    )
                    query_data = [data]

            elif not pet_id and user_id:
                # Select pet by user_id
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsEntity)
                        .filter_by(user_id=user_id)
                        .all()
                    )
                    query_data = data

            elif pet_id and user_id:
                # Select pet by pet_id and user_id:
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsEntity)
                        .filter_by(id=pet_id, user_id=user_id)
                        .one()
                    )
                    query_data = [data]

            return query_data

        except NoResultFound:
            return []
        except:
            db_connection.session.rollback()
            raise
        finally:
            db_connection.session.close()

        return None
