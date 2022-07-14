import pkg_resources
import re
import unified_planning as up
from unified_planning.engines.results import PlanGenerationResultStatus
from unified_planning.model import ProblemKind
from unified_planning.engines import PDDLPlanner, Credits
from unified_planning.exceptions import UPException
from typing import List, Optional


credits = Credits('LPG',
                  'UNIBS Team',
                  'ivan.serina@unibs.it',
                  'https://lpg.unibs.it',
                  '<license>',
                  'LPG is a planner based on local search and planning graphs.',
                  'LPG (Local search for Planning Graphs) is a planner based on local search and planning graphs.')

class LPGEngine(PDDLPlanner):

    def __init__(self):
        super().__init__(needs_requirements=False)

    @staticmethod
    def name() -> str:
        return 'lpg'

    def _get_cmd(self, domain_filename: str, problem_filename: str, plan_filename: str) -> List[str]:
        base_command = [pkg_resources.resource_filename(__name__, 'lpg'), '-o', domain_filename, '-f', problem_filename, '-n', '1', '-out', plan_filename]
        return base_command

    def _plan_from_file(self, problem: 'up.model.Problem', plan_filename: str) -> 'up.plans.Plan':
        '''Takes a problem and a filename and returns the plan parsed from the file.'''
        actions = []
        with open(plan_filename) as plan:
            for line in plan.readlines():
                if re.match(r'^\s*(;.*)?$', line):
                    continue
                res = re.match(r'^\d+:\s*\(\s*([\w?-]+)((\s+[\w?-]+)*)\s*\)\s*\[\d+\]$', line.lower())
                if res:
                    action = problem.action(res.group(1))
                    parameters = []
                    for p in res.group(2).split():
                        parameters.append(problem.env.expression_manager.ObjectExp(problem.object(p)))
                    actions.append(up.plans.ActionInstance(action, tuple(parameters)))
                else:
                    raise UPException('Error parsing plan generated by ' + self.__class__.__name__)
        return up.plans.SequentialPlan(actions)

    def _result_status(self, problem: 'up.model.Problem', plan: Optional['up.plan.Plan']) -> 'PlanGenerationResultStatus':
        '''Takes a problem and a plan and returns the status that represents this plan.
        The possible status with their interpretation can be found in the up.plan file.'''
        return PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY if plan is None else PlanGenerationResultStatus.SOLVED_SATISFICING

    @staticmethod
    def supported_kind() -> 'ProblemKind':
        supported_kind = ProblemKind()
        supported_kind.set_problem_class('ACTION_BASED')  # type: ignore
        supported_kind.set_numbers('CONTINUOUS_NUMBERS')  # type: ignore
        supported_kind.set_typing('FLAT_TYPING')  # type: ignore
        supported_kind.set_fluents_type('NUMERIC_FLUENTS')  # type: ignore
        # supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS')  # type: ignore
        # supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS')  # type: ignore
        supported_kind.set_conditions_kind('EQUALITY')  # type: ignore
        supported_kind.set_numbers('DISCRETE_NUMBERS')  # type: ignore
        supported_kind.set_effects_kind('INCREASE_EFFECTS')  # type: ignore
        supported_kind.set_effects_kind('DECREASE_EFFECTS')  # type: ignore
        return supported_kind

    @staticmethod
    def supports(problem_kind: 'ProblemKind') -> bool:
        return problem_kind <= LPGEngine.supported_kind()

    @staticmethod
    def get_credits(**kwargs) -> Optional['Credits']:
        return credits


class LPGAnytimeEngine(PDDLPlanner):

    def __init__(self):
        super().__init__(needs_requirements=False)

    @staticmethod
    def name() -> str:
        return 'lpg'

    def _get_cmd(self, domain_filename: str, problem_filename: str, plan_filename: str) -> List[str]:
        base_command = [pkg_resources.resource_filename(__name__, 'lpg'), '-o', domain_filename, '-f', problem_filename, '-n', '100', '-out', plan_filename]
        return base_command

    def _plan_from_file(self, problem: 'up.model.Problem', plan_filename: str) -> 'up.plans.Plan':
        '''Takes a problem and a filename and returns the plan parsed from the file.'''
        actions = []
        with open(plan_filename) as plan:
            for line in plan.readlines():
                if re.match(r'^\s*(;.*)?$', line):
                    continue
                res = re.match(r'^\d+:\s*\(\s*([\w?-]+)((\s+[\w?-]+)*)\s*\)\s*\[\d+\]$', line.lower())
                if res:
                    action = problem.action(res.group(1))
                    parameters = []
                    for p in res.group(2).split():
                        parameters.append(problem.env.expression_manager.ObjectExp(problem.object(p)))
                    actions.append(up.plans.ActionInstance(action, tuple(parameters)))
                else:
                    raise UPException('Error parsing plan generated by ' + self.__class__.__name__)
        return up.plans.SequentialPlan(actions)

    def _result_status(self, problem: 'up.model.Problem', plan: Optional['up.plan.Plan']) -> 'PlanGenerationResultStatus':
        '''Takes a problem and a plan and returns the status that represents this plan.
        The possible status with their interpretation can be found in the up.plan file.'''
        return PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY if plan is None else PlanGenerationResultStatus.SOLVED_SATISFICING

    @staticmethod
    def supported_kind() -> 'ProblemKind':
        supported_kind = ProblemKind()
        supported_kind.set_problem_class('ACTION_BASED')  # type: ignore
        supported_kind.set_numbers('CONTINUOUS_NUMBERS')  # type: ignore
        supported_kind.set_typing('FLAT_TYPING')  # type: ignore
        supported_kind.set_fluents_type('NUMERIC_FLUENTS')  # type: ignore
        # supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS')  # type: ignore
        # supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS')  # type: ignore
        supported_kind.set_conditions_kind('EQUALITY')  # type: ignore
        supported_kind.set_numbers('DISCRETE_NUMBERS')  # type: ignore
        supported_kind.set_effects_kind('INCREASE_EFFECTS')  # type: ignore
        supported_kind.set_effects_kind('DECREASE_EFFECTS')  # type: ignore
        return supported_kind

    @staticmethod
    def supports(problem_kind: 'ProblemKind') -> bool:
        return problem_kind <= LPGEngine.supported_kind()

    @staticmethod
    def get_credits(**kwargs) -> Optional['Credits']:
        return credits
