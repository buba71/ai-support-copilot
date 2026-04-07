import json
import redis
from ai_service.service_factory import get_ticket_analyzer

def test_redis_cache_efficiency():
    print("--- Testing Shared Redis Cache Efficiency ---")
    
    analyzer = get_ticket_analyzer()
    
    # 1. Reset counters for test consistency (using raw client if necessary)
    client = redis.Redis(host="localhost", port=6379, db=0)
    client.delete(analyzer.cache.hits_key)
    client.delete(analyzer.cache.misses_key)
    print("Counters reset.")

    test_prompt = "Efficiency test prompt"
    test_result = {"status": "success"}

    # 2. Trigger a miss
    print("Triggering 1 miss...")
    analyzer.cache.get(test_prompt)

    # 3. Set the cache
    print("Setting cache...")
    analyzer.cache.set(test_prompt, test_result)

    # 4. Trigger 2 hits
    print("Triggering 2 hits...")
    analyzer.cache.get(test_prompt)
    analyzer.cache.get(test_prompt)

    # 5. Check efficiency
    eff = analyzer.cache.efficiency()
    print(f"Calculated Efficiency: {eff}")
    
    if eff == 0.667: # 2 hits / 3 total attempts
        print("✅ Efficiency calculation is correct (0.667)!")
    else:
        print(f"❌ Efficiency calculation error. Expected 0.667, got {eff}")

if __name__ == "__main__":
    test_redis_cache_efficiency()
