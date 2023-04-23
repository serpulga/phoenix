from concurrent.futures import Executor


def executor_pool() -> Executor:
    from main import app

    return app.state.executor_pool
