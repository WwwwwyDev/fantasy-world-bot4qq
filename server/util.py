import random
import numpy as np
from server.default_params import Tower
import requests as req
from server.error import LFError


# 判断成功与否
def make_decision(probability: float) -> bool:
    if probability > 1:
        probability = 1
    if probability < 0:
        probability = 0
    return np.random.choice([True, False], p=[probability, 1 - probability])

# 随机决定
def make_decision_list(keys: list, values: list, cnt: int) -> list:
    keys.append(None)
    values.append(1 - sum(values))
    return np.random.choice(keys, cnt, p=values)


# 随机姓名
class RandomUtil:
    NAME_XING = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱',
                 '秦', '尤', '许',
                 '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏',
                 '水', '窦', '章',
                 '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞',
                 '任', '袁', '柳',
                 '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝',
                 '邬', '安', '常',
                 '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和',
                 '穆', '萧', '尹',
                 '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈',
                 '宋', '茅', '庞',
                 '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾',
                 '路', '娄', '危',
                 '江', '童', '颜', '郭', '梅', '盛', '林', '***', '锺', '徐', '丘', '骆', '高', '夏', '蔡', '田', '樊',
                 '胡', '凌', '霍',
                 '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁',
                 '宣', '贲', '邓',
                 '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴',
                 '陆', '荣', '翁',
                 '荀', '羊', '於', '惠', '甄', '麹', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井',
                 '段', '富', '巫',
                 '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋',
                 '仲', '伊', '宫',
                 '甯', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶',
                 '幸', '司', '韶',
                 '郜', '黎', '蓟', '薄', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓',
                 '蔺', '屠', '蒙',
                 '池', '乔', '阴', '鬱', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬',
                 '申', '扶', '堵',
                 '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏',
                 '浦', '尚', '农',
                 '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向',
                 '古', '易', '慎',
                 '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广',
                 '禄', '阙', '东',
                 '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷',
                 '訾', '辛', '阚',
                 '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查',
                 '后', '荆', '红',
                 '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人',
                 '东方', '赫连', '皇甫',
                 '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕',
                 '令狐', '锺离', '宇文',
                 '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官', '司寇', '仉', '督', '子车', '颛孙', '端木',
                 '巫马', '公西', '漆雕', '乐正',
                 '壤驷', '公良', '拓跋', '夹谷', '宰父', '穀梁', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '段干',
                 '百里', '东郭', '南门',
                 '呼延', '归海', '羊舌', '微生', '岳', '帅', '缑', '亢', '况', '後', '有', '琴', '梁丘', '左丘', '东门',
                 '西门', '商', '牟',
                 '佘', '佴', '伯', '赏', '南宫', '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '第五', '言', '福']

    MING = ['壮', '昱杰', '开虎', '凯信', '永斌', '方洲', '长发', '可人', '天弘', '炫锐', '富明', '俊枫', '小玉', '蓝',
            '琬郡', '琛青', '予舴', '妙妙', '梓茵', '海蓉', '语娜', '馨琦', '晓馥', '佳翊']

    @staticmethod
    def random_name_str():
        if random.choice([True, False]):
            while True:
                xing_two = RandomUtil.NAME_XING[random.randint(0, len(RandomUtil.NAME_XING) - 1)]
                if len(xing_two) == 2:
                    xing = xing_two
                    break
        else:
            while True:
                xing_one = RandomUtil.NAME_XING[random.randint(0, len(RandomUtil.NAME_XING) - 1)]
                if len(xing_one) == 1:
                    xing = xing_one
                    break

        ming = RandomUtil.MING[random.randint(0, len(RandomUtil.MING) - 1)]

        return xing + ming


def head(title) -> str:
    space_cnt = 13 - len(title)
    space = " " * space_cnt
    return f"\n{space}💫「{title}」💫\n----------------------------\n"


def separate(title) -> str:
    cnt = 12 - len(title) // 2
    pre = "-" * cnt
    return f"\n{pre}{title}{pre}\n"


def gen_ico(tower_level: int) -> str:
    star_cnt = (tower_level - 1) // Tower.tower_max
    black_star_cnt = star_cnt // 4
    star_cnt -= black_star_cnt * 4
    moon_cnt = black_star_cnt // 4
    black_star_cnt -= moon_cnt * 4
    sun_cnt = moon_cnt // 4
    moon_cnt -= sun_cnt * 4
    crown_cnt = sun_cnt // 4
    sun_cnt -= crown_cnt * 4
    boom_cnt = crown_cnt // 4
    crown_cnt -= boom_cnt * 4
    star = star_cnt * "☆"
    black_star = black_star_cnt * "★"
    moon = moon_cnt * "☾"
    sun = sun_cnt * "✹"
    crown = crown_cnt * "♚"
    boom = boom_cnt * "卐"
    return boom + crown + sun + moon + black_star + star


white_code = "⁡"


# 向数字中添加空白字符防止出现下滑线
def filter_num(num: int) -> str:
    num_str = str(num)
    if len(num_str) < 5:
        return num_str
    return white_code.join(num_str[i:i + 4] for i in range(0, len(num_str), 4))


# 检查名字合法性
def check_name(name: str) -> bool:
    try:
        resp = req.post("https://www.qianmoo.top/admin/sensitiveWord/detection",
                        json={"context": name, "wordType": [1, 2, 3, 4, 99, 100]})
    except:
        raise LFError("敏感词数据库连接失败")
    content = resp.json()
    if content["code"] != 200:
        raise LFError("敏感词数据库连接失败")
    if content["data"]["wordNum"] != 0:
        return False
    else:
        return True

