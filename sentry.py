import machine
import binascii
import os
import sys
import io
import urequests
import ujson


def get_exception_str(exception):
    exception_io = io.StringIO()
    sys.print_exception(exception, exception_io)
    exception_io.seek(0)
    result = exception_io.read()
    exception_io.close()
    return result


class SentryClient:
    def __init__(self, project_id, key):
        self.project_id = project_id
        self.key = key

    def send_exception(self, exception):
        url_tpl = 'https://sentry.io/api/{}/store/'
        url = url_tpl.format(self.project_id)
        json_data = (
            '{'
            '"event_id": "%(event_id)s",'
            '"exception": {"values":[{"type": "%(type)s","value": '
            '%(value)s,"module": "%(module)s"}]},'
            '"tags": {'
            '"machine_id": "%(machine_id)s", '
            '"platform": "%(platform)s",'
            '"os.name": "%(os_name)s",'
            '"os.version": "%(os_version)s"},'
            '"extra": {"stacktrace": %(stacktrace)s}'
            '}' %
            {
                'event_id': binascii.hexlify(os.urandom(16)).decode(),
                'type': exception.__class__.__name__,
                'value': ujson.dumps(
                    exception.args[0] if exception.args else '',
                ),
                'module': exception,
                'stacktrace': ujson.dumps(get_exception_str(exception)),
                'machine_id': binascii.hexlify(machine.unique_id()).decode(),
                'platform': sys.platform,
                'os_name': sys.implementation.name,
                'os_version': ".".join(
                    str(x) for x in sys.implementation.version
                ),
            }
        )
        return urequests.post(
            url,
            data=json_data,
            headers = {
                "Content-Type": "application/json",
                "X-Sentry-Auth": "Sentry sentry_version=7, sentry_key={}, "
                "sentry_client=sentry-micropython/0.1".format(self.key)
            },
        )
