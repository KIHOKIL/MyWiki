"""
Semantic CodeGraph Indexer using libclang / AST
================================================
Extracts semantic code graph (Functions, Calls, Register/Struct member accesses)
from C/C++ source code or compile_commands.json, exporting to JSON-L graph nodes & edges.

Usage:
  python semantic_codegraph_indexer.py --src <path_to_c_file> --out graph.json
  python semantic_codegraph_indexer.py --db compile_commands.json --out graph.json
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Set

# Attempt to import clang.cindex
HAVE_LIBCLANG = False
try:
    import clang.cindex
    from clang.cindex import Index, CursorKind, TypeKind
    HAVE_LIBCLANG = True
except ImportError:
    pass

class SemanticCodeGraphIndexer:
    def __init__(self, compile_flags: List[str] = None):
        self.compile_flags = compile_flags or ["-std=c99", "-I."]
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self._visited_cursors: Set[str] = set()

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "label": label,
                "properties": properties
            }

    def add_edge(self, source: str, target: str, rel_type: str, properties: Dict[str, Any] = None):
        self.edges.append({
            "source": source,
            "target": target,
            "relationship": rel_type,
            "properties": properties or {}
        })

    def parse_with_libclang(self, filepath: str, extra_args: List[str] = None):
        """Parse source file using libclang AST cursor traversal."""
        if not HAVE_LIBCLANG:
            raise RuntimeError("libclang Python binding (`pip install libclang`) is not installed.")

        index = clang.cindex.Index.create()
        args = list(self.compile_flags)
        if extra_args:
            args.extend(extra_args)

        tu = index.parse(filepath, args=args)
        file_node_id = f"file:{os.path.abspath(filepath)}"
        self.add_node(file_node_id, "File", {
            "path": filepath,
            "name": os.path.basename(filepath)
        })

        self._traverse_ast(tu.cursor, file_node_id, current_func=None)

    def _traverse_ast(self, cursor, file_id: str, current_func: str = None):
        # Only inspect cursors in main file (optional: filter system headers)
        if cursor.location.file and os.path.abspath(cursor.location.file.name) != os.path.abspath(file_id.replace("file:", "")):
            # Still traverse children if it's a call or macro inside includes
            pass

        new_func = current_func

        # 1. Function Declarations / Definitions
        if cursor.kind in (clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.CXX_METHOD):
            func_name = cursor.spelling
            if func_name:
                func_id = f"func:{func_name}@{cursor.location.line}"
                self.add_node(func_id, "Function", {
                    "name": func_name,
                    "return_type": cursor.result_type.spelling,
                    "line": cursor.location.line,
                    "file": cursor.location.file.name if cursor.location.file else ""
                })
                self.add_edge(func_id, file_id, "DEFINED_IN")
                new_func = func_id

        # 2. Call Expressions (Function Calls)
        elif cursor.kind == clang.cindex.CursorKind.CALL_EXPR and current_func:
            callee_name = cursor.spelling
            callee_decl = cursor.referenced
            callee_id = f"func:{callee_name}"
            if callee_decl and callee_decl.location.file:
                callee_id = f"func:{callee_name}@{callee_decl.location.line}"
            
            self.add_node(callee_id, "Function", {
                "name": callee_name,
                "is_external": callee_decl is None or not callee_decl.location.file
            })
            self.add_edge(current_func, callee_id, "CALLS", {
                "line": cursor.location.line
            })

        # 3. Struct/Register Member Access (MEMBER_REF_EXPR)
        elif cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR and current_func:
            member_name = cursor.spelling
            parent_type = cursor.type.spelling
            reg_id = f"reg_field:{member_name}"
            
            self.add_node(reg_id, "RegisterField", {
                "name": member_name,
                "type": parent_type,
                "line": cursor.location.line
            })
            self.add_edge(current_func, reg_id, "ACCESSES_REG", {
                "line": cursor.location.line
            })

        for child in cursor.get_children():
            self._traverse_ast(child, file_id, current_func=new_func)

    def parse_mock_simulation(self, filepath: str):
        """Fallback lightweight AST/Regex simulation if libclang runtime binary is missing."""
        file_node_id = f"file:{os.path.abspath(filepath)}"
        self.add_node(file_node_id, "File", {"path": filepath, "name": os.path.basename(filepath)})

        # Simulated parse for demonstration/PoC
        import re
        func_def_pattern = re.compile(r"^\s*(?:static\s+|inline\s+)*[a-zA-Z0-9_*]+\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*\{?", re.M)
        call_pattern = re.compile(r"([a-zA-Z0-9_]+)\s*\(")
        reg_access_pattern = re.compile(r"(?:->|\.)([a-zA-Z0-9_]+)")

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return

        current_func = None
        for line_no, line in enumerate(content.splitlines(), start=1):
            m_func = func_def_pattern.match(line)
            if m_func:
                name = m_func.group(1)
                if name not in ("if", "for", "while", "switch"):
                    current_func = f"func:{name}@{line_no}"
                    self.add_node(current_func, "Function", {"name": name, "line": line_no, "file": filepath})
                    self.add_edge(current_func, file_node_id, "DEFINED_IN")

            if current_func:
                for call in call_pattern.findall(line):
                    if call not in ("if", "for", "while", "switch", "sizeof", "return"):
                        callee_id = f"func:{call}"
                        self.add_node(callee_id, "Function", {"name": call, "is_external": True})
                        self.add_edge(current_func, callee_id, "CALLS", {"line": line_no})
                
                for reg in reg_access_pattern.findall(line):
                    reg_id = f"reg_field:{reg}"
                    self.add_node(reg_id, "RegisterField", {"name": reg, "line": line_no})
                    self.add_edge(current_func, reg_id, "ACCESSES_REG", {"line": line_no})

    def export_graph(self) -> Dict[str, Any]:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "metadata": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges)
            }
        }

    def save_json(self, output_path: str):
        data = self.export_graph()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Graph exported: {len(data['nodes'])} nodes, {len(data['edges'])} edges -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Clang Semantic CodeGraph Indexer")
    parser.add_argument("--src", help="Target C/C++ source file")
    parser.add_argument("--db", help="Path to compile_commands.json")
    parser.add_argument("--out", default="codegraph.json", help="Output graph JSON file")
    args = parser.parse_args()

    indexer = SemanticCodeGraphIndexer()

    if args.src:
        if HAVE_LIBCLANG:
            try:
                indexer.parse_with_libclang(args.src)
            except Exception as e:
                print(f"[Warning] libclang parse failed ({e}), falling back to regex simulation")
                indexer.parse_mock_simulation(args.src)
        else:
            print("[Info] libclang not found. Running AST simulation mode.")
            indexer.parse_mock_simulation(args.src)
    elif args.db and os.path.exists(args.db):
        with open(args.db, "r", encoding="utf-8") as f:
            commands = json.load(f)
        for cmd in commands:
            file = cmd.get("file")
            if file and os.path.exists(file):
                print(f"Indexing {file}...")
                if HAVE_LIBCLANG:
                    indexer.parse_with_libclang(file)
                else:
                    indexer.parse_mock_simulation(file)
    else:
        # Sample self-test
        sample_code = """
        typedef struct {
            volatile unsigned int CTRL;
            volatile unsigned int DATA;
        } PHY_REG_T;

        PHY_REG_T *pPhyReg = (PHY_REG_T*)0x40001000;

        void phy_rf_calibrate(void) {
            pPhyReg->CTRL |= 0x01;
        }

        void phy_init(void) {
            phy_rf_calibrate();
            pPhyReg->DATA = 0xAA;
        }
        """
        temp_src = "sample_phy.c"
        with open(temp_src, "w", encoding="utf-8") as f:
            f.write(sample_code)
        print(f"[Self-Test] Parsing generated sample {temp_src}...")
        indexer.parse_mock_simulation(temp_src)
        if os.path.exists(temp_src):
            os.remove(temp_src)

    indexer.save_json(args.out)

if __name__ == "__main__":
    main()
