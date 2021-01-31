# GAA API

A public & RESTful API which delivers GAA data, populated in a crowd-sourced manner.

## Endpoints

#### Healthcheck

```
GET /api/v1/healthcheck
```

```
{
    "status": "ok"
}
```

#### Services

1) The endpoint hit by the SFTP Service (using the standard external web service job):

```
POST /api/v1/match

{
    "homeTeam": 01204,
    "awayTeam": ...
}
```

```
{
    "status": "success"
}
```

## Running

Ensure you have the relevant credentials for the Database connections.

Clone the repo, open `src/config/base_config.json` to adjust the configuration.
Alternatively, set the `ENVIRONMENT` variable to choose the configuration, and run:

```
make run-dev
```
or inside the container
```
... make run
```

## Testing

This project includes testing at all layers.

### Unit

Unit tests are implemented for all public functions in the `src` module.


### Running Tests

To run the unit tests locally, run
```
make test-dev
```
or to run inside the container:
```
make build test
```

