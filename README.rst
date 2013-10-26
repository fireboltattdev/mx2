Python M2X API Client
=====================

The AT&T `M2X API`_ provides all the needed operations to connect your devices to `AT&T's
M2X service`_. This client provides an easy to use interface for
your favorite language, Python.

The library provides an interface to navigate and register your
data source values with the `AT&T's M2X service`_, while supporting Python 2 and
3.

There are only a few dependencies:

* requests_ (version ``2.0.0``)
* iso8601_ (version ``0.1.8``)


Getting Started
------------
1. Signup for an M2X Account: https://m2x.att.com/signup
2. Obtain your *Master Key* from the Master Keys tab of your Account Settings: https://m2x.att.com/account
3. Create your first Data Source Blueprint and copy its *Feed ID*: https://m2x.att.com/blueprints
4. Review the M2X API Documentation: https://m2x.att.com/developer/documentation/overview

If you have questions about any M2X specific terms, please consult the M2X glossary: https://m2x.att.com/developer/documentation/glossary


Installation
------------

The project is very easy to install — the different options are::

    $ pip install m2x

or::

    $ easy_install m2x

or cloning the repository::

    $ git clone https://github.com/citrusbyte/m2x-python.git
    $ cd m2x-python
    $ python setup.py install


Library structure
-----------------

Currently, the client supports ``API v1`` and all M2X API documents can be found at
`M2X API Documentation`_.

* Client_

  In order to communicate with the M2X API you need an instance of `M2XClient`_ – it
  will provide an interface to all the structures and collections in your
  project. The client will return iterable types representing the main entities
  in M2X, these iterable types are subclasses of Collection_.

* API_

  The API_ is just the interface that knowns how to communicate with the service
  by defining the needed API base path (API version related) and sending the
  needed headers. This class is for internal use only.

* Collections_

  A Collection is an iterable type containing Item_ instances, they provide
  the needed interface to get all (or single) items from the service and create
  new ones. Important methods are:

  - Load items (``.load()`` method)
  - Get item details (``.details(id)`` method)
  - Create items (``.create(**attrs)`` method)

  Attributes required for item creation and update aren't enforced at the
  moment, leaving it open by using ``**attrs`` allows to support future API
  improvements removing future code updates dependency to support new
  attributes.

  A Collection_ extends ``list`` but not all the list methods have an impact on
  the storage service, at least not right now — don't rely on them except for
  data access (iteration, index access, slice, etc.).

* Item_

  An Item_ is the direct representation of an individual instance in the
  storage service. They provide the needed methods to update an instance and
  remove it. Important methods are:

  - Update item attributes (``.update(**attrs)`` method)
  - Remove item from the store (``.remove()`` method)

Item_ and Collection_ instances have a ``data`` attribute (``dict`` type) which
contains the values returned by the server, this ``data`` is processed (dates
are converted to native python ``datetime`` instances). The unprocessed data is
stored in the ``raw_data`` attribute. To ease attribute access the classes
define ``__getattr__`` to access any value in the ``data`` attribute as if they
were instance attributes.


Client usage
------------

To create a client instance only a single parameter, the API Key, is needed. Your Master API Key can
be found in your account_ settings, or a feed API key is available in your Data Source
details screen. To create a client instance just do::

    >>> from m2x.client import M2XClient
    >>> client = M2XClient(key='your api key here')

The client provides an interface to access your Blueprints_, Batches_,
DataSources_, Feeds_, Keys_.

* Blueprints

  ``Blueprints`` is accessible by the ``blueprints`` property in a ``M2XClient``
  instance. The property is an iterable type where each entry is a Blueprint_
  instance.

  - Iteration::

        >>> for blueprint in client.blueprints:
        >>>    ...

  - Creation::

        >>> blueprint = client.blueprints.create(
        ...     name='Blueprint',
        ...     description='Blueprint description',
        ...     visibility='public'
        ... )
        <m2x.blueprints.Blueprint at 0x365c590>

  - Update (following the previous code)::

        >>> blueprint.update(
        ...     name='Blueprint2',
        ...     description='Blueprint2 description',
        ...     visibility='private',
        ...     status='enabled'
        ... )

    The parameters ``name``, ``description`` and ``visibility`` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code ``422``).

  - Removal (following the previous code)::

        >>> blueprint.remove()

  - Single item retrieval::

        >>> blueprint = client.blueprints.details(
        ...     '188a0afb3adc379706e780a4eafbd153'
        ... )
        <m2x.blueprints.Blueprint at 0x1652fd0>

    The parameter to ``.details()`` is the Blueprint_ ID.

  - Related Feed

    A Blueprint_ has a related feed created automatically, to get the feed
    access the ``feed`` property::

        >>> related_feed = blueprint.feed
        <m2x.feeds.Feed at 0x1652fd0>

* Batches

  ``Batches`` is accessible by the ``batches`` property in a ``M2XClient``
  instance. The property is an iterable type where each entry is a Batch_
  instance.

  - Iteration::

        >>> for batch in client.batches:
        >>>    ...

  - Creation::

        >>> batch = client.batches.create(
        ...     name='Batch',
        ...     description='Batch description',
        ...     visibility='public',
        ... )
        <m2x.batches.Batch at 0x365c500>

  - Update (following the previous code)::

        >>> batch.update(
        ...     name='Batch2',
        ...     description='Batch2 description',
        ...     visibility='private',
        ...     status='enabled'
        ... )

    The parameters ``name``, ``description`` and ``visibility`` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code ``422``).

  - Removal (following the previous code)::

        >>> batch.remove()

  - Single item retrieval::

        >>> batch = client.batches.details(
        ...     '7cc8f518983dd62254b98d976400a3d4'
        ... )
        <m2x.batches.Batch at 0x1652fd0>

    The parameter to ``.details()`` is the Batch_ ID.

  - To access all the datasources in this Batch_ use the ``datasources``
    property which also provides the needed method to create new DataSource_::

        >>> batch.datasources
        [<m2x.datasources.DataSource at 0x2674b10>]
        >>> batch.datasources.create(serial='abc123')
        [<m2x.datasources.DataSource at 0x2674b10>, <m2x.datasources.DataSource at 0x2674d50>]

  - Related Feed

    A Batch_ has a related feed created automatically, to get the feed access
    the ``feed`` property::

        >>> related_feed = batch.feed
        <m2x.feeds.Feed at 0x1652fd0>

* DataSources

  ``DataSources`` is accessible by the ``datasources`` property in a
  ``M2XClient`` instance. The property is an iterable type where each entry is
  a DataSource_ instance.

  - Iteration::

        >>> for datasource in client.datasources:
        >>>    ...

  - Creation::

        >>> datasource = client.datasources.create(
        ...     name='Datasource',
        ...     description='Datasource description',
        ...     visibility='public',
        ... )
        <m2x.datasources.DataSource at 0x365c500>

  - Update (following the previous code)::

        >>> datasource.update(
        ...     name='Datasource2',
        ...     description='Datasource2 description',
        ...     visibility='private',
        ...     status='enabled'
        ... )

    The parameters ``name``, ``description`` and ``visibility`` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code ``422``).

  - Removal (following the previous code)::

        >>> datasource.remove()

  - Single item retrieval::

        >>> datasource = client.datasources.details(
        ...     '61179472a42583cffc889478010a092a'
        ... )
        <m2x.datasources.DataSource at 0x1652fd0>

    The parameter to ``.details()`` is the DataSource_ ID.

  - Related Feed

    A DataSource_ has a related feed created automatically, to get the feed
    access the ``feed`` property::

        >>> related_feed = datasource.feed
        <m2x.feeds.Feed at 0x1652fd0>

* Keys

  ``Keys`` is accessible by the ``keys`` property in a ``M2XClient`` instance.
  The property is an iterable type where each entry is a Key_ instance.

  - Iteration::

        >>> for key in client.keys
        >>>    ...

  - Creation::

        >>> key = client.keys.create(
        ...     name='Key',
        ...     permissions=['DELETE', 'GET', 'POST', 'PUT']
        ... )
        <m2x.keys.Key at 0x365c500>

  - Update (following the previous code)::

        >>> key.update(
        ...     name='Key2',
        ...     permissions=['GET', 'POST', 'PUT']
        ... )

    The parameters ``name`` and ``permissions`` **must** be provided, otherwise
    a validation error is returned by the service (response status code ``422``).

  - Removal (following the previous code)::

        >>> key.remove()

  - Single item retrieval::

        >>> key = client.keys.details(
        ...     '61179472a42583cffc889478010a092a'
        ... )
        <m2x.keys.Key at 0x1652fd0>

    The parameter to ``.details()`` is the Key_ ``key``.

  Feed keys are documented below.


* Feeds

  ``Feeds`` is accessible by the ``feeds`` property in a ``M2XClient`` instance.
  The property is an iterable type where each entry is a Feed_ instance.

  Feeds creation is done when creating a DataSource_, Blueprint_ or Batch_.
  Update and removal is not supported by the cloud API.

  - Iteration::

        >>> for feed in client.feeds
        >>>    ...

  - Single item retrieval::

        >>> feed = client.feeds.details(
        ...     '0e545075fd71aaabf5e85bfb502ea35a'
        ... )
        <m2x.feeds.Feed at 0x1652fd0>

    The parameter to ``.details()`` is the Feed_ ``id``.

  - Feed location

    Location information can be retrieved by doing::

        >>> feed.location
        <m2x.feeds.Location at 0x18f86d0>

    Location can be updated by doing::

        >>> feed.location.update(
        ...     elevation=0,
        ...     longitude=-56.0,
        ...     latitude=-34.0
        ... )
        <m2x.feeds.Location at 0x18f86d0>

    Location removal is not supported.

  - Feed keys

    The keys related to the current feed can be retrieved with::

        >>> feed.keys
        [<m2x.keys.Key at 0x1cbac10>]

    Key methods documented above apply to these keys too.

  - Feed logs

    Get feed logs with::

        >>> feed.logs
        [<m2x.feeds.Log at 0x1bb1d50>, <m2x.feeds.Log at 0x1b94b10>, ...]

    Logs access is just read-only.

  - Feed streams

    Streams are accessible by the ``streams`` property in the Feed_, to get
    them::

        >>> feed.streams
        [<m2x.streams.Stream at 0x2c39a90>, <m2x.streams.Stream at 0x2c39a10>]

    New streams can be created, the only required argument is the stream name::

        >>> stream = feed.streams.create('Stream')
        <m2x.streams.Stream at 0x2c39a90>

    An stream can be removed too::

        >>> stream.remove()

    Or updated::

        >>> stream.update(unit={'label': 'Celsius', 'symbol': 'C'})


* Values

  Given a data stream, values can be inspected and new added easily using the
  ``values`` collection in the stream instance::

      >>> stream.values
      [<m2x.values.Value at 0x2cd8e90>, <m2x.values.Value at 0x2cd8ed0>, ...]

  Each entry is a Value_ instance, the ``at`` attribute contains the date-time
  for the given value, while ``value`` contains the value itself. Entries are
  sorted by ``at`` in ascending order.

  Values cannot be updated or removed at the moment.

  New values can be created in several ways using ``stream.values.add_value()``::

    >>> stream.values.add_value(10)
    <m2x.values.Value at 0x2c39b10>

    >>> now = datetime.now()
    >>> stream.values.add_value(10, now)
    <m2x.values.Value at 0x2c39b10>

  Or ``stream.values.add_values()``::

    >>> now = datetime.now()
    >>> stream.values.add_values(10, (20,), (now, 30), {'value': 40},
    ...                          {'value': 50, 'at': now})
    <m2x.values.Value at 0x2c39b10>


Lets build a RandomNumberGenerator Data Source
----------------------------------------------

Lets build a python random number generator data source using the API
described above.

First import everything::

    >>> import random
    >>> from m2x.client import M2XClient

Create a client instance::

    >>> client = M2XClient(key='288b375565d3402a8b6bd8c343e9fcad')

Now create a batch for the values::

    >>> batch = client.batches.create(
    ...     name='RNG Batch Example',
    ...     description='Batch for RandomNumberGenerator example',
    ...     visibility='public'
    ... )

And add a datasource and grab the related feed::

    >>> datasource = batch.datasources.create(serial='rng')
    >>> feed = datasource.feed

Create a data stream in the feed::

    >>> stream = feed.streams.create(name='example')

And now it's time to register some values in the stream::

    >>> for x in range(10):
    ...    stream.values.add_value(random.randint(0, 100))

Lets add some more values::

    >>> stream.values.add_values(*[random.randint(0, 100) for _ in range(10)])
    [<m2x.values.Value at 0x2cd8a90>, <m2x.values.Value at 0x2cd8ad0>, ...]

Lets print the values::

    >>> for val in stream.values:
    ...    print '{0} - {1}'.format(val.at.strftime('%Y-%m-%d %H:%M:%S'),
    ...                             val.value)


License
=======

This library is released under the MIT license. See ``LICENSE`` for the terms.

.. _M2X API: https://m2x.att.com/developer/documentation/overview
.. _AT&T's M2X service: https://m2x.att.com/
.. _M2X API Documentation: https://m2x.att.com/developer/documentation/overview
.. _requests: http://www.python-requests.org
.. _iso8601: https://pypi.python.org/pypi/iso8601
.. _Client: https://github.com/citrusbyte/m2x-python/blob/master/m2x/client.py#L10
.. _API: https://github.com/citrusbyte/m2x-python/blob/master/m2x/api.py#L9
.. _M2XClient: https://github.com/citrusbyte/m2x-python/blob/master/m2x/client.py#L10
.. _account: https://m2x.att.com/account
.. _Blueprints: https://m2x.att.com/developer/documentation/datasource#List-Blueprints
.. _Blueprint: https://github.com/citrusbyte/m2x-python/blob/master/m2x/blueprints.py#L4
.. _Batches: https://m2x.att.com/developer/documentation/datasource#List-Batches
.. _Batch: https://github.com/citrusbyte/m2x-python/blob/master/m2x/batches.py#L4
.. _DataSources: https://m2x.att.com/developer/documentation/datasource#List-Data-Sources
.. _DataSource: https://github.com/citrusbyte/m2x-python/blob/master/m2x/datasources.py#L4
.. _Feeds: https://m2x.att.com/developer/documentation/feed
.. _Feed: https://github.com/citrusbyte/m2x-python/blob/master/m2x/feeds.py#L21
.. _Keys: https://m2x.att.com/developer/documentation/keys
.. _Key: https://github.com/citrusbyte/m2x-python/blob/master/m2x/keys.py#L4
.. _Collection: https://github.com/citrusbyte/m2x-python/blob/master/m2x/resource.py#L91
.. _Collections: https://github.com/citrusbyte/m2x-python/blob/master/m2x/resource.py#L91
.. _Item: https://github.com/citrusbyte/m2x-python/blob/master/m2x/resource.py#L81
.. _Value: https://github.com/citrusbyte/m2x-python/blob/master/m2x/values.py#L8
