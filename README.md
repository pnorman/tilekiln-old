# Tilekiln

## Background

Tilekiln is a set of command-line utilities to generate and serve Mapbox Vector Tiles (MVTs). It generates asynchronously with tilekiln-generate and serves them with tilekiln-serve.

Generation relies on the standard method of a PostgreSQL + PostGIS server as a data source, and ST_AsMVT to serialize the MVTs.

The target use-case is vector tiles for OpenStreetMap Carto on openstreetmap.org, a worldwide complex basemap under high load.

## Install

For local development

```sh
python3 -m venv venv
. venv/bin/activate
pip install --editable .
```

## Requirements

Tilekiln requires a PostGIS database with data loaded to generate vector tiles, saving them to a filesystem or object store [supported by PyFilesystem](https://www.pyfilesystem.org/page/index-of-filesystems/).

[OpenStreetMap Carto's](https://github.com/gravitystorm/openstreetmap-carto/blob/master/INSTALL.md#openstreetmap-data) directions are a good starting place for loading OpenStreetMap data into a PostGIS database.

- PostgreSQL 9.5+
- PostGIS 2.4+, 3.0 is strongly recommended
- Python 3.6+

## Usage

### tilekiln-tilejson

This reads a config file and produces a tilejson file, frequently used in software consuming vector tiles.

### tilekiln-generate

This reads a config file and generates vector tiles, saving them to the object store

#### tilekiln-generate area

```
Usage: tilekiln-generate area [OPTIONS] CONFIG STORAGE

  Generates tiles for an area

Options:
  -d, --dbname TEXT
  -h, --host TEXT
  -p, --port TEXT
  -U, --username TEXT
  -c, --connections INTEGER
  -s, --chunk-size INTEGER
  -z, --min-zoom INTEGER
  -Z, --max-zoom INTEGER
  --help                     Show this message and exit.
```

## Contributing

Test code with ``python setup.py test``.

All code should be formatted according to flake8. Check this with `flake8 tilekiln tests`

## License

This repository is licensed under the ISC license contained in [LICENSE](LICENSE)
