Python M2X API Client
=====================

`M2X API`_ provides all the needed operations to connect your devices to `AT&T
M2X storage service`_. This application provides an easy to use interface for
your favorite language, Python.

The library provides an easy to use interface to navigate and register your
devices values into `AT&T M2X storage service`_, while supporting Python 2 and
3.

Dependencies list is really small:

* requests_ (version ``2.0.0``)
* six_ (version ``1.4.1``)


Installation
------------

The project is really easy to install, the different options are::

    $ pip install m2x

or::

    $ easy_install m2x

or cloning the repository::

    $ git clone https://github.com/attm2x/m2x-python.git
    $ cd m2x-python
    $ python setup.py install


Library structure
-----------------

Right not the client supports ``API v1``, all the API documents can be found at
`M2X API Documentation`_.

* Client_

  In order to communicate with the API you need an instance of `M2XClient`_, it
  will provide an interface to all the structures and collections of your
  project. The client will return iterable types representing the main entities
  in M2X, these iterable types are subclasses of Collection_.

* API_

  The API_ is just the interface that knowns how communicate with the service
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
  the storage service, at least not right now, don't rely on them except for
  data access (iteration, index access, slice, etc.).

* Item_

  An Item_ is the directly representation of an individual instance in the
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

To create a client instance just a parameter is needed, the API Key, that can
be found on your account_ section, or your feed API key available in your Feed
details. To create a client instance just do::

    >>> from m2x.client import M2XClient
    >>> client = M2XClient(key='your api key here')

The client provides an interface to access your Blueprints_, Batches_,
DataSources_, Feeds_, Keys_.

* Blueprints

  Blueprints is accessible by the ``blueprints`` property in a ``M2XClient``
  instance. The property is an iterable type where each entry is a Blueprint_
  instance.

  - Iteration::

        >>> for blueprint in client.blueprints:
        >>>    ...

  - Creation:

```python
        >>> blueprint = client.blueprints.create(
        ...     name='Blueprint',
        ...     description='Blueprint description',
        ...     visibility='public'
        ... )
        <m2x.blueprints.Blueprint at 0x365c590>
```

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


* Batches

  Batches is accessible by the ``batches`` property in a ``M2XClient``
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


* DataSources

  **TODO**


* Feeds

  **TODO**


* Keys

  **TODO**


.. _M2X API: https://m2x.att.com/developer/documentation/overview
.. _AT&T M2X storage service: https://m2x.att.com/
.. _M2X API Documentation: https://m2x.att.com/developer/documentation/overview
.. _requests: http://www.python-requests.org
.. _six: https://bitbucket.org/gutworth/six
.. _Client: https://github.com/attm2x/m2x-python/blob/master/m2x/client.py#L10
.. _API: https://github.com/attm2x/m2x-python/blob/master/m2x/api.py#L9
.. _M2XClient: https://github.com/attm2x/m2x-python/blob/master/m2x/client.py#L10
.. _account: https://m2x.att.com/account
.. _Blueprints: https://m2x.att.com/developer/documentation/datasource#List-Blueprints
.. _Blueprint: https://github.com/attm2x/m2x-python/blob/master/m2x/blueprints.py#L4
.. _Batches: https://m2x.att.com/developer/documentation/datasource#List-Batches
.. _Batch: https://github.com/attm2x/m2x-python/blob/master/m2x/batches.py#L4
.. _DataSources: https://m2x.att.com/developer/documentation/datasource#List-Data-Sources
.. _Feeds: https://m2x.att.com/developer/documentation/feed
.. _Keys: https://m2x.att.com/developer/documentation/keys
.. _Collection: https://github.com/attm2x/m2x-python/blob/master/m2x/resource.py#L91
.. _Collections: https://github.com/attm2x/m2x-python/blob/master/m2x/resource.py#L91
.. _Item: https://github.com/attm2x/m2x-python/blob/master/m2x/resource.py#L81
