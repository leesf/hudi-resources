#!/usr/bin/env python3
"""
Link Validator for README.md
This script checks all links in the README to identify broken or slow-loading links.
"""

import re
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

def extract_links(readme_path):
    """
    Extract all URLs from README.md
    
    Args:
        readme_path: Path to README.md
    
    Returns:
        List of (line_number, url) tuples
    """
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    links = []
    # Improved regex pattern to handle URLs in markdown links and parentheses
    url_pattern = r'https?://[^\s\)\]"<>]+'
    
    for i, line in enumerate(lines, 1):
        urls = re.findall(url_pattern, line)
        for url in urls:
            # Clean up any trailing punctuation that might have been captured
            url = url.rstrip('.,;:!?')
            links.append((i, url))
    
    return links

def check_link(line_num, url, timeout=10):
    """
    Check if a link is accessible and measure response time.
    
    Args:
        line_num: Line number in README
        url: URL to check
        timeout: Request timeout in seconds
    
    Returns:
        Dict with check results
    """
    result = {
        'line': line_num,
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'response_time': None,
        'error': None
    }
    
    # Add User-Agent header to avoid being blocked by servers
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0; +https://github.com/leesf/hudi-resources)'
    }
    
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True, headers=headers)
        result['status_code'] = response.status_code
        result['response_time'] = response.elapsed.total_seconds()
        
        if response.status_code == 200:
            result['status'] = 'ok'
        elif response.status_code >= 400:
            result['status'] = 'broken'
        else:
            result['status'] = 'redirected'
            
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = f'Timeout after {timeout}s'
    except requests.exceptions.RequestException as e:
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result

def main():
    """Main function to validate all links."""
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / 'README.md'
    
    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}")
        return 1
    
    print("Extracting links from README.md...")
    links = extract_links(readme_path)
    print(f"Found {len(links)} links to check.\n")
    
    print("Checking links (this may take a while)...")
    print("-" * 80)
    
    results = {
        'ok': [],
        'broken': [],
        'timeout': [],
        'error': [],
        'slow': []
    }
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_link, line, url): (line, url) 
                  for line, url in links}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            
            if result['status'] == 'ok':
                results['ok'].append(result)
                if result['response_time'] and result['response_time'] > 3.0:
                    results['slow'].append(result)
                    print(f"[{i}/{len(links)}] ⚠️  SLOW (Line {result['line']}): {result['url'][:60]}... ({result['response_time']:.2f}s)")
                else:
                    print(f"[{i}/{len(links)}] ✓ OK (Line {result['line']}): {result['url'][:60]}...")
            elif result['status'] == 'broken':
                results['broken'].append(result)
                print(f"[{i}/{len(links)}] ✗ BROKEN (Line {result['line']}): {result['url'][:60]}... (Status: {result['status_code']})")
            elif result['status'] == 'timeout':
                results['timeout'].append(result)
                print(f"[{i}/{len(links)}] ⏱️  TIMEOUT (Line {result['line']}): {result['url'][:60]}...")
            else:
                results['error'].append(result)
                print(f"[{i}/{len(links)}] ❌ ERROR (Line {result['line']}): {result['url'][:60]}...")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total links: {len(links)}")
    print(f"✓ Working: {len(results['ok'])}")
    print(f"⚠️  Slow (>3s): {len(results['slow'])}")
    print(f"⏱️  Timeout: {len(results['timeout'])}")
    print(f"✗ Broken: {len(results['broken'])}")
    print(f"❌ Errors: {len(results['error'])}")
    
    if results['broken']:
        print("\n" + "-" * 80)
        print("BROKEN LINKS:")
        for r in results['broken']:
            print(f"  Line {r['line']}: {r['url']} (Status: {r['status_code']})")
    
    if results['slow']:
        print("\n" + "-" * 80)
        print("SLOW LINKS (>3s):")
        for r in results['slow']:
            print(f"  Line {r['line']}: {r['url']} ({r['response_time']:.2f}s)")
    
    return 1 if (results['broken'] or results['timeout'] or results['error']) else 0

if __name__ == '__main__':
    exit(main())
