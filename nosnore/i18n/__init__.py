import ConfigParser
from gettext import gettext, ngettext

from babel import Locale 


_ = gettext
N_ = ngettext


def i18n_init():
    """ Initialize locale """
    config = ConfigParser.RawConfigParser()
    config.read('nosnore/configs/config.ini')
    locale = config.get('Locale', 'locale')
    Locale.parse(locale, sep='_')


def set_locale(locale):
    """ Set locale """
    config = ConfigParser.RawConfigParser()
    config.read('nosnore/configs/config.ini')
    available_locale = config.get('Locale', 'available_locale')
    available_locale = available_locale.split(',')
    if locale in available_locale:
        config.set('Locale', 'locale', locale)
    else:
        raise NameError("The following locale is not available.")
    with open('nosnore/configs/config.ini', 'wb') as configfile:
        config.write(configfile)


i18n_init()


if __name__ == '__main__':
    set_locale('en_US')
