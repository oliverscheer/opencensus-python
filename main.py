import logging
import config
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

# TODO: replace the all-zero GUID with your instrumentation key.
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=' + config.INSTRUMENTATION_KEY)
)

def valuePrompt():
    try:
        line = input("Enter a value: ")
        logger.warning(line)
    except Exception:
        properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}
        logger.exception('Captured an exception.', extra=properties)

def main():
    while True:
        logger.info("Another iteration")
        valuePrompt()

if __name__ == "__main__":
    main()