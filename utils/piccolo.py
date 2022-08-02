from piccolo.table import Table as BaseTable
from piccolo.columns import m2m
import inspect
from uuid import uuid4

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
