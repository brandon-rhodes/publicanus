"""Core business logic models for Publican.

You might have expected the core business logic to live next door, in
the `models` module.

Alas, you would be mistaken.

Gary Bernhardt talked in his PyCon 2012 talk about fast unit testing,
which, he asserts, means being able to test without hitting a database.
After all, if your test manipulates a database, then you are really
taking extra time to test the ORM *and* DB-API implementation *and*
database, not merely the "unit" that is under test.

But, he was asked during the Q&A, how can tests run without invoking the
database when models inherit from a persistence `Model`?  His answer was
to break business logic *away* from the persistence layer, so that your
classes can always be unit tested separately from the database, then
plugged into persistence at runtime when it is needed.

Therefore, this module contains ideas: classes that hold information,
and do things, but do *not* have the knowledge to persist themselves.
Two things happen to these classes in other code:

1. Tests can instantiate them directly, fill them with fake data, and
   pass them into the units under test with no additional expense.

2. The `models` module takes each class and turns it into a Django model
   that can load and save itself to the database, so that data gets
   saved for real when the application is up and running.

"""
class Account(object):
    """An account in our system of double-entry bookkeeping.

    An account is a bare internal identity from which funds can be
    debited and to which they can be credited.  Other tables provide
    more information about the entities listed here, depending on what
    kind of account this is.

    """
    TYPES = ('business', 'consultant', 'employee')

    def __init__(self, type):
        super(Account, self).__init__()
        assert type in self.TYPES
        self.type = type


class Transaction(object):
    """Transfer of money between accounts in our double-entry bookkeeping.

    Specifies a particular `date` on which an `amount` of money was
    removed from `debit_account` and placed in `credit_account`.  There
    is also a free-form `comment` field where users can put notes like
    "invoice #24" or "for rebuilding my model classes".

    """
    def __init__(self, date, debit_account, credit_account, amount,
                 comment=''):
        self.date = date
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.amount = amount
        self.comment = comment
