# AT&T's M2X Python Client - Usage

## V2 Client usage

To create a client instance only a single parameter, the API Key, is needed.
Your API Keys can be found in your account settings. To create a client
instance just do:

```python
>>> from m2x.client import M2XClient
>>> client = M2XClient(key='your api key here')
```

The client provides an interface to access your Devices (and Catalog),
Distributions and Keys.

* Devices

  `Devices` is accessible by the `devices` property in a `M2XClient`
  instance. The property is an iterable type where each entry is a Device
  instance.

  - Iteration:

    ```python
    >>> for device in client.devices:
    >>>    ...
    ```

  - Creation:

    ```python
    >>> device = client.devices.create(
    ...     name='Devices',
    ...     description='Device description',
    ...     visibility='public'
    ... )
    <m2x.v2.devices.Device at 0x365c590>
    ```

  - Search:

    ```python
    >>> devices = client.devices.search(...)
    ```

  - Update (following the previous code):

    ```python
    >>> device.update(
    ...     name='Device2',
    ...     description='Device2 description',
    ...     visibility='private',
    ...     status='enabled'
    ... )
    ```

    The parameters `name`, `visibility` **must** be provided, otherwise
    a validation error is returned by the service (response status code
    `422`).

  - Removal (following the previous code):

    ```python
    >>> device.remove()
    ```

  - Single item retrieval:

    ```python
    >>> device = client.devices.get(
    ...     '188a0afb3adc379706e780a4eafbd153'
    ... )
    <m2x.v2.devices.Device at 0x1652fd0>
    ```

    The parameter to `.get()` is the Device ID.

  - Devices groups:

    ```python
    >>> client.devices.groups()
    {"groups": [{"group #1": 2}, {"group #2": 3}]}
    ```

  - Device streams:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> device.streams
    [<m2x.v2.streams.Stream at 0x7f6791d12290>]
    ```

  - Device location:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> device.location
    <m2x.v2.devices.Location at 0x7f6791d60e50>
    ```

  - Device triggers:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> device.triggers
    [<m2x.v2.triggers.Trigger at 0x7f6791d4d690>]

    >>> trigger = device.triggers[0]
    <m2x.v2.triggers.Trigger at 0x7f6791d4d690>
    >>> trigger.test()
    ```

  - Device updates (post several values to the device in a single request):

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> device.updates({'stream1': [value1, value2]})
    ```

* Catalog

  The catalog is just a list of public devices accessible to everybody. To
  access it, just use the `catalog` property:

    ```python
    >>> for device in client.catalog:
    >>>    ...
    ```

* Keys

  `Keys` is accessible by the `keys` property in a `M2XClient` instance.
  The property is an iterable type where each entry is a Key instance.

  - Iteration:

    ```python
    >>> for key in client.keys
    >>>    ...
    ```

  - Creation:

    ```python
    >>> key = client.keys.create(
    ...     name='Key',
    ...     permissions=['DELETE', 'GET', 'POST', 'PUT']
    ... )
    <m2x.v2.keys.Key at 0x365c500>
    ```

  - Search:

    Keys don't support searching, but the method is left implemented in
    case it's supported in the future. Calling search will return all the keys.

  - Update (following the previous code):

    ```python
    >>> key.update(
    ...     name='Key2',
    ...     permissions=['GET', 'POST', 'PUT']
    ... )
    ```

    The parameters `name` and `permissions` **must** be provided, otherwise
    a validation error is returned by the service (response status code `422`).

  - Removal (following the previous code):

    ```python
    >>> key.remove()
    ```

  - Single item retrieval:

    ```python
    >>> key = client.keys.details(
    ...     '61179472a42583cffc889478010a092a'
    ... )
    <m2x.v2.keys.Key at 0x1652fd0>
    ```

    The parameter to `.details()` is the Key `key`.

  Feed keys are documented below.


* Streams

  `Streams` can be seen as collection of values, M2X provides some useful
  methods for streams.

  - Iteration:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> for stream in device.streams:
            ...
    ```

  - Values:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> stream = device.streams[0]
    <m2x.v2.streams.Stream at 0x7f6791d12290>
    >>> stream.values
    [<m2x.v2.values.Value at 0x7f6791d123d0>, <m2x.v2.values.Value at 0x7f6791250890>, ...]
    ```

  - Sampling:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> stream = device.streams[0]
    <m2x.v2.streams.Stream at 0x7f6791d12290>
    >>> stream.sampling
    [<m2x.v2.values.Value at 0x7f6791d123d0>, <m2x.v2.values.Value at 0x7f6791250890>, ...]
    ```

  - Stats:

    ```python
    >>> device = client.devices.get('188a0afb3adc379706e780a4eafbd153')
    <m2x.v2.devices.Device at 0x1652fd0>
    >>> stream = device.streams[0]
    <m2x.v2.streams.Stream at 0x7f6791d12290>
    >>> stream.stats()
    {
        u'end': u'2015-01-01T22:44:37.890Z',
        u'stats': {
            u'avg': u'0.40545455E2',
            u'count': 11.0,
            u'max': 82.0,
            u'min': 8.0,
            u'stddev': 21.266122
        }
    }
    ```


* Distributions

  `Distributions` are accessible by the `distributions` property in
  a `M2XClient` instance. The property is an iterable type where each entry
  is a Distribution instance.

  - Iteration:

    ```python
    >>> for distribution in client.distributions:
    >>>    ...
    ```

  - Creation:

    ```python
    >>> device = client.distributions.create(
    ...     name='Distribution',
    ...     description='Distribution description',
    ...     visibility='public'
    ... )
    <m2x.v2.distributions.Distribution at 0x365c590>
    ```

  - Search:

    ```python
    >>> distributions = client.distributions.search(...)
    ```

  - Update (following the previous code):

    ```python
    >>> distribution.update(
    ...     name='Distribution2',
    ...     description='Distribution2 description',
    ...     visibility='private'
    ... )
    ```

    The parameters `name`, `visibility` **must** be provided, otherwise
    a validation error is returned by the service (response status code
    `422`).

  - Removal (following the previous code):

    ```python
    >>> distribution.remove()
    ```

  - Single item retrieval:

    ```python
    >>> distribution = client.distributions.get(
    ...     '188a0afb3adc379706e780a4eafbd153'
    ... )
    <m2x.v2.distributions.Distribution at 0x1652fd0>
    ```

    The parameter to `.get()` is the Distribution ID.

  - Devices (following previous code):

    ```python
    >>> distribution.devices
    [<m2x.v2.devices.Device at 0x7f6791d60f90>, <m2x.v2.devices.Device at 0x7f6791d60410>]
    ```

  - Strems (following previous code):

    ```python
    >>> distribution.streams
    [<m2x.v2.streams.Stream at 0x7f6791d12290>]
    ```

  - Triggers (following previous code):

    ```python
    >>> distribution.triggers
    [<m2x.v2.triggers.Trigger at 0x7f6791d4d690>]
    ```

### Lets build a V2 RandomNumberGenerator Data Source

Lets build a python random number generator data source using the API
described above.

```python
# First import everything:
import random
from m2x.client import M2XClient

# Create a client instance:
client = M2XClient(key='288b375565d3402a8b6bd8c343e9fcad')

# Now create a device for the values:
device = client.devices.create(
    name='RNG Device Example',
    description='Device for RandomNumberGenerator example',
    visibility='public'
)

# Create a data stream in the feed:
stream = device.streams.create(name='values')

# And now it's time to register some values in the stream:
for x in range(10):
    stream.values.add_value(random.randint(0, 100))

# Lets add some more values:
stream.values.add_values(*[random.randint(0, 100) for _ in range(10)])

# Lest add even more values:
device.updates({
    'values': [{'value': random.randint(0, 100)} for _ in range(10)]
})

# Lets print the values:
for val in stream.values:
    print '{0} - {1}'.format(val.at.strftime('%Y-%m-%d %H:%M:%S'),
                             val.value)
```


## V1 Client usage (deprecated)

To create a v1 client instance, two parameters are needed, the API Key and the
API V1 implementation interface. Your Master API Key can be found in your
account settings, or a feed API key is available in your Data Source details
screen. To create a client instance just do:

```python
>>> from m2x.client import M2XClient
>>> from m2x.v1.api import APIVersion1
>>> client = M2XClient(key='your api key here', api=APIVersion1)
```

The client provides an interface to access your Blueprints, Batches,
DataSources, Feeds, Keys.

* Blueprints

  `Blueprints` is accessible by the `blueprints` property in a `M2XClient`
  instance. The property is an iterable type where each entry is a Blueprint
  instance.

  - Iteration:

    ```python
    >>> for blueprint in client.blueprints:
    >>>    ...
    ```

  - Creation:

    ```python
    >>> blueprint = client.blueprints.create(
    ...     name='Blueprint',
    ...     description='Blueprint description',
    ...     visibility='public'
    ... )
    <m2x.blueprints.Blueprint at 0x365c590>
    ```

  - Search:

    ```python
    >>> blueprints = client.blueprints.search(...)
    ```

  - Update (following the previous code):

    ```python
    >>> blueprint.update(
    ...     name='Blueprint2',
    ...     description='Blueprint2 description',
    ...     visibility='private',
    ...     status='enabled'
    ... )
    ```

    The parameters `name`, `description` and `visibility` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code `422`).

  - Removal (following the previous code):

    ```python
    >>> blueprint.remove()
    ```

  - Single item retrieval:

    ```python
    >>> blueprint = client.blueprints.details(
    ...     '188a0afb3adc379706e780a4eafbd153'
    ... )
    <m2x.blueprints.Blueprint at 0x1652fd0>
    ```

    The parameter to `.details()` is the Blueprint ID.

  - Related Feed

    A Blueprint has a related feed created automatically, to get the feed
    access the `feed` property:

    ```python
    >>> related_feed = blueprint.feed
    <m2x.feeds.Feed at 0x1652fd0>
    ```

* Batches

  `Batches` is accessible by the `batches` property in a `M2XClient`
  instance. The property is an iterable type where each entry is a Batch
  instance.

  - Iteration:

    ```python
    >>> for batch in client.batches:
    >>>    ...
    ```

  - Creation:

    ```python
    >>> batch = client.batches.create(
    ...     name='Batch',
    ...     description='Batch description',
    ...     visibility='public',
    ... )
    <m2x.batches.Batch at 0x365c500>
    ```

  - Search:

    ```python
    >>> batches = client.batches.search(...)
    ```

  - Update (following the previous code):

    ```python
    >>> batch.update(
    ...     name='Batch2',
    ...     description='Batch2 description',
    ...     visibility='private',
    ...     status='enabled'
    ... )
    ```

    The parameters `name`, `description` and `visibility` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code `422`).

  - Removal (following the previous code):

    ```python
    >>> batch.remove()
    ```

  - Single item retrieval:

    ```python
    >>> batch = client.batches.details(
    ...     '7cc8f518983dd62254b98d976400a3d4'
    ... )
    <m2x.batches.Batch at 0x1652fd0>
    ```

    The parameter to `.details()` is the Batch ID.

  - To access all the datasources in this Batch use the `datasources`
    property which also provides the needed method to create new DataSource:

    ```python
    >>> batch.datasources
    [<m2x.datasources.DataSource at 0x2674b10>]
    >>> batch.datasources.create(serial='abc123')
    [<m2x.datasources.DataSource at 0x2674b10>, <m2x.datasources.DataSource at 0x2674d50>]
    ```

  - Related Feed

    A Batch has a related feed created automatically, to get the feed access
    the `feed` property:

    ```python
    >>> related_feed = batch.feed
    <m2x.feeds.Feed at 0x1652fd0>
    ```

* DataSources

  `DataSources` is accessible by the `datasources` property in a
  `M2XClient` instance. The property is an iterable type where each entry is
  a DataSource instance.

  - Iteration:

    ```python
    >>> for datasource in client.datasources:
    >>>    ...
    ```

  - Creation:

    ```python
    >>> datasource = client.datasources.create(
    ...     name='Datasource',
    ...     description='Datasource description',
    ...     visibility='public',
    ... )
    <m2x.datasources.DataSource at 0x365c500>
    ```

  - Search:

    ```python
    >>> datasources = client.datasources.search(...)
    ```

  - Update (following the previous code):

    ```python
    >>> datasource.update(
    ...     name='Datasource2',
    ...     description='Datasource2 description',
    ...     visibility='private',
    ...     status='enabled'
    ... )
    ```

    The parameters `name`, `description` and `visibility` **must** be
    provided, otherwise a validation error is returned by the service (response
    status code `422`).

  - Removal (following the previous code):

    ```python
    >>> datasource.remove()
    ```

  - Single item retrieval:

    ```python
    >>> datasource = client.datasources.details(
    ...     '61179472a42583cffc889478010a092a'
    ... )
    <m2x.datasources.DataSource at 0x1652fd0>
    ```

    The parameter to `.details()` is the DataSource ID.

  - Related Feed

    A DataSource has a related feed created automatically, to get the feed
    access the `feed` property:

    ```python
    >>> related_feed = datasource.feed
    <m2x.feeds.Feed at 0x1652fd0>
    ```

* Keys

  `Keys` is accessible by the `keys` property in a `M2XClient` instance.
  The property is an iterable type where each entry is a Key instance.

  - Iteration:

    ```python
    >>> for key in client.keys
    >>>    ...
    ```

  - Creation:

    ```python
    >>> key = client.keys.create(
    ...     name='Key',
    ...     permissions=['DELETE', 'GET', 'POST', 'PUT']
    ... )
    <m2x.keys.Key at 0x365c500>
    ```

  - Search:

    Keys don't support searching, but the method is left implemented in
    case it's supported in the future. Calling search will return all the keys.

  - Update (following the previous code):

    ```python
    >>> key.update(
    ...     name='Key2',
    ...     permissions=['GET', 'POST', 'PUT']
    ... )
    ```

    The parameters `name` and `permissions` **must** be provided, otherwise
    a validation error is returned by the service (response status code `422`).

  - Removal (following the previous code):

    ```python
    >>> key.remove()
    ```

  - Single item retrieval:

    ```python
    >>> key = client.keys.details(
    ...     '61179472a42583cffc889478010a092a'
    ... )
    <m2x.keys.Key at 0x1652fd0>
    ```

    The parameter to `.details()` is the Key `key`.

  Feed keys are documented below.


* Feeds

  `Feeds` is accessible by the `feeds` property in a `M2XClient` instance.
  The property is an iterable type where each entry is a Feed instance.

  Feeds creation is done when creating a DataSource, Blueprint or Batch.
  Update and removal is not supported by the cloud API.

  - Iteration:

    ```python
    >>> for feed in client.feeds
    >>>    ...
    ```

  - Single item retrieval:

    ```python
    >>> feed = client.feeds.details(
    ...     '0e545075fd71aaabf5e85bfb502ea35a'
    ... )
    <m2x.feeds.Feed at 0x1652fd0>
    ```

    The parameter to `.details()` is the Feed `id`.

  - Search:

    ```python
    >>> feeds = client.feeds.search(...)
    ```

    Feeds can be filtered by `type` by doing:

    ```python
    >>> feeds = client.feeds.search(type='blueprint')
    ```

    The available options are `blueprint`, `batch` and `datasource`.

    It's also possible to filter by `latitude`, `longitude`, `distance`
    specified in `distance_unit` (either `mi`, `miles` or `km`).

  - Feed location

    Location information can be retrieved by doing:

    ```python
    >>> feed.location
    <m2x.feeds.Location at 0x18f86d0>
    ```

    Location can be updated by doing:

    ```python
    >>> feed.location.update(
    ...     elevation=0,
    ...     longitude=-56.0,
    ...     latitude=-34.0
    ... )
    <m2x.feeds.Location at 0x18f86d0>
    ```

    Location removal is not supported.

  - Feed keys

    The keys related to the current feed can be retrieved with:

    ```python
    >>> feed.keys
    [<m2x.keys.Key at 0x1cbac10>]
    ```

    Key methods documented above apply to these keys too.

  - Feed logs

    Get feed logs with:

    ```python
    >>> feed.logs
    [<m2x.feeds.Log at 0x1bb1d50>, <m2x.feeds.Log at 0x1b94b10>, ...]
    ```

    Logs access is just read-only.

  - Feed streams

    Streams are accessible by the `streams` property in the Feed, to get
    them:

    ```python
    >>> feed.streams
    [<m2x.streams.Stream at 0x2c39a90>, <m2x.streams.Stream at 0x2c39a10>]
    ```

    New streams can be created, the only required argument is the stream name:

    ```python
    >>> stream = feed.streams.create('Stream')
    <m2x.streams.Stream at 0x2c39a90>
    ```

    An stream can be removed too:

    ```python
    >>> stream.remove()
    ```

    Or updated:

    ```python
    >>> stream.update(unit={'label': 'Celsius', 'symbol': 'C'})
    ```

  - Feed values

    It's possible to register a multiple values in multiple streams directly
    from the feed:

    ```python
    >>> feed.streams.create('foo')
    >>> feed.streams.create('bar')
    >>> feed.add_values({'foo': [{'value': 10}, {'value': 20}],
                         'bar': [{'value': 100}, {'value': 200}]})
    ```

    As the example shows, the parameter needed is a `dict` where the keys are
    the stream names and the values are the desired values to store in M2X. The
    values list can follow the same syntax defined below in
    `stream.values.add_values()`.

* Values

  Given a data stream, values can be inspected and new added easily using the
  `values` collection in the stream instance:

  ```python
  >>> stream.values
  [<m2x.values.Value at 0x2cd8e90>, <m2x.values.Value at 0x2cd8ed0>, ...]
  ```

  Each entry is a Value instance, the `at` attribute contains the date-time
  for the given value, while `value` contains the value itself. Entries are
  sorted by `at` in ascending order.

  Values cannot be updated or removed at the moment.

  New values can be created in several ways using `stream.values.add_value()`:

  ```python
  >>> stream.values.add_value(10)
  <m2x.values.Value at 0x2c39b10>

  >>> now = datetime.datetime.now()
  >>> stream.values.add_value(10, now)
  <m2x.values.Value at 0x2c39b10>
  ```

  Or `stream.values.add_values()`:

  ```python
  >>> now = datetime.datetime.now()
  >>> stream.values.add_values(10, (20,), (now, 30), {'value': 40},
  ...                          {'value': 50, 'at': now})
  <m2x.values.Value at 0x2c39b10>
  ```

  Also searched by date, but there's a helper for that already:

  ```python
  >>> stream.values.by_date(start=..., end=..., limit=...)
  ```

  All parameters are optional. `start` and `end` must be a `date` or
  `datetime` instance (any string format supported by iso8601 module also
  work). `limit` must be an `int` and it will limit the result count to
  that value.


### Lets build a V1 RandomNumberGenerator Data Source

Lets build a python random number generator data source using the API described
above.

```python
# First import everything
import random
from m2x.client import M2XClient

# Create a client instance:
client = M2XClient(key='288b375565d3402a8b6bd8c343e9fcad')

# Now create a batch for the values:
batch = client.batches.create(
    name='RNG Batch Example',
    description='Batch for RandomNumberGenerator example',
    visibility='public'
)

# And add a datasource and grab the related feed:
datasource = batch.datasources.create(serial='rng')
feed = datasource.feed

# Create a data stream in the feed:
stream = feed.streams.create(name='example')

# And now it's time to register some values in the stream:
for x in range(10):
    stream.values.add_value(random.randint(0, 100))

# Lets add some more values:
stream.values.add_values(*[random.randint(0, 100) for _ in range(10)])

# Lest add even more values:
feed.add_values({
    'example': [random.randint(0, 100) for _ in range(10)]
})

# Lets print the values:
for val in stream.values:
    print '{0} - {1}'.format(val.at.strftime('%Y-%m-%d %H:%M:%S'),
                             val.value)
```
