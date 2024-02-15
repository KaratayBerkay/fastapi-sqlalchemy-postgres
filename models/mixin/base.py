from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_mixins.utils import classproperty
from sqlalchemy_mixins.session import SessionMixin
from sqlalchemy_mixins.inspection import InspectionMixin


class CrudMixin(InspectionMixin, SessionMixin):
    __abstract__ = True

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    @classmethod
    def filter_by(cls, list_items=None, **kwargs):
        if not list_items:
            data = cls.query.filter_by(**kwargs).populate_existing()
            return data.all(), data.count()
        data = (
            cls.query.filter_by(**kwargs)
            .order_by(
                getattr(cls, list_items.sortField).desc()
                if list_items.sortOrder == "desc"
                else getattr(cls, list_items.sortField).asc()
            )
            .limit(list_items.pageSize)
            .offset((list_items.pageNumber - 1) * list_items.pageSize)
            .populate_existing()
        )
        return data.all(), data.count()

    @classmethod
    def filter(cls, list_items=None, *arg):
        if not list_items:
            data = cls.query.filter(*arg).populate_existing()
            return data.all(), data.count()
        data = (
            cls.query.filter_by(*arg)
            .order_by(
                getattr(cls, list_items.sortField).desc()
                if list_items.sortOrder == "desc"
                else getattr(cls, list_items.sortField).asc()
            )
            .limit(list_items.pageSize)
            .offset((list_items.pageNumber - 1) * list_items.pageSize)
            .populate_existing()
        )
        return data.all(), data.count()

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
        return self

    def save(self):
        """Saves the updated model to the current entity db."""
        try:
            self.session.add(self)
            self.session.commit()
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            if isinstance(e, exc.IntegrityError):
                raise SQLAlchemyError(e.__str__())
            raise SQLAlchemyError(e.__str__())
        else:
            return self

    @classmethod
    def create(cls, **kwargs):
        """Create and persist a new record for the model
        :param kwargs: attributes for the record
        :return: the new model instance
        """
        return cls(**kwargs).save()

    def update(self, **kwargs):
        """Same as :meth:`fill` method but persists changes to database."""
        return self.fill(**kwargs).save()

    def delete(self):
        """Removes the model from the current entity session and mark for deletion."""
        self.session.delete(self)
        self.session.commit()
        self.session.flush()

    @classmethod
    def destroy(cls, *ids):
        """Delete the records with the given ids
        :type ids: list
        :param ids: primary key ids of records
        """
        for pk in ids:
            obj = cls.find(pk)
            if obj:
                obj.delete()
        cls.session.commit()
        cls.session.flush()

    @classmethod
    def get(cls, id_):
        """Find record by the id
        :param id_: the primary key
        """
        return cls.query.get(id_)

    @classmethod
    def get_or_abort(cls, id_):
        r = cls.get(id_)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SQLAlchemyError(message)
        return r

    @classmethod
    def find(cls, *arg):
        return cls.filter(*arg).order_by(None).limit(1).first()

    @classmethod
    def find_or_abort(cls, *arg):
        r = cls.find(*arg)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SQLAlchemyError(message)
        return r

    @classmethod
    def find_one(cls, **kwargs):
        return (
            cls.query.filter_by(**kwargs)
            .populate_existing()
            .order_by(None)
            .limit(1)
            .first()
        )

    @classmethod
    def find_one_or_abort(cls, **kwargs):
        r = cls.find_one(**kwargs)
        if r is None:
            message = "Record '{}' doesn't exist".format(cls.__table__.name)
            raise SQLAlchemyError(message)
        return r

    @classmethod
    def check_and_abort(cls, *arg):
        if cls.find(*arg) is not None:
            message = "Record '{}' exist".format(cls.__table__.name)
            raise SQLAlchemyError(message)
        return True

    @classmethod
    def find_or_create(cls, **kwargs):
        if kwargs is None:
            return None
        obj = cls.find_one(**kwargs)
        if obj is not None:
            return obj
        obj = cls.create(**kwargs)
        return obj

    @classmethod
    def handle_query(cls, **data):
        if "query" in data and data["query"] is not None:
            return data.get("query")
        return cls.filter()
