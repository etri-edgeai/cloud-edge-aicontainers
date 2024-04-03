# Demo project to display RedisTimeSeries data on the Worldmap in Grafana

<div id="badges" align="center">

[![Grafana 7](https://img.shields.io/badge/Grafana-7-blue)](https://www.grafana.com)
[![RedisTimeSeries](https://img.shields.io/badge/RedisTimeSeries-inspired-yellowgreen)](https://oss.redislabs.com/redistimeseries/)
[![Grafana-Redis-Datasource plugin](https://img.shields.io/badge/GrafanaRedisDatasource-powered-red)](https://github.com/RedisTimeSeries/grafana-redis-datasource)

</div>


## Introduction

Redis Coronavirus map demo is an example of the integration of [RedisTimeSeries](https://oss.redislabs.com/redistimeseries/) and Grafana Worldmap Panel using [Redis Data Source](https://github.com/RedisTimeSeries/grafana-redis-datasource). Redis Data Source plug-in is not officially supported by Grafana Worldmap, but there's a little workaround how to do it. 

For this demo we are using United States coronavirus statistics from [Coronavirus API](http://coronavirusapi.com/) website.
 
Besides standard graph representation, data are also drawn on the map. After you configure the Datasource and specify the query, you need to do the following: 

1. Apply the Transformation “Labels to fields” to TimeSeries output result.
2. Change the map parameter “Location Data” to table mode and map the relevant fields accordingly, including the `geohash` field.

![](images/coronavirus_map.gif)

## The Docker container runs the following applications

* coronavirusapi_exporter.py - Python application to create time series from weather metrics using http://coronavirusapi.com/.
* Redis database with RedisTimeSeries module - to store the time series. We also use Redis Set to keep the list of states to use them in Grafana dashboard variable.
* Grafana with Redis Data Source - to display the data.

### Run using `docker-compose`

The project provides `docker-compose.yml` to start Redis with RedisTimeSeries module, Grafana 7.0 and data exporter.

```bash
docker-compose up
```

## Feedback

We love to hear from users, developers and the whole community interested by [Redis Data Source](https://github.com/RedisTimeSeries/grafana-redis-datasource) plug-in. These are various ways to get in touch with us:

- Ask a question, request a new feature and file a bug with GitHub issues.
- Star the repository to show your support.

## Other interesting resources

- [RedisTimeSeries](https://oss.redislabs.com/redistimeseries/)
- [Redis Data Source for Grafana](https://grafana.com/grafana/plugins/redis-datasource)
- [Grafana Smart Weather Dashboard](https://github.com/RedisTimeSeries/redis-weather)

## License

- Apache License Version 2.0, see [LICENSE](LICENSE)
