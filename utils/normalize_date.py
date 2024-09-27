import time
from typing import Iterable

def normalize_date(datestr: str, date_pattern: 'str | Iterable[str]', normalizing_pattern: str="%Y-%m-%d") -> str:
    """
    #### 可将网站给的时间日期格式转换成本项目采用的标准日期格式 "%Y-%m-%d"
    如把 ' 17-07-2022' 标准化成 '2022-07-17'

    %a Locale’s abbreviated weekday name.

    %A Locale’s full weekday name.

    %b Locale’s abbreviated month name.

    %B Locale’s full month name.

    %c Locale’s appropriate date and time representation.

    %d Day of the month as a decimal number [01,31].

    %H Hour (24-hour clock) as a decimal number [00,23].

    %I Hour (12-hour clock) as a decimal number [01,12].

    %j Day of the year as a decimal number [001,366].

    %m Month as a decimal number [01,12].

    %M Minute as a decimal number [00,59].

    %p Locale’s equivalent of either AM or PM.

    %S Second as a decimal number [00,61].

    %U Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.

    %w Weekday as a decimal number [0(Sunday),6].

    %W Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.

    %x Locale’s appropriate date representation.

    %X Locale’s appropriate time representation.

    %y Year without century as a decimal number [00,99].

    %Y Year with century as a decimal number.

    %z Time zone offset indicating a positive or negative time difference from UTC/GMT of the form +HHMM or -HHMM, where H represents decimal hour digits and M represents decimal minute digits [-23:59, +23:59]. 1

    %Z Time zone name (no characters if no time zone exists). Deprecated. 1

    %% A literal '%' character.
    """
    for pattern in [date_pattern] if isinstance(date_pattern, str) else date_pattern:
        try:
            return time.strftime(normalizing_pattern, time.strptime(datestr,pattern))
        except:
            pass
    raise ValueError(f"time data '{datestr}' does not match any format in {[date_pattern] if isinstance(date_pattern, str) else date_pattern}")


def normalized_local_date(normalizing_pattern: str="%Y-%m-%d_%H:%M:%S") -> str:
    '''
    #### 输出标准化的当前日期，如 '2022-07-28'
    可用于不显示账户的注册时间的网站，所以自己填。但其实不太准确，因为不知道网站的显示的到期时间是用什么时区
    '''
    return time.strftime(normalizing_pattern,time.localtime())