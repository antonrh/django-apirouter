from django.test import override_settings

from apirouter.conf import import_setting

obj = object()


@override_settings(IMPORT_TARGET="tests.test_conf.obj")
def test_import_settings_string():
    target = import_setting("IMPORT_TARGET", obj)

    assert target is obj
