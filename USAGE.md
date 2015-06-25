# AT&T's M2X Python Client - Usage

To create a client instance only a single parameter, the API Key, is needed.
Your API Keys can be found in your account settings. To create a client
instance just do:

```python
>>> from m2x.client import M2XClient
>>> client = M2XClient(key='YOUR API KEY HERE')
```

The client provides an interface to access your Devices (and Catalog),
Distributions and Keys.


## Devices

`Devices` is accessible by the `devices` property in a `M2XClient`
instance. The property is an iterable type where each entry is a Device
instance.

#### Iteration:

```python
>>> for device in client.devices():
>>>    ...
```

#### Creation:

```python
>>> device = client.create_device(
...     name='Devices',
...     description='Device description',
...     visibility='public'
... )
<m2x.v2.devices.Device at 0x365c590>
```

#### Search:

```python
>>> devices = client.devices(q=...)
```

#### Update (following the previous code):

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

#### Removal (following the previous code):

```python
>>> device.remove()
```

#### Single item retrieval:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
```

The parameter to `.get()` is the Device ID.

#### Devices by tags:

```python
>>> client.device_tags()
[{"tag #1": 2}, {"tag #2": 3}]
```

#### Device streams:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> device.streams()
[<m2x.v2.streams.Stream at 0x7f6791d12290>]
```

#### Device location:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> device.location()
<m2x.v2.devices.Location at 0x7f6791d60e50>
```

#### Device triggers:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> device.triggers()
[<m2x.v2.triggers.Trigger at 0x7f6791d4d690>]

>>> trigger = device.triggers()[0]
<m2x.v2.triggers.Trigger at 0x7f6791d4d690>
>>> trigger.test()
```

#### Device updates (post several values to the device in a single request):

```python
>>> from datetime import datetime
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> device.post_updates(values={
    'stream1': [
        {
            'timestamp': datetime.now(),
            'value': 100
        }, {
            'timestamp': datetime.now(),
            'value': 200
        }
    ],
    'stream2': [
        {
            'timestamp': datetime.now(),
            'value': 300
        }, {
            'timestamp': '2015-02-03T00:33:43.422440Z'
            'value': 400
        }
    ]
})
```

## Catalog

The catalog is just a list of public devices accessible to everybody. To
access it, just use the `catalog` property:

```python
>>> for device in client.device_catalog():
>>>    ...
```

## Keys

`Keys` is accessible by the `keys` property in a `M2XClient` instance.
The property is an iterable type where each entry is a Key instance.

#### Iteration:

```python
>>> for key in client.keys():
>>>    ...
```

#### Creation:

```python
>>> key = client.create_key(
...     name='Key',
...     permissions=['DELETE', 'GET', 'POST', 'PUT']
... )
<m2x.v2.keys.Key at 0x365c500>
```

#### Search:

Keys don't support searching, but the method is left implemented in
case it's supported in the future. Calling search will return all the keys.

#### Update (following the previous code):

```python
>>> key.update(
...     name='Key2',
...     permissions=['GET', 'POST', 'PUT']
... )
```

The parameters `name` and `permissions` **must** be provided, otherwise
a validation error is returned by the service (response status code `422`).

#### Removal (following the previous code):

```python
>>> key.remove()
```

## Streams

`Streams` can be seen as collection of values, M2X provides some useful
methods for streams.

#### Iteration:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> for stream in device.streams():
        ...
```

#### Values:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> stream = device.streams()[0]
<m2x.v2.streams.Stream at 0x7f6791d12290>
>>> stream.values()
[<m2x.v2.values.Value at 0x7f6791d123d0>, <m2x.v2.values.Value at 0x7f6791250890>, ...]
# Add a value without timestamp (server will set current date as timestamp)
>>> stream.add_value(1234)
# Add a with timestamp
>>> stream.add_value(1234, datetime.datetime.now())
# Post several values
>>> stream.post_values([
    {'timestamp': datetime.datetime.now(), 'value': 100},
    {'timestamp': datetime.datetime.now(), 'value': 200}
])
```

#### Sampling:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> stream = device.streams[0]
<m2x.v2.streams.Stream at 0x7f6791d12290>
>>> stream.sampling(interval=1)
[<m2x.v2.values.Value at 0x7f6791d123d0>, <m2x.v2.values.Value at 0x7f6791250890>, ...]
```

#### Stats:

```python
>>> device = client.device('188a0afb3adc379706e780a4eafbd153')
<m2x.v2.devices.Device at 0x1652fd0>
>>> stream = device.stream()[0]
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


## Distributions

`Distributions` are accessible by the `distributions` property in
a `M2XClient` instance. The property is an iterable type where each entry
is a Distribution instance.

#### Iteration:

```python
>>> for distribution in client.distributions():
>>>    ...
```

#### Creation:

```python
>>> device = client.create_distribution(
...     name='Distribution',
...     description='Distribution description',
...     visibility='public'
... )
<m2x.v2.distributions.Distribution at 0x365c590>
```

#### Search:

```python
>>> distributions = client.distributions(q=...)
```

#### Update (following the previous code):

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

#### Removal (following the previous code):

```python
>>> distribution.remove()
```

#### Devices (following previous code):

```python
>>> distribution.devices()
[<m2x.v2.devices.Device at 0x7f6791d60f90>, <m2x.v2.devices.Device at 0x7f6791d60410>]
```

## Time

For devices that do not have a Real Time Clock, M2X provides a set of endpoints
that returns the server' times.

```
>>> client.time()
{u'iso8601': u'2015-06-25T21:06:54.841Z',
 u'millis': 1435266414841,
 u'seconds': 1435266414}
>>> client.time_seconds()
1435266437
>>> client.time_millis()
1435266445736
>>> client.time_iso8601()
'2015-06-25T21:07:31.328Z'
```

## Lets build a V2 RandomNumberGenerator Data Source

Lets build a python random number generator data source using the API
described above.

```python
# First import everything:
import random
from m2x.client import M2XClient

# Create a client instance:
client = M2XClient(key='288b375565d3402a8b6bd8c343e9fcad')

# Now create a device for the values:
device = client.create_device(
    name='RNG Device Example',
    description='Device for RandomNumberGenerator example',
    visibility='public'
)

# Create a data stream in the feed:
stream = device.create_stream(name='values')

# And now it's time to register some values in the stream:
for x in range(10):
    stream.add_value(random.randint(0, 100))

# Lets print the values:
for val in stream.values():
    print '{0} - {1}'.format(val.at.strftime('%Y-%m-%d %H:%M:%S'),
                             val.value)
```
