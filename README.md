# TekAn

Technical analysis scratch area

> The toolkit probably doesn't work anymore since Yahoo APIs are no longer a thing (or have changed)

## Getting started

Installing pandas you need to install python3-dev libraries since pandas need to be compiled.

`sudo apt-get install python3-dev`

## MongoDB

In the root of this project, run `docker-compose up -d`

Mongoclient runs on `http://localhost:3000`. When asked to login set the hostname as `mongo`

## Tools & Examples

### Data sourcing

To get some time series data from yahoo, all you need is a symbol and a place to put it. Currently you can save to a csv file
or to mongo.

eg. To save to a running mongo

`python ta.retrieve_yahoo -s SPXS -p mongo`

For other options run

`python ta.retrieve_yahoo -h`

### Workflow Examples

Run simple workflow using mongo source.

`python ta.run_workflow -f examples/sample_workflow_mongo_ds.yml -i SYM.EMA20_OF_MA20`

Run simple workflow using a file source.

`python ta.run_workflow -f examples/sample_workflow_file_ds.yml -i SYM.EMA20_OF_MA20`
