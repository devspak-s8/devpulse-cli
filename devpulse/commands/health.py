import typer
import psutil
from datetime import datetime

app = typer.Typer(help="System health monitoring")


@app.command()
def check(
    service: str = typer.Option("all", "--service", "-s", help="Service to check (all, cpu, memory, disk, processes)")
):
    """Check system health status."""
    typer.echo(f"🏥 Checking health: {service}\n")
    
    if service in ["all", "cpu"]:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        status = "✅" if cpu_percent < 80 else "⚠️"
        typer.echo(f"{status} CPU Usage: {cpu_percent}%")
    
    if service in ["all", "memory"]:
        memory = psutil.virtual_memory()
        status = "✅" if memory.percent < 80 else "⚠️"
        typer.echo(f"{status} Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)")
    
    if service in ["all", "disk"]:
        disk = psutil.disk_usage('/')
        status = "✅" if disk.percent < 90 else "⚠️"
        typer.echo(f"{status} Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
    
    if service in ["all", "processes"]:
        process_count = len(psutil.pids())
        typer.echo(f"📊 Active Processes: {process_count}")
    
    typer.echo("\n✅ Health check complete!")


@app.command()
def report(
    format: str = typer.Option("console", "--format", "-f", help="Report format (console, json)")
):
    """Generate comprehensive health report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get system info once
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    if format == "console":
        typer.echo("\n" + "="*50)
        typer.echo("📊 SYSTEM HEALTH REPORT")
        typer.echo("="*50)
        typer.echo(f"Generated: {timestamp}\n")
        
        # CPU Info
        typer.echo(f"🖥️  CPU Information:")
        typer.echo(f"   Cores: {cpu_count}")
        typer.echo(f"   Usage: {cpu_percent}%")
        typer.echo(f"   Frequency: {psutil.cpu_freq().current:.0f} MHz\n")
        
        # Memory Info
        typer.echo(f"🧠 Memory Information:")
        typer.echo(f"   Total: {memory.total // (1024**3)}GB")
        typer.echo(f"   Used: {memory.used // (1024**3)}GB")
        typer.echo(f"   Available: {memory.available // (1024**3)}GB")
        typer.echo(f"   Usage: {memory.percent}%\n")
        
        # Disk Info
        typer.echo(f"💾 Disk Information:")
        typer.echo(f"   Total: {disk.total // (1024**3)}GB")
        typer.echo(f"   Used: {disk.used // (1024**3)}GB")
        typer.echo(f"   Free: {disk.free // (1024**3)}GB")
        typer.echo(f"   Usage: {disk.percent}%\n")
        
        # System Info
        typer.echo(f"📋 System Information:")
        typer.echo(f"   Platform: {psutil.os.name}")
        typer.echo(f"   Processes: {len(psutil.pids())}")
        typer.echo(f"   Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")
        
        typer.echo("\n" + "="*50)
    
    elif format == "json":
        import json
        health_data = {
            "timestamp": timestamp,
            "cpu": {
                "percent": cpu_percent,
                "cores": cpu_count,
                "frequency_mhz": psutil.cpu_freq().current
            },
            "memory": {
                "total_gb": memory.total // (1024**3),
                "used_gb": memory.used // (1024**3),
                "available_gb": memory.available // (1024**3),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": disk.total // (1024**3),
                "used_gb": disk.used // (1024**3),
                "free_gb": disk.free // (1024**3),
                "percent": disk.percent
            },
            "processes": len(psutil.pids())
        }
        typer.echo(json.dumps(health_data, indent=2))


@app.command()
def processes(
    top: int = typer.Option(10, "--top", "-t", help="Show top N processes by memory usage"),
    sort_by: str = typer.Option("memory", "--sort", "-s", help="Sort by (memory, cpu, name)")
):
    """List top processes by resource usage."""
    typer.echo(f"\n📋 Top {top} Processes (by {sort_by}):\n")
    
    processes_list = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent'])
            processes_list.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by selected metric
    if sort_by == "memory":
        processes_list.sort(key=lambda x: x['memory_percent'], reverse=True)
    elif sort_by == "cpu":
        processes_list.sort(key=lambda x: x['cpu_percent'], reverse=True)
    else:
        processes_list.sort(key=lambda x: x['name'])
    
    # Display top N
    typer.echo(f"{'PID':<8} {'Name':<30} {'Memory %':<12} {'CPU %':<10}")
    typer.echo("-" * 60)
    for proc in processes_list[:top]:
        name = proc['name'][:29]
        typer.echo(f"{proc['pid']:<8} {name:<30} {proc['memory_percent']:<12.2f} {proc['cpu_percent']:<10.2f}")
    
    typer.echo()


@app.command()
def alert(
    cpu_threshold: int = typer.Option(80, "--cpu", "-c", help="CPU threshold %"),
    memory_threshold: int = typer.Option(80, "--memory", "-m", help="Memory threshold %"),
    disk_threshold: int = typer.Option(90, "--disk", "-d", help="Disk threshold %")
):
    """Check if system metrics exceed thresholds and alert."""
    typer.echo("🚨 Checking for alerts...\n")
    
    alerts = []
    
    cpu_percent = psutil.cpu_percent(interval=0.1)
    if cpu_percent > cpu_threshold:
        alerts.append(f"⚠️  CPU ALERT: Usage is {cpu_percent}% (threshold: {cpu_threshold}%)")
    
    memory = psutil.virtual_memory()
    if memory.percent > memory_threshold:
        alerts.append(f"⚠️  MEMORY ALERT: Usage is {memory.percent}% (threshold: {memory_threshold}%)")
    
    disk = psutil.disk_usage('/')
    if disk.percent > disk_threshold:
        alerts.append(f"⚠️  DISK ALERT: Usage is {disk.percent}% (threshold: {disk_threshold}%)")
    
    if alerts:
        for alert_msg in alerts:
            typer.echo(alert_msg)
    else:
        typer.echo("✅ No alerts - all metrics within thresholds!")
