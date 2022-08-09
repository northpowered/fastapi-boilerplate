from piccolo.table import Table as BaseTable
from piccolo.columns import m2m, base
import inspect
from uuid import uuid4
from typing import Any, Optional





def uuid4_for_PK()->str:
    """
    Just returns UUID4 in string format
    Using for 'default' kwarg in PK TEXT column

        default=uuid4_for_PK #for column
        uuid4_for_PK() #for other cases

    Returns:
        str: uuid4 string
    """
    return str(uuid4())

def get_pk_from_resp(resp: Any, attr: str) -> str | None:
    try:
        return resp[0].get('id')
    except (IndexError, TypeError, ValueError, AttributeError):
        return None

class Table(BaseTable):
    def __init__(self, ignore_missing: bool = False, exists_in_db: bool = False, **kwargs):
        super().__init__(ignore_missing, exists_in_db, **kwargs) # type: ignore
    
    async def __join_field(self, field: str, ignore: bool=False)->list:
        """
        Runs get_m2m for a FIELD of object. Catches ValueError, when there are
        no relations in M2M table and returns empty list(). If ignore flag is
        True, also returns empty list
        Args:
            field (str): Attr name
            ignore (bool, optional): Flag for include and exclude logic of join_m2m. Defaults to False.

        Returns:
            list: list of related objects, or an empty one
        """
        if ignore:
            return list()
        try:
            return await self.get_m2m(self.__getattribute__(field)).run()
        except ValueError:
            return list()

    async def join_m2m(
        self, 
        include_fields: set[str] | list[str] | None=None, 
        exclude_fields: set[str] | list[str] | None=None
        ):
        """
        Runs get_m2m() method for all M2M fields of object. Can be useful for
        complex PyDantic models in READ actions. Returns empty list() for an
        attribute, if there are no relations to this object.

        Optional, you can include or exclude fields to define which attrs should
        be joined. Setting either include_fields, and exclude_fields will raise 
        AssertionError.

        .. code-block:: python

            >>> band = await Band.objects().get(Band.name == "Pythonistas")
            >>> await band.join_m2m()
            >>> band.genres
        [<Genre: 1>, <Genre: 2>]
            >>> band.tours
        [<Tour: 1>,<Tour: 2>,<Tour: 3>]

        include_fields example:

        .. code-block:: python

            >>> await band.join_m2m(include_fields=['genres'])
            >>> band.genres
        [<Genre: 1>, <Genre: 2>]
            >>> band.tours
        []

        exclude_fields example:

        .. code-block:: python

            >>> await band.join_m2m(exclude_fields=['genres'])
            >>> band.genres
        []
            >>> band.tours
        [<Tour: 1>,<Tour: 2>,<Tour: 3>]

        Args:
            include_fields (set[str] | list[str] | None, optional): Only this fields will be joined to base model`s object. Defaults to None.
            exclude_fields (set[str] | list[str] | None, optional): This fields will be excluded from join. Defaults to None.
        """
        assert (include_fields==None) or (exclude_fields==None), "Only one of FIELDS arguments can exist"
        if not include_fields is None:
            assert isinstance(include_fields,set | list), "include_fields MUST be set, list or None"
        if not exclude_fields is None:
            assert isinstance(exclude_fields,set | list), "exclude_fields MUST be set, list or None"
        m2m_fields: set = set([field for field, object in inspect.getmembers(
                self, 
                lambda a:(
                    isinstance(
                        a,
                        m2m.M2M
                    )
                )
            )
        ])
        ignore_fields: list = list()
        if include_fields:
            ignore_fields = list(m2m_fields.difference(set(include_fields)))
        if exclude_fields:
            ignore_fields = list(m2m_fields.intersection(set(exclude_fields)))
        for field in list(m2m_fields):
            ignore: bool = False
            if field in ignore_fields:
                ignore = True
            self.__setattr__(
                field, #M2M attr name
                await self.__join_field(
                    field=field,
                    ignore=ignore
                )
            )


#@dataclass
class UniqueConstraint():

    def __init__(self, columns: list[str]) -> None:
        self.columns = columns
"""      
        self._meta = base.ColumnMeta(
            # null=null,
            # primary_key=primary_key,
            # unique=unique,
            # index=index,
            # index_method=index_method,
            # params=kwargs,
            # required=required,
            # help_text=help_text,
            # choices=choices,
            # _db_column_name=db_column_name,
            # secret=secret,
        )

        self._alias: Optional[str] = None

    @property
    def ddl(self) -> str:
"""
        #Used when creating tables.
"""
        query = f'"{self._meta.db_column_name}" {self.column_type}'
        if self._meta.primary_key:
            query += " PRIMARY KEY"
        if self._meta.unique:
            query += " UNIQUE"
        if not self._meta.null:
            query += " NOT NULL"

        foreign_key_meta: t.Optional[ForeignKeyMeta] = getattr(
            self, "_foreign_key_meta", None
        )
        if foreign_key_meta:
            references = foreign_key_meta.resolved_references
            tablename = references._meta.tablename
            on_delete = foreign_key_meta.on_delete.value
            on_update = foreign_key_meta.on_update.value
            target_column_name = (
                foreign_key_meta.resolved_target_column._meta.name
            )
            query += (
                f" REFERENCES {tablename} ({target_column_name})"
                f" ON DELETE {on_delete}"
                f" ON UPDATE {on_update}"
            )

        if self.__class__.__name__ not in ("Serial", "BigSerial"):
            default = self.get_default_value()
            sql_value = self.get_sql_value(value=default)
            query += f" DEFAULT {sql_value}"

        return 
"""  