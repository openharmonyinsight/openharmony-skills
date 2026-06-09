#!/usr/bin/env python3

import os
import sys
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from xml.etree.ElementTree import ET


def parse_code_coverage_html(html_path):
    if not os.path.exists(html_path):
        print(f"Error: Code coverage html not found: {html_path}", file=sys.stderr)
        return None
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'lxml')

        result = {}

        for metric in ["Lines", "Functions", "Branches"]:
            metric_cell = soup.find('td', class_='headerItem', string=metric)
            if not metric_cell:
                print(f"Warning: {metric} metric not found in html report", file=sys.stderr)
                result[metric.lower()] = {"hit":0, "total":0, "coverage": "0.0%"}
                continue

            row = metric_cell.parent
            if not row:
                print(f"Warning: {metric} row not found", file=sys.stderr)
                result[metric.lower()] = {"hit":0, "total":0, "coverage": "0.0%"}
                continue                

            cell = row.find_all('td', class_='headerCovTableEntry')
            if len(cell) < 3:
                print(f"Warning: {metric} has insufficient data cells", file=sys.stderr)
                result[metric.lower()] = {"hit":0, "total":0, "coverage": "0.0%"}
                continue   

            hit = int(cells[0].get_text().strip())
            total = int(cells[1].get_text().strip())
            coverage = cells[2].get_text().strip()

            result[metric.lower()] = {
                "hit": hit,
                "total": total,
                "coverage": coverage
            }

        return result
    
    except Exception as e:
        print(f"error parsing code coverage html: {e}", file=sys.stderr)
        return None


def parse_interface_coverage_xml(xml_path):
    if not os.path.exists(xml_path):
        print(f"Error: interface coverage xml file not found: {xml_path}", file=sys.stderr)
        return None
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        subsystems = []
        summary_coverage = None

        for subsystem in root.findall('.//item'):
            name = subsystem.get('subsystem_name')
            function_count = subsystem.get('function_count')
            coverage_value = subsystem.get('coverage_value')

            if name and function_count and coverage_value:
                subsystems.append({
                    "name": name,
                    "function_count": int(function_count),
                    "coverage": coverage_value
                })

            if name =="Summary":
                summary_coverage = coverage_value
            
            return {
                "subsystems": subsystems,
                "summary": {"coverage": summary_coverage}
            }
        
    except Exception as e:
        print(f"error parsing interface coverage html: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description='Parse coverage report files')
    parser.add_argument('--output_path', required=True, help='Output path of coverage reports')
    parser.add_argument('--report_type', choices=['all', 'code', 'interface'],  default='all', help='Report type to parse (default: all)')
    
    args = parser.parse_args()
    
    output_path = args.output_path
    result = {}
    
    if args.report_type in ["code", "all"]:
        code_html_path = os.path.join(output_path, "code_coverage", "index.html")
        code_coverage = parse_code_coverage_html(code_html_path)
        result["code_coverage"] = code_coverage
    
    if args.report_type in ["interface", "all"]:
        interface_xml_path = os.path.join(output_path, "interface_coverage", "coverage", "interface_kits", "ohos_interfaceCoverage.xml")
        interface_coverage = parse_interface_coverage_xml(interface_xml_path)
        result["interface_coverage"] = interface_coverage

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())