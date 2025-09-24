
import copy


class BasePythonScriptEngineEnvironment:
    def __init__(self, environment_globals=None):
        self.globals = environment_globals or {}

    def evaluate(self, expression, context, external_context=None):
        raise NotImplementedError("Subclass must implement this method")

    def execute(self, script, context, external_context=None):
        raise NotImplementedError("Subclass must implement this method")

    def call_service(self, context, **kwargs):
        raise NotImplementedError("Subclass must implement this method.")


class TaskDataEnvironment(BasePythonScriptEngineEnvironment):

    def evaluate(self, expression, context, external_context=None):
        my_globals = copy.copy(self.globals)  # else we pollute all later evals.
        self._prepare_context(context)
        my_globals.update(external_context or {})
        my_globals.update(context)
        return eval(expression, my_globals)

    def execute(self, script, context, external_context=None):
        self.check_for_overwrite(context, external_context or {})
        my_globals = copy.copy(self.globals)
        self._prepare_context(context)
        my_globals.update(external_context or {})
        context.update(my_globals)
        try:
            exec(script, context)
        finally:
            pass
            #self._remove_globals_and_functions_from_context(context, external_context)
        return context

    def _prepare_context(self, context):
        pass

    def _remove_globals_and_functions_from_context(self, context, external_context=None):
        """When executing a script, don't leave the globals, functions
        and external methods in the context that we have modified."""
        for k in list(context):
            if k == "__builtins__" or \
                    hasattr(context[k], '__call__') or \
                    k in self.globals or \
                    external_context and k in external_context:
                context.pop(k)

    def check_for_overwrite(self, context, external_context):
        """It's possible that someone will define a variable with the
        same name as a pre-defined script, rendering the script un-callable.
        This results in a nearly indecipherable error.  Better to fail
        fast with a sensible error message."""
        func_overwrites = set(self.globals).intersection(context)
        func_overwrites.update(set(external_context).intersection(context))
        if len(func_overwrites) > 0:
            msg = f"You have task data that overwrites a predefined " \
                  f"function(s). Please change the following variable or " \
                  f"field name(s) to something else: {func_overwrites}"
            raise ValueError(msg)
