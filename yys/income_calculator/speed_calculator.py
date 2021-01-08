from enum import Enum


class SpeedCalculationCategory(Enum):
    SinglePull = 0
    SinglePush = 1
    DoublePull = 2
    PullPush = 3
    PushPull = 4


SHIRANUI_BONUS_SPEED = 25


def calculate_single_pull(input_dict):
    """
    :param input_dict:
    :return:
    """
    self_has_shiranui = input_dict['self_has_shiranui']
    opponent_has_shiranui = input_dict['opponent_has_shiranui']
    self_top_speed = input_dict['self_top_speed']
    opponent_top_speed = input_dict['opponent_top_speed']
    pull_coefficient = input_dict['pull_coefficient']
    if self_top_speed == opponent_top_speed:
        return {
            'speed': self_top_speed * (1 - pull_coefficient)
        }



    return


def calculate_single_push(input_dict):
    return


def calculate_double_pull(input_dict):
    return


def calculate_pull_push(input_dict):
    return


def calculate_push_pull(input_dict):
    return


CalculatorByCategory = {
    SpeedCalculationCategory.SinglePull: calculate_single_pull,
    SpeedCalculationCategory.SinglePush: calculate_single_push,
    SpeedCalculationCategory.DoublePull: calculate_double_pull,
    SpeedCalculationCategory.PullPush: calculate_pull_push,
    SpeedCalculationCategory.PushPull: calculate_push_pull,
}


def calculate_speed(input_dict, category):
    calculator = CalculatorByCategory[category]
    result = calculator(input_dict)
    return result
