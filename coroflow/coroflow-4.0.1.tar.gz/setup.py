# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coroflow']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'coroflow',
    'version': '4.0.1',
    'description': 'Asynchronous pipeline builder',
    'long_description': '# Coroflow: Easy and Fast Pipelines\n\nCoroflow makes it easy to run pipelines with coroutines and also support mixing\nin blocking functions and generators.\n\nCoroflow does a lot of heavy-lifting for you:\n\n* Manage all tasks in the pipelinen concurently in one thread using coroutines\n* Pass data between tasks with queues\n* Easily specify concurrency limits\n* Connect stages of the pipeline with fan-out/fan-in patterns or load-balancer patterns\n* Define tasks as coroutines, normal (blocking) functions, async generators or normal generators; coroflow will run it appropriately \n  in either the event-loop, a thread pool, or optionally in a processes pool\n* Provides an apache-ariflow-like api for connecting tasks\n\n\n\n## Getting Started\n\n\nCoroflow makes it easy to run pipelines with coroutines and also support mixing\nin blocking functions and generators\n\n```python\n    from coroflow import Node, Pipeline\n    import asyncio\n    import time\n\n\n    class GenNode(Node):\n        async def execute():\n            """\n            The execute method of the first/root Node has to be a generator,\n            either async or synchronous.\n            """\n            for url in [\'img_url_1\', \'img_url_2\', \'img_url_3\']:\n                print(f"Yielding {url}")\n                await asyncio.sleep(1)\n                yield url\n            print("Generator is exhausted")\n            return\n\n\n    class DoSomething(Node):\n        async def execute(inpt, param=None):\n            """\n            The execute method of all non-root Nodes should be a async\n            or synchronous method.\n            """\n            # do your async pipelined work\n            await asyncio.sleep(1)  # simulated IO delay\n            outp = inpt\n            print(f"func1: T1 sending {inpt}")\n            return outp\n\n\n    p = Pipeline()\n    t0 = GenNode(\'gen\', p)\n    t1 = DoSomething(\'func1\', p, kwargs={\'param\': \'param_t1\'})\n    t2 = DoSomething(\'func2\', p, kwargs={\'param\': \'param_t2\'})\n    t0.set_downstream(t1)\n    t1.set_downstream(t2)\n\n\n    start_time = time.time()\n    p.run()\n    print(f"Asynchronous duration: {time.time() - start_time}s.")\n```\n\n# Tests\n\nRun like so:\n\n$ pytest',
    'author': 'Dewald Abrie',
    'author_email': 'dewaldabrie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dewaldabrie/coroflow/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
