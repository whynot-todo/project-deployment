import tornado.ioloop
import tornado.web
import json
import urllib.request
from datetime import datetime, timedelta
import os


class MainHandler(tornado.web.RequestHandler):

    @staticmethod
    def format_datetime(_datetime):
        utc_date = datetime.strptime(_datetime[:-9], "%Y-%m-%dT%H:%M:%S")
        return utc_date + timedelta(hours=8)

    @staticmethod
    def parse_time_block(target):
        total_height = 1000
        day_delta, now = timedelta(hours=24), datetime.now()
        zero_datetime = now - timedelta(
            hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond
        )
        for _i in target:
            _start_time, _end_time = _i["start_time"], _i["end_time"]
            tomato_precent = (_end_time - _start_time) / day_delta
            top_precent = (_start_time - zero_datetime) / day_delta
            _i["left"] = total_height * top_precent
            _i["width"] = total_height * tomato_precent

        return target
    
    @staticmethod
    def is_today(time):
        _time = time.strftime("%Y-%m-%d %H:%M:%S")
        _date = datetime.now().date().strftime("%Y-%m-%d")
        return f"{_date} 00:00:00" <= _time <= f"{_date} 23:59:59"

    @staticmethod
    def is_continuous(pre_t, cur_t):
        if not pre_t:
            return True, timedelta(minutes=0)
        _cur_start_time = cur_t["start_time"]
        _pre_end_time = pre_t["end_time"]
        _delta = _cur_start_time - _pre_end_time
        return _delta <= timedelta(minutes=10), _delta
    
    @staticmethod
    def get_bg_color(tomato):
        color_map = dict(
            no_con_tit="rgb(36, 164, 136)",
            no_con="#a8a3a3",
            no_tit="rgb(36, 221, 49)"
        )
        _is_continuous = tomato.get("is_continuous")
        _title = tomato.get("task")[0].get("title")

        if not _is_continuous and not _title:
            return color_map.get("no_con_tit")
        elif not _is_continuous:
            return color_map.get("no_con")
        elif not _title:
            return color_map.get("no_tit")
        else:
            return None

    @staticmethod
    def get_max_continus(tomato_list):
        _count = 0
        contu_list = []
        for _i in tomato_list:
            if _i.get("is_continuous"):
                _count += 1
            else:
                contu_list.append(_count)
                _count = 0

        contu_list.append(_count)

        return max(contu_list), contu_list[-1]

    @staticmethod
    def get_score():
        """
        1. 连续的番茄
        2. 不连续的番茄
        2. 番茄的时长
        3. 无标题的番茄或者添加的番茄
        """
        pass


    def get(self):
        url = 'https://api.dida365.com/api/v2/pomodoros/timeline'

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cookie": "UM_distinctid=180929bb18739d-09462cf713e58c-49647e56-144000-180929bb188335; t=73AE2E6CC13DD96769D3228AEF41CBE964EDC68D37C3D367BA9245FB043EC7D7186C31FD3F39C211862E9EE26FDF737A101401AE59A9B2604C3B36C08BDB3E60A13A0371B5EB85CEA02292AF70C5C33D7471C6C8CCE687EF4E8C68F32CC0AB51385AA04082B6E13207380EE6E17F65D7FFFFEEAD0717CC2C25CF649369FDC0C5C584137C5C040F2F6977C7AE93E07C3C0A6993E9066367DBC093C355F178EA86151002FFD8A51141ED48EB889B07BD4E; AWSALB=PzP62kX7+ewBy3hwAAlfZGcwd1d7lOnXFTb8T13nCS69PEMiNYWTdGVJr3QmmZQieobNR1bz6fwUo2ZHtvluw3IBVlf5ETuv0DKEV+njUgiDEwl0q91SIqnIdZuD; AWSALBCORS=PzP62kX7+ewBy3hwAAlfZGcwd1d7lOnXFTb8T13nCS69PEMiNYWTdGVJr3QmmZQieobNR1bz6fwUo2ZHtvluw3IBVlf5ETuv0DKEV+njUgiDEwl0q91SIqnIdZuD",
            "hl": "zh_CN",
            "origin": "https://dida365.com",
            "referer": "https://dida365.com/",
            "sec-ch-ua": '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceid": "632596a16285a8648d1118d5",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
            "x-device": '{"platform": "web","os": "Windows 10","device": "Chrome 105.0.0.0","name": "","version": 4265,"id": "630a2f0e1ed3070024891234","channel": "website","campaign": "", "websocket": "632546056285a8648d1117b0"}'
        }
        # 请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        content = json.loads(content)
        content = sorted(content, key=lambda _i: _i["startTime"])

        _res = []
        for _i in content:
            _tomato, tasks_list = dict(), _i["tasks"]
            start_time = self.format_datetime(_i["startTime"])
            end_time = self.format_datetime(_i["endTime"])
            # if not self.is_today(start_time):
            #     continue
            # 任务信息处理
            _tomato["task"] = []
            for _t in tasks_list:
                _task_dict = dict(
                    title=_t.get("title"), project_name=_t.get("projectName"), tags=_t.get("tags"),
                    start_time=datetime.strptime(
                        _i["startTime"][:-9], "%Y-%m-%dT%H:%M:%S"),
                    end_time=datetime.strptime(
                        _i["endTime"][:-9], "%Y-%m-%dT%H:%M:%S")
                )
                _tomato["task"].append(_task_dict)
            # 基本新消息
            _tomato["start_time"] = start_time
            _tomato["end_time"] = end_time
            _tomato["is_add"] = _i.get("added")
            # 是否连续
            _is_continuous, _delta = self.is_continuous(
                _res[-1] if len(_res) else {}, _tomato
            )
            _tomato["is_continuous"] = _is_continuous
            rest_time = round(_delta.seconds / 60, 2)
            _tomato["rest_time"] = '较长' if rest_time > 200 else rest_time
            _tomato["bgColor"] = self.get_bg_color(_tomato)

            _res.append(_tomato)
        max_continus, last_continus = self.get_max_continus(_res)
        self.render(
            "index.html",
            tomato_list=self.parse_time_block(_res),
            max_continus=dict(max_continus=max_continus,last_continus=last_continus)
        )


def make_app():
    return tornado.web.Application(
        [(r"/", MainHandler)],
        # 网页模板
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # 静态路径
        static_path=os.path.join(os.path.dirname(__file__),"static")
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("OK~~~~")
    tornado.ioloop.IOLoop.current().start()
