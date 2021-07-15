import logging
import config
import time
import psutil

# Required for Logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Required for correlation
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

# Required for metrics
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

CONNECTION_STRING = 'InstrumentationKey=' + config.INSTRUMENTATION_KEY
print("Connection String: " + CONNECTION_STRING)

def sample_logging():
    logger_name = "logging_sample"
    logger = logging.getLogger(logger_name)
    logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))

    # Default Log Level is Warning, everything below warning is ignored.
    # Levels are: INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(logging.INFO)
    logger.info('Hello, World! This is an INFO')
    logger.warning("We might run out of time. This is a WARNING")
    logger.critical("Houston, we have a problem. This is CRITICAL")


def sample_correlation():

    config_integration.trace_integrations(['logging'])

    logger_name = "sample_correlation"
    logger = logging.getLogger(logger_name)

    handler = AzureLogHandler(connection_string=CONNECTION_STRING)
    handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
    logger.addHandler(handler)

    tracer = Tracer(
        exporter=AzureExporter(connection_string=CONNECTION_STRING),
        sampler=ProbabilitySampler(1.0)
    )

    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')


def sample_custom_properties():

    logger_name = "sample_custom_properties"
    logger = logging.getLogger(logger_name)

    logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))

    properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}
    logger.warning('action', extra=properties)


def sample_metrics():

    stats = stats_module.stats
    view_manager = stats.view_manager
    stats_recorder = stats.stats_recorder

    CARROTS_MEASURE = measure_module.MeasureInt("carrots",
                                                "number of carrots",
                                                "carrots")
    CARROTS_VIEW = view_module.View("carrots_view",
                                    "number of carrots",
                                    [],
                                    CARROTS_MEASURE,
                                    aggregation_module.CountAggregation())

    # Enable metrics
    # Set the interval in seconds in which you want to send metrics
    exporter = metrics_exporter.new_metrics_exporter(connection_string=CONNECTION_STRING)
    view_manager.register_exporter(exporter)

    view_manager.register_view(CARROTS_VIEW)
    mmap = stats_recorder.new_measurement_map()
    tmap = tag_map_module.TagMap()

    mmap.measure_int_put(CARROTS_MEASURE, 1000)
    mmap.record(tmap)
    # Default export interval is every 15.0s
    # Your application should run for at least this amount
    # of time so the exporter will meet this interval
    # Sleep can fulfill this
    time.sleep(60)
    print("Done recording metrics")


def sample_performance_counter():
    # All you need is the next line. You can disable performance counters by
    # passing in enable_standard_metrics=False into the constructor of
    # new_metrics_exporter()
    _exporter = metrics_exporter.new_metrics_exporter(connection_string=CONNECTION_STRING)

    for i in range(10):
        print(psutil.virtual_memory())
        time.sleep(3)

    print("Done recording metrics")


def sample_trace():

    tracer = Tracer(
        exporter=AzureExporter(
            connection_string=CONNECTION_STRING
        ),
        sampler=ProbabilitySampler(1.0)
    )

    with tracer.span(name='hello'):
        print('Hello, World!')


if __name__ == "__main__":
    sample_logging()
    sample_correlation()
    sample_custom_properties()
    sample_metrics()
    sample_performance_counter()
    sample_trace()
