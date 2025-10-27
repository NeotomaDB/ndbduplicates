[![NSF-2410961](https://img.shields.io/badge/NSF-2410961-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=2410961)

# ndbdup - The Neotoma Duplicate Manager

A set of commandline tools used to manage duplicate records in Neotoma. The tools help to:

1. Visualize duplicate records, see what values are duplicated and how they differ from one another.
2. See the extent of PK-FK links for a particular table. Which tables might be affected by changes to an PK value.
3. Update or merge values among entries with duplicated values.
4. Delete and update FKs throughout the database.

Because data is entered by data stewards, there are times when we need to clean or correct these entries. This can be challenging if each of the duplicated entries is used elsewhere within the database. This tool is intended to help database management by bringing a number of these resources together in one place.

## Development

* [Simon Goring](http://goring.org): University of Wisconsin - Madison [![orcid](https://img.shields.io/badge/orcid-0000--0002--2700--4605-brightgreen.svg)](https://orcid.org/0000-0002-2700-4605)

## Using this Repository

### Installing the Needed Packages

This project uses the `uv` package manager. In the root directory you will find a `pyptoject.toml` file that indicates all the required packages for installation. After cloning the repository to your local system, use `uv install` to install all required packages.

### Connecting to Neotoma

The repository includes an `.env-template` file to use as an example, but requires a `.env` file in the project root. That file should include connection strings for the Neotoma database, either the remote server (if you have permissions) or a local snapshot of the database.

### Using the Tools

#### Visualizing Duplicate Records

Often the first step is assessing why records are duplicates. In this case we can execute:

```bash
uv run ndbdup.py show_rows -t taxa -s ndb -c taxonname -q Cadmium
```

This will show us all rows with the value `Cadmium` in the `taxonname` column of the `ndb.taxa` table:

```bash
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ taxonid ┃ taxoncode ┃ taxonname ┃ author ┃ valid ┃ highertaxonid ┃ extinct ┃ taxagroupid ┃ publicationid ┃ validatorid ┃ validatedate ┃ notes ┃ recdatecreated      ┃ recdatemodified     ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 27926   │ Cd        │ Cadmium   │ None   │ True  │ 21260         │ False   │ WCH         │ None          │ 7126        │ 2016-08-10   │ None  │ 2016-08-10 20:43:05 │ 2016-08-10 20:43:05 │
│ 41878   │ Cd        │ Cadmium   │ None   │ True  │ 23801         │ False   │ CHM         │ 12788         │ 8713        │ 2020-06-17   │ None  │ 2020-06-17 13:34:05 │ 2020-06-17 13:34:05 │
└─────────┴───────────┴───────────┴────────┴───────┴───────────────┴─────────┴─────────────┴───────────────┴─────────────┴──────────────┴───────┴─────────────────────┴─────────────────────┘
```

Here it is possible to see that Cadmium has been entered into the database twice, once as part of the *Water Chemistry* taxon group and once as part of the *Chemical* taxon group. We might presume that these are the same elements, and wish to understand further how they are used within the database.

#### Visualizing Foreign Key Relationships

To see which tables may be impacted by any changes we make to the primary key by deleting or altering a record, we can visualize how the primary key is used across tables in the database.

```bash
uv run ndbdup.py show_keys -t taxa -s ndb
```

This will show us all tables (and columns) that have a PK-FK relationship to the table `taxa`.

```bash
** Checking the use of "taxas" Primary Key **
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Related Schema ┃ Related Table     ┃ Related Column ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ ndb            │ datasettaxonnotes │ taxonid        │
│ ndb            │ ecolgroups        │ taxonid        │
│ ndb            │ externaltaxa      │ taxonid        │
│ ndb            │ formtaxa          │ affinityid     │
│ ndb            │ formtaxa          │ taxonid        │
│ ndb            │ isostratdata      │ taxonid        │
│ ndb            │ samples           │ taxonid        │
│ ndb            │ specimendates     │ taxonid        │
│ ndb            │ synonyms          │ invalidtaxonid │
│ ndb            │ synonyms          │ validtaxonid   │
│ ndb            │ synonymy          │ reftaxonid     │
│ ndb            │ synonymy          │ taxonid        │
│ ndb            │ taxa              │ highertaxonid  │
│ ndb            │ taxaalthierarchy  │ highertaxonid  │
│ ndb            │ taxaalthierarchy  │ taxonid        │
│ ndb            │ taxonpaths        │ taxonid        │
│ ndb            │ variables         │ taxonid        │
└────────────────┴───────────────────┴────────────────┘
```

#### Understanding Row Use

Once we know which rows we are targeting, and which tables may be impacted, we can look at the counts of those PK identifiers in the related tables.

```bash
uv run ndbdup.py show_counts -t taxa -s ndb -c taxonid -r 27926,41878
```

This will then run a query on each table for which the `taxonid` has a PK-FK relationship and show how many times that value appears in those related tables.

```bash
** Checking the use of the duplicate row pair 27926,41878 **
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ Related Schema ┃ Related Table     ┃ Related Column ┃ Row Value ┃ Count ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ ndb            │ datasettaxonnotes │ taxonid        │ 27926     │ 25    │
│ ndb            │ datasettaxonnotes │ taxonid        │ 41878     │ 0     │
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
│ ndb            │ ecolgroups        │ taxonid        │ 27926     │ 1     │
│ ndb            │ ecolgroups        │ taxonid        │ 41878     │ 1     │
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
│ ndb            │ externaltaxa      │ taxonid        │ 27926     │ 0     │
│ ndb            │ externaltaxa      │ taxonid        │ 41878     │ 0     │
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
...                                                                     ...
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
│ ndb            │ taxaalthierarchy  │ taxonid        │ 27926     │ 0     │
│ ndb            │ taxaalthierarchy  │ taxonid        │ 41878     │ 0     │
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
│ ndb            │ taxonpaths        │ taxonid        │ 27926     │ 0     │
│ ndb            │ taxonpaths        │ taxonid        │ 41878     │ 0     │
├────────────────┼───────────────────┼────────────────┼───────────┼───────┤
│ ndb            │ variables         │ taxonid        │ 27926     │ 1     │
│ ndb            │ variables         │ taxonid        │ 41878     │ 4     │
└────────────────┴───────────────────┴────────────────┴───────────┴───────┘
```

This lets us see that there are clearly cases where the Cadmium is identified, particularly in the `ndb.datasettaxonnotes` table for `taxonid` 27926. Each Cadmium is used in the `ndb.variables` table, so we need to check these rows to see what is actually happening.

#### Updating Duplicate Rows

In the case where you have duplicate rows and want to assign all foreign keys to one specific PK value throughout the database, we would use the `keep_id` option:

```bash
uv run ndbdup.py keep_id -t taxa -s ndb -r 1234,1235 -k 1234
```

In this case across all tables we would be looking for any table that refers to the PK 1234 and 1235 in the taxon table, and we would change every instance of `1235` with `1234` (the PK to `keep`).

## Contribution

We welcome user contributions to this project.  All contributors are expected to follow the [code of conduct](https://github.com/Neotomadb/api_nodetest/blob/master/code_of_conduct.md).  Contributors should fork this project and make a pull request indicating the nature of the changes and the intended utility.  Further information for this workflow can be found on the GitHub [Pull Request Tutorial webpage](https://help.github.com/articles/about-pull-requests/).

## Funding

This work is funded by NSF grants to Neotoma: NSF Geoinformatics -[2410961](https://nsf.gov/awardsearch/showAward?AWD_ID=2410961)
