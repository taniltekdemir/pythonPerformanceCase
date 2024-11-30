from datetime import datetime
import asyncio
import aiohttp

BASE_URL = "http://localhost:8000/api/v1/truckdata"
TEST_DATA_TEMPLATE = {
    "truck_id": "test_truck_{}",
    "timestamp": datetime.now().isoformat(),
    "location": "40.7128,-74.00{}",
    "speed": 55.5
}

async def send_request(session, data):
    try:
        # await asyncio.sleep(50)
        async with session.post(BASE_URL, json=data) as response:
            status = response.status
            response_data = await response.json()
            return status, response_data
    except Exception as e:
        return 500, {"error": str(e)}


async def perform_bulk_requests(concurrent_requests=1000):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(concurrent_requests):
            data = TEST_DATA_TEMPLATE.copy()
            data["truck_id"] = data["truck_id"].format(i)
            data["location"] = data["location"].format(i)
            tasks.append(send_request(session, data))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


async def run_performance_test():
    concurrent_requests = 1000

    responses = await perform_bulk_requests(concurrent_requests)

    success_count = sum(1 for status, _ in responses if status == 200)
    failure_count = len(responses) - success_count

    print(f"success_count: {success_count}")
    print(f"failure_count: {failure_count}")

if __name__ == "__main__":
    asyncio.run(run_performance_test())