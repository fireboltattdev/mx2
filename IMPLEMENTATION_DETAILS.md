# AT&T's M2X Python Client - Implementation Details

## Library structure

Currently, the client supports `API v1` and `API v2` (defaulting to `v2`) and
all M2X API documents can be found at [M2X API
Documentation](https://m2x.att.com/developer/documentation/v2/overview).


* Client

  In order to communicate with the M2X API you need an instance of `M2XClient`
  – it will provide an interface to all the structures and collections in your
  project. The client will return iterable types representing the main entities
  in M2X, these iterable types are subclasses of Collection.

* API

  The API is just the interface that knowns how to communicate with the
  service by defining the needed API base path (API version related) and
  sending the needed headers. This class is for internal use only.

* Collections

  A Collection is an iterable type containing Item instances, they provide the
  needed interface to get all (or single) items from the service and create new
  ones. Important methods are:

  - Load items (`.load()` method)
  - Get item details (`.get(id)` method)
  - Create items (`.create(**attrs)` method)
  - Search items (`.search(...)` method)

  Attributes required for item creation and update aren't enforced at the
  moment, leaving it open by using `**attrs` allows to support future API
  improvements removing future code updates dependency to support new
  attributes.

  A Collection implements `list` methods needed to simplify data access like
  iteration, index access, slice, etc. `extend` and others are implemented
  too, but they don't have any impact in the server at the moment.

* Item

  An Item is the direct representation of an individual instance in the
  storage service. They provide the needed methods to update an instance and
  remove it. Important methods are:

  - Update item attributes (`.update(**attrs)` method)
  - Remove item from the store (`.remove()` method)

Item and Collection instances have a `data` attribute (`dict` type) which
contains the values returned by the server, this `data` is processed (dates
are converted to native python `datetime` instances). The unprocessed data is
stored in the `raw_data` attribute. To ease attribute access the classes
define `__getattr__` to access any value in the `data` attribute as if they
were instance attributes.


### Collections searching

All Collection subclasses are searchable. The result of calling `.search(...)`
is a list (not a Collection). While searching there are a few common
parameters that can be passed:

* `query`
  A query criteria that usually gets applied to the name attribute.

* `tags`
  Filter by a given tag list, it must be a `list` or `tuple` of strings
  (it's sent joined by `,` to the server).

* `page`
  Pagination page

* `limit`
  Limit the number of items to return

* Collection-related criteria
  Any option related to the collection (check the related API documentation for
  details on supported options).
