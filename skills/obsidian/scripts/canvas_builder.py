#!/usr/bin/env python3
"""
Obsidian Canvas Builder & Automation Tool
Programmatically generates interactive .canvas files with nodes, groups,
chromatic coloring, and directional connections according to Obsidian Canvas JSON spec.
"""
import sys
import os
import json
import uuid
import argparse

class ObsidianCanvas:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def _gen_id(self):
        return uuid.uuid4().hex[:16]

    def add_text_node(self, text, x, y, width=320, height=200, color="5", node_id=None):
        nid = node_id or self._gen_id()
        node = {
            "id": nid,
            "type": "text",
            "text": text,
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
            "color": str(color)
        }
        self.nodes.append(node)
        return nid

    def add_file_node(self, file_path, x, y, width=400, height=350, color="4", node_id=None):
        nid = node_id or self._gen_id()
        node = {
            "id": nid,
            "type": "file",
            "file": file_path,
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
            "color": str(color)
        }
        self.nodes.append(node)
        return nid

    def add_group(self, label, x, y, width, height, color="1", group_id=None):
        gid = group_id or self._gen_id()
        group = {
            "id": gid,
            "type": "group",
            "label": label,
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
            "color": str(color)
        }
        self.nodes.append(group)
        return gid

    def add_edge(self, from_node, to_node, from_side="right", to_side="left", color="5", label=None, edge_id=None):
        eid = edge_id or self._gen_id()
        edge = {
            "id": eid,
            "fromNode": from_node,
            "fromSide": from_side,
            "toNode": to_node,
            "toSide": to_side,
            "color": str(color)
        }
        if label:
            edge["label"] = label
        self.edges.append(edge)
        return eid

    def to_dict(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

    def save(self, filepath):
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"✅ Canvas saved successfully ({len(self.nodes)} nodes, {len(self.edges)} edges): {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Obsidian Canvas Builder CLI")
    parser.add_argument("output", help="Path to output .canvas file")
    parser.add_argument("--demo", action="store_true", help="Generate a demo self-help knowledge map canvas")
    args = parser.parse_args()

    canvas = ObsidianCanvas()
    if args.demo:
        # Group 1: Mindset & Motive
        g1 = canvas.add_group("🔥 Core Motive & Psychological Anchor", 40, 40, 720, 460, color="1")
        n1 = canvas.add_file_node("01_Mindset_Motive/Motive_and_Dignity_Anchor.md", 70, 90, 320, 380, color="1")
        n2 = canvas.add_file_node("01_Mindset_Motive/Cerebellar_Tension_and_Dopamine.md", 410, 90, 320, 380, color="2")
        
        # Group 2: Cognitive & Learning
        g2 = canvas.add_group("🧠 Cognitive Mastery & Focus", 800, 40, 720, 460, color="5")
        n3 = canvas.add_file_node("02_Cognitive_Learning/Oakley_Learning_Framework.md", 830, 90, 320, 380, color="5")
        n4 = canvas.add_file_node("02_Cognitive_Learning/Micro_Sprint_Protocol.md", 1170, 90, 320, 380, color="5")
        
        # Central Edge
        canvas.add_edge(n1, n3, from_side="right", to_side="left", color="1", label="powers focus")
        
        canvas.save(args.output)
    else:
        print("Please specify --demo to generate a demo canvas or use ObsidianCanvas as a Python module.")

if __name__ == "__main__":
    main()
