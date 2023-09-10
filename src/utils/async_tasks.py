import asyncio


async def execute_tasks(list_of_tasks: list) -> list:
    """Execute tasks asynchronously to get the best performance and return list of result"""

    # Run the tasks concurrently
    results = await asyncio.gather(*list_of_tasks, return_exceptions=True)

    # Add all values that are not None
    list_of_processed_tasks = [element for element in results if element is not None]

    return list_of_processed_tasks
