#!/usr/bin/env python3
"""
Weaviate Statistics and Diagnostic Tool
Shows what's actually indexed in Weaviate to help debug search issues.
Works on both macOS and Linux.
"""
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from store.weaviate_client import WeaviateClient
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install: pip install rich")
    sys.exit(1)

console = Console()

def get_weaviate_stats():
    """Get comprehensive statistics from Weaviate."""
    try:
        wc = WeaviateClient(ensure_schema=False)
        client = wc._client
        
        # All artifact classes
        classes = [
            'DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm',
            'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
            'GwtEndpoint', 'JsArtifact'
        ]
        
        stats = {
            'classes': {},
            'projects': Counter(),
            'total_objects': 0,
            'projects_by_class': defaultdict(Counter),
            'sample_paths': defaultdict(list)
        }
        
        console.print("\n[bold blue]Connecting to Weaviate...[/bold blue]")
        
        for class_name in classes:
            try:
                # Check if class exists first
                if not client.schema.exists(class_name):
                    console.print(f"[dim]Class {class_name} does not exist, skipping...[/dim]")
                    continue
                
                # Get all objects (limit to 10000 for better coverage)
                # Use aggregate query to get total count first
                try:
                    agg_res = client.query.aggregate(class_name).with_meta_count().do()
                    total_count = agg_res.get('data', {}).get('Aggregate', {}).get(class_name, [{}])[0].get('meta', {}).get('count', 0)
                    console.print(f"[dim]Class {class_name}: {total_count} total objects[/dim]")
                except:
                    total_count = 0
                
                # Get sample objects using data_object.get (more reliable than query.get without search)
                hits = []
                try:
                    # Use data_object.get which is more reliable for retrieving objects
                    # This works even when query.get() without search method fails
                    res = client.data_object.get(class_name=class_name, limit=10000)
                    if res and 'objects' in res:
                        # Convert to same format as query.get results
                        for obj in res['objects']:
                            props = obj.get('properties', {})
                            # Add id for consistency
                            props['_id'] = obj.get('id')
                            hits.append(props)
                        console.print(f"[dim]  Retrieved {len(hits)} objects using data_object.get[/dim]")
                    else:
                        console.print(f"[yellow]  No objects returned from data_object.get for {class_name}[/yellow]")
                except Exception as e:
                    console.print(f"[red]  Failed to get objects for {class_name}: {e}[/red]")
                    import traceback
                    console.print(f"[dim]{traceback.format_exc()}[/dim]")
                    hits = []
                
                if hits:
                    class_stats = {
                        'count': len(hits),
                        'projects': Counter(),
                        'sample_paths': []
                    }
                    
                    for hit in hits:
                        if isinstance(hit, dict):
                            project = hit.get('project', 'NO_PROJECT')
                            path = hit.get('path', 'Unknown')
                            
                            stats['projects'][project] += 1
                            class_stats['projects'][project] += 1
                            stats['projects_by_class'][class_name][project] += 1
                            
                            if len(class_stats['sample_paths']) < 3:
                                class_stats['sample_paths'].append(path)
                    
                    stats['classes'][class_name] = class_stats
                    stats['total_objects'] += len(hits)
                    
            except Exception as e:
                console.print(f"[yellow]Warning: Could not query {class_name}: {e}[/yellow]")
        
        return stats
        
    except Exception as e:
        console.print(f"[bold red]Error connecting to Weaviate: {e}[/bold red]")
        return None

def display_stats(stats: Dict[str, Any]):
    """Display statistics in a formatted way."""
    if not stats:
        return
    
    # Overall summary
    console.print("\n" + "=" * 80)
    console.print("[bold green]WEAVIATE STATISTICS[/bold green]")
    console.print("=" * 80)
    
    # Total objects
    console.print(f"\n[bold]Total Objects Indexed:[/bold] {stats['total_objects']}")
    
    # By class
    console.print("\n[bold]Objects by Class:[/bold]")
    class_table = Table(box=box.SIMPLE)
    class_table.add_column("Class", style="cyan")
    class_table.add_column("Count", style="green", justify="right")
    class_table.add_column("Projects", style="yellow", justify="right")
    
    for class_name, class_stats in sorted(stats['classes'].items()):
        class_table.add_row(
            class_name,
            str(class_stats['count']),
            str(len(class_stats['projects']))
        )
    
    console.print(class_table)
    
    # Projects overview
    console.print("\n[bold]Projects Overview:[/bold]")
    project_table = Table(box=box.SIMPLE)
    project_table.add_column("Project", style="cyan")
    project_table.add_column("Total Objects", style="green", justify="right")
    
    for project, count in stats['projects'].most_common(30):
        project_table.add_row(project, str(count))
    
    console.print(project_table)
    
    # Projects by class
    console.print("\n[bold]Projects by Class (Top 10 projects per class):[/bold]")
    for class_name in sorted(stats['classes'].keys()):
        class_stats = stats['classes'][class_name]
        if class_stats['projects']:
            console.print(f"\n[cyan]{class_name}:[/cyan]")
            class_proj_table = Table(box=box.SIMPLE, show_header=False)
            class_proj_table.add_column("Project", style="yellow")
            class_proj_table.add_column("Count", style="green", justify="right")
            
            for project, count in class_stats['projects'].most_common(10):
                class_proj_table.add_row(project, str(count))
            
            console.print(class_proj_table)
    
    # Sample paths
    console.print("\n[bold]Sample Paths by Class:[/bold]")
    for class_name in sorted(stats['classes'].keys()):
        class_stats = stats['classes'][class_name]
        if class_stats['sample_paths']:
            console.print(f"\n[cyan]{class_name}:[/cyan]")
            for path in class_stats['sample_paths']:
                console.print(f"  • {path[:100]}")
    
    # Search test
    console.print("\n" + "=" * 80)
    console.print("[bold]Search Test Results:[/bold]")
    console.print("=" * 80)
    
    # Test searches for top projects
    wc = WeaviateClient(ensure_schema=False)
    top_projects = [p for p, _ in stats['projects'].most_common(5)]
    
    for project in top_projects:
        console.print(f"\n[cyan]Testing search for project: {project}[/cyan]")
        try:
            results = wc.search_artifacts('DaoCall', 'dao', project=project, limit=3)
            if results:
                console.print(f"  ✓ Found {len(results)} results")
                for r in results[:2]:
                    console.print(f"    • {r.get('path', 'Unknown')[:80]}")
            else:
                console.print(f"  ✗ No results found")
        except Exception as e:
            console.print(f"  ✗ Error: {e}")

def main():
    """Main function."""
    console.print(Panel.fit(
        "[bold blue]Weaviate Statistics Tool[/bold blue]\n"
        "Analyzing what's indexed in Weaviate",
        border_style="blue"
    ))
    
    stats = get_weaviate_stats()
    
    if stats:
        display_stats(stats)
        
        # Summary panel
        console.print("\n" + "=" * 80)
        console.print(Panel.fit(
            f"[bold green]Summary[/bold green]\n\n"
            f"Total Objects: {stats['total_objects']}\n"
            f"Classes: {len(stats['classes'])}\n"
            f"Projects: {len(stats['projects'])}\n\n"
            f"Top 5 Projects:\n" + 
            "\n".join([f"  • {p}: {c}" for p, c in stats['projects'].most_common(5)]),
            title="Statistics",
            border_style="green"
        ))
    else:
        console.print("[bold red]Failed to retrieve statistics from Weaviate[/bold red]")
        sys.exit(1)

if __name__ == '__main__':
    main()

