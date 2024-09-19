from service.pojo.user import User
from service.util import head, tail
from service.default_params import Tower
from service.pojo.combat import TowerMonsterCombatPojo, get_attribute_content
def tower_info(params: list, user: User) -> str:
    star_cnt = (user.tower_level-1) // Tower.tower_max
    moon_cnt = star_cnt // 4
    star_cnt -= moon_cnt * 4
    sun_cnt = moon_cnt // 4
    moon_cnt -= sun_cnt * 4
    crown_cnt = sun_cnt // 4
    sun_cnt -= crown_cnt * 4
    boom_cnt = crown_cnt // 4
    crown_cnt -= boom_cnt * 4
    star = star_cnt * "⭐"
    moon = moon_cnt * "🌙"
    sun = sun_cnt * "☀️"
    crown = crown_cnt * "👑"
    boom = boom_cnt * "💥"
    ico_res = boom + crown + sun + moon + star
    monster_name = Tower.monster_name[(user.tower_level-1) % Tower.tower_max]
    current_tower_level  = user.tower_level
    return head(f"第{user.tower_level}层信息") +f"""[小怪] {monster_name}{ico_res}
[精英怪] {monster_name}(变异){ico_res}
[首领] {monster_name}王{ico_res}""" + tail(f"首领属性") + get_attribute_content(TowerMonsterCombatPojo(current_tower_level))