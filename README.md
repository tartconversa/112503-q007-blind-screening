# 长剧盲评的可比性与剪辑复核配额

看片批次、真实接触区间及补看可用资源。评分 1 到 7。故事片段有前置段落，多版片段的 segment 相同表示按同一剧情位置比较。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- segments.csv 的字段为 edition、segment、previous、from_sec、to_sec、rev。
- rooms.csv 的字段为 show、round、room、date、capacity、edition、segments。
- assignments.csv 的字段为 allocation、viewer、show、stratum、status。
- attendance.csv 的字段为 viewer、show、observed_start、observed_end、prior_edition、prior_segment、known_on。
- forms.csv 的字段为 form、viewer、show、segment、score。
- availability.csv 的字段为 viewer、can_attend、stratum、screened、requires_access。
- room_capability.csv 的字段为 room、accessible_seats。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
