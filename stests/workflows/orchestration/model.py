import typing

from stests.core.orchestration import ExecutionContext
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.workflows.generators.meta import GENERATOR_MAP as MODULES



class WorkflowStep():
    """A step with a phase of a broader workflow.
    
    """
    def __init__(self, ctx: ExecutionContext, index: int, module):
        """Constructor.
        
        """
        # Workflow execution context information.
        self.ctx: ExecutionContext = ctx

        # Index within the set of phase steps.
        self.index: int = index

        # Flag indicating whether this is the last step within the phase.
        self.is_last: bool = False

        # Python module in which the step is declared.
        self.module = module

        # Execution error.
        self.error: typing.Union[str, Exception] = None

        # Execution result.
        self.result: typing.Union[None, typing.Callable] = None

    @property
    def has_verifer(self) -> bool:
        try:
            self.module.verify
        except AttributeError:
            return False
        else:
            return True

    @property
    def has_verifer_for_deploy(self) -> bool:
        try:
            self.module.verify_deploy
        except AttributeError:
            return False
        else:
            return True

    @property
    def label(self) -> str:
        return self.module.LABEL
    
    @property
    def is_async(self) -> bool:     
        """A flag indicating whether this is an asynchronous step - i.e. relies upon chain events to complete."""   
        return hasattr(self.module, "verify_deploy")   

    @property
    def is_sync(self) -> bool:     
        """A flag indicating whether this is a synchronous step."""   
        return not self.is_async

    def execute(self):
        """Performs step execution.
        
        """
        try:
            self.result = self.module.execute(self.ctx)
        except Exception as err:
            self.error = err


    def verify(self):
        """Performs step verification.
        
        """
        self.module.verify(self.ctx)


    def verify_deploy(self, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
        """Performs step deploy verification.
        
        """
        self.module.verify_deploy(self.ctx, node_id, block_hash, deploy_hash)


class WorkflowPhase():
    """A phase within a broader workflow.
    
    """
    def __init__(self, ctx: ExecutionContext, index: int, container):
        """Constructor.
        
        """
        # Index within the set of phases.
        self.index: int = index

        # Flag indicating whether this is the last phase within the workflow.
        self.is_last: bool = False

        # Set steps.
        if isinstance(container, tuple):
            self.steps = [WorkflowStep(ctx, i, s) for i, s in enumerate(container)]
        else:
            self.steps = [WorkflowStep(ctx, i, s) for i, s in enumerate(container.STEPS)]

        # Set last step flag.
        if self.steps:
            self.steps[-1].is_last = True


    def get_step(self, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        return self.steps[step_index - 1]


class Workflow():
    """A workflow executed in order to test a scenario.
    
    """
    def __init__(self, ctx: ExecutionContext, meta):
        """Constructor.

        :param ctx: Execution context information.
        :param meta: Workflow metadata module.

        """
        # Set phases.
        self.phases = [WorkflowPhase(ctx, i, p) for i, p in enumerate(meta.PHASES)]

        # Set last phase flag.
        if self.phases:
            self.phases[-1].is_last = True

    
    def get_phase(self, phase_index: int) -> WorkflowPhase:
        """Returns a phase within managed collection.
        
        """
        return self.phases[phase_index - 1]


    def get_step(self, phase_index: int, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        phase = self.get_phase(phase_index) 

        return phase.get_step(step_index)


    @staticmethod
    def create(ctx: ExecutionContext):
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            MODULES[ctx.run_type]
        except KeyError:
            raise ValueError(f"Unsupported workflow type: {ctx.run_type}")
        else:
            return Workflow(ctx, MODULES[ctx.run_type])


    @staticmethod
    def get_phase_(ctx: ExecutionContext, phase_index: int) -> WorkflowPhase:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            wflow = Workflow.create(ctx)
        except:
            return None
        else:
            return wflow.get_phase(phase_index)


    @staticmethod
    def get_phase_step(ctx: ExecutionContext, phase_index: int, step_index: int) -> WorkflowStep:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            wflow = Workflow.create(ctx)
        except:
            return None
        else:
            return wflow.get_step(phase_index, step_index)
