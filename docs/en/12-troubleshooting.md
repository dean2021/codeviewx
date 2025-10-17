# Troubleshooting

This document provides comprehensive troubleshooting guidance for common issues encountered when using CodeViewX, covering installation problems, runtime errors, performance issues, and deployment challenges.

## Quick Reference

| Issue Category | Common Symptoms | Quick Fix |
|----------------|----------------|-----------|
| **Installation** | Module not found, permission errors | Use `pip install -e .` or virtual environment |
| **API Issues** | Invalid API key, rate limits | Check ANTHROPIC_API_KEY environment variable |
| **Performance** | Slow processing, memory issues | Increase recursion limit, use parallel processing |
| **File System** | Permission denied, file not found | Check file permissions and paths |
| **Network** | Connection timeouts, SSL errors | Verify internet connection and proxy settings |

## Installation Issues

### Problem: Module Not Found Error

**Symptoms**:
```
ModuleNotFoundError: No module named 'codeviewx'
```

**Causes**:
- CodeViewX not installed or installed in wrong environment
- Virtual environment not activated
- Python path issues

**Solutions**:

#### 1. Install in Development Mode
```bash
# Navigate to project directory
cd /path/to/codeviewx

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

#### 2. Verify Installation
```bash
# Check if module is installed
python -c "import codeviewx; print('Installation successful')"

# Check version
codeviewx --version
```

#### 3. Check Python Path
```python
# Debug Python path issues
import sys
print(sys.path)
```

### Problem: Permission Errors During Installation

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
```

**Solutions**:

#### 1. Use User Installation
```bash
pip install --user -e .
```

#### 2. Use Virtual Environment
```bash
python -m venv ~/.codeviewx_env
source ~/.codeviewx_env/bin/activate
pip install -e .
```

#### 3. Use System Package Manager (Linux)
```bash
# Ubuntu/Debian
sudo apt install python3-pip
sudo pip3 install -e .

# macOS with Homebrew
brew install python3
pip3 install -e .
```

### Problem: ripgrep Not Found

**Symptoms**:
```
rg: command not found
Error: ripgrep (rg) is not installed
```

**Solutions**:

#### Install ripgrep
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt update
sudo apt install ripgrep

# CentOS/RHEL
sudo yum install ripgrep

# Windows with Chocolatey
choco install ripgrep

# Windows with Scoop
scoop install ripgrep

# Manual installation
# Download from https://github.com/BurntSushi/ripgrep/releases
```

#### Verify Installation
```bash
rg --version
```

## API and Authentication Issues

### Problem: Invalid API Key

**Symptoms**:
```
Error: Invalid API key
401 Unauthorized
```

**Solutions**:

#### 1. Set Environment Variable
```bash
# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Add to shell profile for persistence
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $ANTHROPIC_API_KEY
```

#### 2. Check API Key Validity
```bash
# Test API key with curl
curl -X POST https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-3-haiku-20240307",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Hi"}]
  }'
```

#### 3. Use Configuration File
```bash
# Create ~/.anthropic/config
mkdir -p ~/.anthropic
cat > ~/.anthropic/config << EOF
[default]
api_key = your-api-key-here
EOF
```

### Problem: API Rate Limiting

**Symptoms**:
```
429 Too Many Requests
Rate limit exceeded
```

**Solutions**:

#### 1. Reduce Request Frequency
```bash
# Increase recursion limit to reduce API calls
codeviewx --recursion-limit 2000

# Use verbose mode to monitor API usage
codeviewx --verbose
```

#### 2. Upgrade API Plan
- Check your current API limits in Anthropic console
- Consider upgrading to a higher tier plan

#### 3. Implement Caching
```python
# Enable caching in your application
from codeviewx.optimization.cache import PerformanceCache

cache = PerformanceCache()
# Use cached results when available
```

### Problem: Network Connection Issues

**Symptoms**:
```
Connection timeout
SSL verification failed
Network unreachable
```

**Solutions**:

#### 1. Check Internet Connection
```bash
# Test basic connectivity
ping google.com

# Test HTTPS connection
curl -I https://api.anthropic.com
```

#### 2. Configure Proxy
```bash
# Set proxy environment variables
export https_proxy=http://proxy.company.com:8080
export http_proxy=http://proxy.company.com:8080

# Test with proxy
curl -I --proxy $https_proxy https://api.anthropic.com
```

#### 3. Disable SSL Verification (Not Recommended for Production)
```bash
# Only for testing
export PYTHONHTTPSVERIFY=0
```

## Performance Issues

### Problem: Slow Processing

**Symptoms**:
- Documentation generation takes very long time
- Progress seems stuck
- High CPU usage for extended periods

**Diagnostic Steps**:

#### 1. Monitor Progress with Verbose Mode
```bash
codeviewx --verbose --working-dir /path/to/project
```

#### 2. Check System Resources
```bash
# Monitor CPU and memory
top -p $(pgrep -f codeviewx)

# Check disk I/O
iotop

# Monitor network usage
nethogs
```

#### 3. Analyze Project Size
```bash
# Count files in project
find /path/to/project -type f | wc -l

# Find large files
find /path/to/project -type f -size +1M -exec ls -lh {} \;

# Check for ignored directories
ls -la /path/to/project/.git
ls -la /path/to/project/node_modules
```

**Solutions**:

#### 1. Optimize Configuration
```bash
# Increase recursion limit for complex projects
codeviewx --recursion-limit 3000

# Use parallel processing
codeviewx --max-workers 32
```

#### 2. Segment Large Projects
```python
# Split large project into smaller chunks
from codeviewx.optimization.scalability import ProjectSegmenter

segmenter = ProjectSegmenter(max_files_per_segment=500)
segments = segmenter.segment_project("/path/to/large/project")

# Process each segment separately
for segment in segments:
    codeviewx --working-dir segment.path --output-dir f"docs_segment_{segment.id}"
```

#### 3. Enable Caching
```bash
# Create cache directory
mkdir -p .codeviewx_cache

# Use cache in your script
export CODEVIEWX_CACHE_DIR=".codeviewx_cache"
```

### Problem: High Memory Usage

**Symptoms**:
- System becomes unresponsive
- Out of memory errors
- Swap usage increases

**Diagnostic Steps**:

#### 1. Monitor Memory Usage
```bash
# Check memory usage
ps aux | grep codeviewx

# Monitor in real-time
watch -n 1 'ps aux | grep codeviewx | grep -v grep'

# Check system memory
free -h
```

#### 2. Profile Memory Usage
```python
# memory_profiler.py
import psutil
import time
from codeviewx import generate_docs

def monitor_memory():
    process = psutil.Process()
    while True:
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"Memory: {memory_mb:.1f}MB")
        time.sleep(5)

# Run in background while processing
import threading
monitor_thread = threading.Thread(target=monitor_memory)
monitor_thread.daemon = True
monitor_thread.start()

generate_docs(working_directory="/path/to/project")
```

**Solutions**:

#### 1. Reduce Batch Size
```python
# Reduce concurrent operations
from codeviewx.optimization.parallel_processor import ParallelProcessor

processor = ParallelProcessor(max_workers=4)  # Reduce from default 16
```

#### 2. Enable Garbage Collection
```python
import gc
import time

def process_with_gc():
    # Your processing code
    pass
    
    # Force garbage collection
    gc.collect()
```

#### 3. Use Streaming Processing
```bash
# Process files in smaller batches
codeviewx --batch-size 25  # Default is 50
```

## File System Issues

### Problem: Permission Denied

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
Access denied
```

**Solutions**:

#### 1. Check File Permissions
```bash
# Check directory permissions
ls -la /path/to/project

# Check specific file
ls -la /path/to/project/file.py

# Change permissions if needed
chmod 644 /path/to/project/file.py
chmod 755 /path/to/project/directory
```

#### 2. Run with Correct User
```bash
# Check current user
whoami

# Run as different user if needed
sudo -u username codeviewx --working-dir /path/to/project
```

#### 3. Use Writable Directory
```bash
# Create writable output directory
mkdir -p ~/codeviewx_output
chmod 755 ~/codeviewx_output

codeviewx --output-dir ~/codeviewx_output
```

### Problem: File Not Found

**Symptoms**:
```
FileNotFoundError: [Errno 2] No such file or directory
File not found: /path/to/file
```

**Solutions**:

#### 1. Verify File Exists
```bash
# Check if file exists
ls -la /path/to/file

# Search for file
find /path/to/project -name "filename.py"
```

#### 2. Check Working Directory
```bash
# Verify working directory
pwd

# Use absolute paths
codeviewx --working-dir /absolute/path/to/project
```

#### 3. Check Symbolic Links
```bash
# Check for broken symbolic links
find -L . -type l
```

### Problem: Disk Space Issues

**Symptoms**:
```
OSError: [Errno 28] No space left on device
Disk quota exceeded
```

**Solutions**:

#### 1. Check Disk Space
```bash
# Check disk usage
df -h

# Check directory size
du -sh /path/to/project

# Find large files
find /path/to/project -type f -size +100M -exec ls -lh {} \;
```

#### 2. Clean Up Space
```bash
# Remove cache files
rm -rf .codeviewx_cache
rm -rf __pycache__
rm -rf .pytest_cache

# Clean old documentation
rm -rf old_docs/

# Clean system cache
pip cache purge
```

#### 3. Use External Storage
```bash
# Use different output directory
codeviewx --output-dir /external/drive/docs

# Mount additional storage
sudo mount /dev/sdb1 /mnt/external
codeviewx --output-dir /mnt/external/docs
```

## CLI Issues

### Problem: Invalid Command Arguments

**Symptoms**:
```
error: unrecognized arguments: --invalid-option
usage: codeviewx [-h] [OPTIONS]
```

**Solutions**:

#### 1. Check Help
```bash
codeviewx --help
```

#### 2. Verify Command Syntax
```bash
# Correct syntax
codeviewx --working-dir /path/to/project --output-dir docs

# Common mistakes to avoid
# Wrong: codeviewx -working-dir /path  # Missing double dash
# Wrong: codeviewx --working_dir /path  # Wrong separator
```

#### 3. Check Argument Values
```bash
# Valid language options
codeviewx --language English
codeviewx --language Chinese

# Invalid
codeviewx --language invalid_lang
```

### Problem: CLI Crashes or Hangs

**Symptoms**:
- CLI becomes unresponsive
- Process hangs indefinitely
- No output for long periods

**Diagnostic Steps**:

#### 1. Check Process Status
```bash
# Check if process is running
ps aux | grep codeviewx

# Check process details
ps -f -p $(pgrep -f codeviewx)

# Monitor process
top -p $(pgrep -f codeviewx)
```

#### 2. Enable Debug Mode
```bash
# Run with maximum verbosity
codeviewx --verbose --working-dir /path/to/project

# Enable Python debugging
PYTHONDEBUG=1 codeviewx --verbose
```

#### 3. Check for Deadlocks
```bash
# Send signal to process for debugging
kill -USR1 $(pgrep -f codeviewx)

# Generate core dump for analysis
ulimit -c unlimited
codeviewx --working-dir /path/to/project
# If it crashes, analyze core dump
gdb python core.$(pgrep -f codeviewx)
```

**Solutions**:

#### 1. Increase Timeout
```bash
# Set longer timeout for large projects
export CODEVIEWX_TIMEOUT=600  # 10 minutes
```

#### 2. Use Smaller Recursion Limit
```bash
# Reduce recursion limit to prevent infinite loops
codeviewx --recursion-limit 500
```

#### 3. Kill and Restart
```bash
# Kill hanging process
kill -9 $(pgrep -f codeviewx)

# Restart with different configuration
codeviewx --max-workers 4 --recursion-limit 1000
```

## Web Server Issues

### Problem: Server Won't Start

**Symptoms**:
```
Address already in use
Port 5000 is already in use
Permission denied
```

**Solutions**:

#### 1. Check Port Availability
```bash
# Check if port is in use
netstat -tulpn | grep 5000
lsof -i :5000

# Kill process using port
kill -9 $(lsof -t -i:5000)
```

#### 2. Use Different Port
```bash
# Start server on different port
codeviewx --serve --port 8080
```

#### 3. Check Permissions
```bash
# Check if you can bind to port < 1024
sudo codeviewx --serve --port 80

# Or use port forwarding
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
```

### Problem: Can't Access Web Interface

**Symptoms**:
- Connection refused
- Page not found
- 404 errors

**Solutions**:

#### 1. Check Server Status
```bash
# Check if server is running
curl -I http://localhost:5000

# Check server logs
docker logs codeviewx-container
```

#### 2. Verify Firewall Settings
```bash
# Check firewall rules
sudo ufw status
sudo iptables -L

# Allow port through firewall
sudo ufw allow 5000
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```

#### 3. Check Network Configuration
```bash
# Bind to all interfaces
codeviewx --serve --host 0.0.0.0

# Check network interfaces
ip addr show
ifconfig
```

## Docker Issues

### Problem: Container Won't Start

**Symptoms**:
```
docker: Error response from daemon: ...
Container exited with code 1
```

**Solutions**:

#### 1. Check Container Logs
```bash
# Check container logs
docker logs codeviewx-container

# Follow logs in real-time
docker logs -f codeviewx-container
```

#### 2. Debug Container
```bash
# Run container interactively
docker run -it --rm codeviewx:latest /bin/bash

# Check container configuration
docker inspect codeviewx-container
```

#### 3. Check Resource Limits
```bash
# Check available memory
docker system df
docker system prune

# Increase memory limit
docker run --memory=2g codeviewx:latest
```

### Problem: Build Failures

**Symptoms**:
```
failed to solve: process "/bin/sh -c pip install" did not complete successfully
No matching distribution found
```

**Solutions**:

#### 1. Update Base Image
```dockerfile
# Use newer base image
FROM python:3.11-slim
```

#### 2. Clear Package Cache
```dockerfile
# Clear pip cache
RUN pip install --no-cache-dir -r requirements.txt
```

#### 3. Use Multi-stage Build
```dockerfile
# Multi-stage build to reduce size
FROM python:3.11-slim as builder
# ... build steps ...

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

## Kubernetes Issues

### Problem: Pod Crashes

**Symptoms**:
```
Pod has a CrashLoopBackOff
Container terminated with error
```

**Solutions**:

#### 1. Check Pod Status
```bash
# Get pod details
kubectl get pods -n codeviewx
kubectl describe pod <pod-name> -n codeviewx

# Check pod logs
kubectl logs <pod-name> -n codeviewx
kubectl logs <pod-name> -n codeviewx --previous
```

#### 2. Debug Pod
```bash
# Execute command in pod
kubectl exec -it <pod-name> -n codeviewx -- /bin/bash

# Check pod events
kubectl get events -n codeviewx --sort-by=.metadata.creationTimestamp
```

#### 3. Check Resource Limits
```bash
# Check resource usage
kubectl top pods -n codeviewx

# Describe pod for resource info
kubectl describe pod <pod-name> -n codeviewx
```

### Problem: Service Not Accessible

**Symptoms**:
- Connection timeout
- Service unavailable
- 503 errors

**Solutions**:

#### 1. Check Service Status
```bash
# Check service
kubectl get svc -n codeviewx
kubectl describe svc codeviewx-service -n codeviewx

# Check endpoints
kubectl get endpoints -n codeviewx
```

#### 2. Port Forward for Debugging
```bash
# Port forward to local machine
kubectl port-forward service/codeviewx-service 5000:80 -n codeviewx
```

#### 3. Check Network Policies
```bash
# Check network policies
kubectl get networkpolicies -n codeviewx
kubectl describe networkpolicy codeviewx-netpol -n codeviewx
```

## Getting Help

### Collect Debug Information

When seeking help, collect the following information:

```bash
# System information
uname -a
python --version
pip list | grep codeviewx
rg --version

# CodeViewX configuration
echo $ANTHROPIC_API_KEY | head -c 10  # Show first 10 chars only
codeviewx --version

# Error reproduction
codeviewx --working-dir /path/to/problematic/project --verbose 2>&1 | tee debug.log
```

### Community Support

1. **GitHub Issues**: Report bugs at https://github.com/dean2021/codeviewx/issues
2. **Discussions**: Join community discussions at https://github.com/dean2021/codeviewx/discussions
3. **Documentation**: Check latest documentation at https://github.com/dean2021/codeviewx/tree/main/docs

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Run command: `codeviewx ...`
2. Observe error
3. See result

## Expected Behavior
What should have happened

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.11.0]
- CodeViewX: [e.g., 0.2.0]
- ripgrep: [e.g., 14.0.3]

## Additional Context
Any other relevant information
```

This comprehensive troubleshooting guide should help resolve most common issues encountered when using CodeViewX. For issues not covered here, please refer to the community support channels.