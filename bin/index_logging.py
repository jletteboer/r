import os
import logging
import logging.handlers
import splunk

logger = None


def setup_logging():
    global logger
    if not logger:
        logger = logging.getLogger('splunk.r')
        if 'SPLUNK_HOME' in os.environ:
            splunk_home = os.environ['SPLUNK_HOME']
            logging_default_config_file = os.path.join(splunk_home, 'etc', 'log.cfg')
            logging_local_config_file = os.path.join(splunk_home, 'etc', 'log-local.cfg')
            logging_stanza_name = 'python'
            logging_file_name = "r.log"
            base_log_path = os.path.join('var', 'log', 'splunk')
            logging_format = "%(asctime)s %(levelname)s %(message)s"
            splunk_log_handler = logging.handlers.RotatingFileHandler(
                os.path.join(splunk_home, base_log_path, logging_file_name), mode='a')
            splunk_log_handler.setFormatter(logging.Formatter(logging_format))
            logger.addHandler(splunk_log_handler)
            splunk.setupSplunkLogger(logger, logging_default_config_file, logging_local_config_file, logging_stanza_name)
    return logger

setup_logging()


def log(source, fields):
    #r_index = service.indexes["r"]
    #args = {
    #    'index': r_index.name,
    #    'source': source,
    #    'sourcetype': 'r'
    #}
    body = 'module=\"%s\"' % source
    for k in fields:
        v = fields[k]
        if isinstance(v, list) or isinstance(v, set):
            body += ' '.join(['%s=\"%s\" ' % (k, f) for f in v])
        else:
            body += ' %s=\"%s\" ' % (k, v)

    logger.info(body)

    #r_index.service.post(
    #    '/services/receivers/simple',
    #    body=body,
    #    **args)