import time
import requests

# Container lopala run chestunnam కాబట్టి localhost vaadali
BASE_URL = "http://localhost:8000"

def run_benchmark():
    print("🚀 Starting CDN Performance Benchmark...")
    
    # 1. Upload a file first with explicit Content-Type to avoid S3 Errors
    # Added ('filename', content, 'mime-type') format for stability
    files = {'file': ('test.txt', b'Hello world content for benchmark', 'text/plain')}
    
    try:
        upload_res = requests.post(
            f"{BASE_URL}/assets/upload", 
            files=files, 
            data={'is_private': 'false'}
        )
        
        if upload_res.status_code != 201:
            print(f"❌ Upload failed with status {upload_res.status_code}: {upload_res.text}")
            return
            
        data = upload_res.json()
        # API 'id' return chesthe 'id' teesko, lekapothe 'asset_id' teesko
        asset_id = data.get('id') or data.get('asset_id')
        etag = data['etag']
        print(f"✅ Uploaded asset for testing. ID: {asset_id}")

        # 2. Simulate 100 requests to check Cache/ETag logic
        hits = 0
        total_requests = 100
        
        print(f"📡 Sending {total_requests} cached requests...")
        start_time = time.time()
        for i in range(total_requests):
            # We send the ETag in If-None-Match to simulate a CDN/Browser cache check
            headers = {'If-None-Match': etag}
            response = requests.get(f"{BASE_URL}/assets/{asset_id}/download", headers=headers)
            
            # 304 Not Modified means Cache Hit
            if response.status_code == 304:
                hits += 1
                
        end_time = time.time()
        
        # 3. Calculate Stats
        duration = end_time - start_time
        hit_ratio = (hits / total_requests) * 100
        
        print("\n--- 📊 BENCHMARK RESULTS ---")
        print(f"Total Requests: {total_requests}")
        print(f"Cache Hits (304 Responses): {hits}")
        print(f"Cache Hit Ratio: {hit_ratio}%")
        print(f"Total Time: {duration:.4f} seconds")
        print(f"Avg Response Time (Cached): {(duration/total_requests)*1000:.2f}ms")
        print("----------------------------\n")

        if hit_ratio >= 95:
            print("🎯 TARGET ACHIEVED: Cache Hit Ratio is over 95%!")
        else:
            print("⚠️ Warning: Cache Hit Ratio is below target.")
            
    except Exception as e:
        print(f"💥 Script Error: {str(e)}")

if __name__ == "__main__":
    # App start avvadaniki konchem time ivvali
    print("⏳ Waiting for server to stabilize...")
    time.sleep(5) 
    run_benchmark()