---
last_updated: 2026-04-14
confidence: high
sources: [queue-systems, job-scheduling, logging-patterns, error-tracking]
---

# Render Queue Management

## Overview

Queue management for batch renders: job submission, progress tracking, error logging,
and completion reporting. Includes Python patterns for queue creation, status polling,
and error recovery.

## Queue Data Model

### Job Schema (JSON)
```json
{
  "job_id": "shot_001_lighting_v02",
  "created_at": "2026-04-14T10:00:00Z",
  "status": "in_progress",
  "priority": 1,
  "blend_file": "/projects/shot_001/lighting_v02.blend",
  "output_dir": "/renders/shot_001/lighting_v02",
  "frames": {
    "start": 1,
    "end": 250
  },
  "render_settings": {
    "engine": "CYCLES",
    "samples": 256,
    "denoise": true,
    "gpu": true
  },
  "progress": {
    "frames_completed": 87,
    "frames_failed": 2,
    "started_at": "2026-04-14T10:05:00Z",
    "eta_completion": "2026-04-14T14:30:00Z"
  },
  "errors": [
    {
      "frame": 15,
      "error": "CUDA out of memory",
      "retry_count": 2,
      "timestamp": "2026-04-14T10:15:00Z"
    }
  ],
  "output_metadata": {
    "format": "exr",
    "color_depth": 32,
    "file_size_mb": 0,
    "checksum": ""
  }
}
```

## Queue Management Patterns

### Simple File-Based Queue
```python
import json
import os
from datetime import datetime
from pathlib import Path

class RenderQueue:
    def __init__(self, queue_dir="/renders/queue"):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(exist_ok=True)
    
    def submit_job(self, job_id, blend_file, frames_start, frames_end, engine="CYCLES"):
        """Add render job to queue"""
        job = {
            "job_id": job_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "blend_file": blend_file,
            "frames": {"start": frames_start, "end": frames_end},
            "engine": engine,
            "progress": {"completed": 0, "failed": 0}
        }
        
        queue_file = self.queue_dir / f"{job_id}.json"
        with open(queue_file, 'w') as f:
            json.dump(job, f, indent=2)
        
        print(f"Job submitted: {job_id}")
        return job_id
    
    def get_job(self, job_id):
        """Retrieve job status"""
        queue_file = self.queue_dir / f"{job_id}.json"
        if queue_file.exists():
            with open(queue_file) as f:
                return json.load(f)
        return None
    
    def update_progress(self, job_id, frames_completed, frames_failed=0):
        """Update job progress"""
        job = self.get_job(job_id)
        if job:
            job["status"] = "in_progress"
            job["progress"]["completed"] = frames_completed
            job["progress"]["failed"] = frames_failed
            job["updated_at"] = datetime.utcnow().isoformat()
            
            queue_file = self.queue_dir / f"{job_id}.json"
            with open(queue_file, 'w') as f:
                json.dump(job, f, indent=2)
    
    def mark_complete(self, job_id):
        """Mark job as finished"""
        job = self.get_job(job_id)
        if job:
            job["status"] = "completed"
            job["completed_at"] = datetime.utcnow().isoformat()
            
            queue_file = self.queue_dir / f"{job_id}.json"
            with open(queue_file, 'w') as f:
                json.dump(job, f, indent=2)
    
    def list_pending(self):
        """List all pending jobs"""
        pending = []
        for f in self.queue_dir.glob("*.json"):
            with open(f) as fh:
                job = json.load(fh)
                if job["status"] == "pending":
                    pending.append(job)
        return pending
```

### Usage Example
```python
queue = RenderQueue()

# Submit jobs
queue.submit_job("shot_001_v1", "shot_001.blend", 1, 250)
queue.submit_job("shot_002_v1", "shot_002.blend", 1, 200)

# Check pending
pending = queue.list_pending()
print(f"Pending jobs: {len(pending)}")

# Update progress
queue.update_progress("shot_001_v1", frames_completed=100)

# Mark complete
queue.mark_complete("shot_001_v1")
```

## Progress Tracking

### Frame-Level Logging
```python
import logging

def setup_logging(job_id):
    """Create per-job logger"""
    log_file = f"/renders/logs/{job_id}.log"
    
    logger = logging.getLogger(job_id)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# In render loop
logger = setup_logging("shot_001_v1")
logger.info("Starting render job")

for frame in range(1, 251):
    try:
        # Render frame
        cmd = ["blender", "-b", "scene.blend", "-f", str(frame), "-o", "/renders/frame_####.exr"]
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        if result.returncode == 0:
            logger.info(f"Frame {frame:04d} rendered successfully")
        else:
            logger.error(f"Frame {frame:04d} failed: {result.stderr.decode()}")
    except subprocess.TimeoutExpired:
        logger.error(f"Frame {frame:04d} timeout (10min)")
    except Exception as e:
        logger.error(f"Frame {frame:04d} error: {str(e)}")

logger.info("Job completed")
```

### Real-Time Status Endpoint
```python
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/queue/<job_id>')
def get_status(job_id):
    """REST API for job status"""
    queue_file = f"/renders/queue/{job_id}.json"
    
    if os.path.exists(queue_file):
        with open(queue_file) as f:
            job = json.load(f)
        
        total = job["frames"]["end"] - job["frames"]["start"] + 1
        completed = job["progress"]["completed"]
        percent = (completed / total) * 100
        
        return jsonify({
            "job_id": job_id,
            "status": job["status"],
            "progress": f"{completed}/{total} ({percent:.1f}%)",
            "eta": job.get("progress", {}).get("eta")
        })
    
    return jsonify({"error": "Job not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)
```

## Error Handling & Retry

### Automatic Retry with Backoff
```python
import time

def render_with_retry(blend_file, frame, output_path, max_retries=3):
    """Render single frame with exponential backoff"""
    
    for attempt in range(max_retries):
        try:
            cmd = [
                "blender", "-b", blend_file, 
                "-f", str(frame),
                "-o", output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=600,  # 10 min per frame
                text=True
            )
            
            if result.returncode == 0:
                return True, "Success"
            else:
                error_msg = result.stderr
                
                # Check for recoverable errors
                if "CUDA out of memory" in error_msg:
                    logger.warning(f"Frame {frame}: CUDA OOM, retrying with CPU...")
                    # Fallback to CPU render
                    continue
                elif "timeout" in error_msg.lower():
                    logger.warning(f"Frame {frame}: Timeout, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return False, error_msg
        
        except subprocess.TimeoutExpired:
            logger.warning(f"Frame {frame}: Process timeout, attempt {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)
    
    return False, "Max retries exceeded"

# Usage
success, msg = render_with_retry("scene.blend", 42, "/renders/frame_0042.exr")
```

### Dead Letter Queue (DLQ)
```python
class FailedJobQueue:
    def __init__(self, dlq_dir="/renders/dlq"):
        self.dlq_dir = Path(dlq_dir)
        self.dlq_dir.mkdir(exist_ok=True)
    
    def add_failed_job(self, job_id, frame, error_msg):
        """Move failed frame to DLQ"""
        dlq_file = self.dlq_dir / f"{job_id}_frame_{frame:04d}.json"
        
        record = {
            "job_id": job_id,
            "frame": frame,
            "error": error_msg,
            "timestamp": datetime.utcnow().isoformat(),
            "retry_count": 0
        }
        
        with open(dlq_file, 'w') as f:
            json.dump(record, f, indent=2)
    
    def retry_failed_frames(self, job_id):
        """Re-process failed frames"""
        for f in self.dlq_dir.glob(f"{job_id}_*.json"):
            with open(f) as fh:
                record = json.load(fh)
            
            if record["retry_count"] < 3:
                record["retry_count"] += 1
                # Re-queue for rendering
                print(f"Retrying {job_id} frame {record['frame']}")
```

## Performance Metrics

### Render Time Estimation
```python
def estimate_render_time(num_frames, avg_time_per_frame=120):
    """Estimate completion time"""
    total_seconds = num_frames * avg_time_per_frame
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    return f"~{int(hours)}h {int(minutes)}m"

# Track actual timings
render_times = []

for frame in range(1, 251):
    start = time.time()
    subprocess.run(cmd)
    elapsed = time.time() - start
    render_times.append(elapsed)
    
    avg_time = sum(render_times) / len(render_times)
    remaining = (250 - frame) * avg_time
    print(f"Frame {frame}: {elapsed:.1f}s | ETA: {remaining/60:.0f} min")
```

### Throughput Reporting
```python
def generate_report(job_id, queue_file):
    """Generate completion report"""
    with open(queue_file) as f:
        job = json.load(f)
    
    total = job["frames"]["end"] - job["frames"]["start"] + 1
    completed = job["progress"]["completed"]
    failed = job["progress"].get("failed", 0)
    
    start_time = datetime.fromisoformat(job["created_at"])
    end_time = datetime.fromisoformat(job.get("completed_at", datetime.utcnow().isoformat()))
    duration = (end_time - start_time).total_seconds() / 60  # minutes
    
    report = f"""
    RENDER JOB REPORT
    ================
    Job ID: {job_id}
    Total Frames: {total}
    Completed: {completed}
    Failed: {failed}
    Success Rate: {(completed/total)*100:.1f}%
    Duration: {duration:.0f} min
    Avg Frame Time: {duration*60/completed:.1f}s
    Output Directory: {job['output_dir']}
    """
    
    return report
```

## Verification Checklist

- [ ] Queue stores all job metadata (JSON or DB)
- [ ] Progress updates at least once per frame
- [ ] Error log captures stderr from Blender
- [ ] Failed frames detected and retried (max 3 attempts)
- [ ] Dead letter queue stores permanent failures
- [ ] ETA calculated from running average frame time
- [ ] Report generated at job completion
- [ ] Output files checksummed for corruption detection
