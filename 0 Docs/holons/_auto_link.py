#!/usr/bin/env python3
"""
자동 양방향 링크 업데이트
- A가 B를 참조하면 B의 related에도 A 추가
- parent-child 관계 자동 동기화
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional


class AutoLinker:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.holons: Dict[str, dict] = {}
        self.holon_files: Dict[str, Path] = {}
        
    def load_holons(self) -> None:
        """모든 Holon 문서 로드"""
        for md_file in self.base_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
                
            content = md_file.read_text(encoding="utf-8")
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            
            if json_match:
                try:
                    holon = json.loads(json_match.group(1))
                    holon_id = holon.get("holon_id", md_file.stem)
                    self.holons[holon_id] = holon
                    self.holon_files[holon_id] = md_file
                except json.JSONDecodeError:
                    pass
    
    def update_holon_file(self, holon_id: str, holon: dict) -> None:
        """Holon 파일의 JSON 부분 업데이트"""
        file_path = self.holon_files.get(holon_id)
        if not file_path:
            return
            
        content = file_path.read_text(encoding="utf-8")
        
        # JSON 부분 찾기
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if not json_match:
            return
        
        # 새 JSON 생성 (예쁘게 포맷)
        new_json = json.dumps(holon, ensure_ascii=False, indent=2)
        
        # 교체
        new_content = content[:json_match.start()] + "```json\n" + new_json + "\n```" + content[json_match.end():]
        
        file_path.write_text(new_content, encoding="utf-8")
    
    def sync_parent_child(self) -> int:
        """Parent-Child 관계 양방향 동기화"""
        changes = 0
        
        for holon_id, holon in self.holons.items():
            links = holon.get("links", {})
            parent_id = links.get("parent")
            
            # Parent가 있으면 Parent의 children에 자신 추가
            if parent_id and parent_id in self.holons:
                parent = self.holons[parent_id]
                parent_links = parent.setdefault("links", {})
                parent_children = parent_links.setdefault("children", [])
                
                if holon_id not in parent_children:
                    parent_children.append(holon_id)
                    self.update_holon_file(parent_id, parent)
                    print(f"  ✅ {parent_id}.children에 {holon_id} 추가")
                    changes += 1
            
            # Children이 있으면 각 Child의 parent를 자신으로 설정
            for child_id in links.get("children", []):
                if child_id in self.holons:
                    child = self.holons[child_id]
                    child_links = child.setdefault("links", {})
                    
                    if child_links.get("parent") != holon_id:
                        child_links["parent"] = holon_id
                        self.update_holon_file(child_id, child)
                        print(f"  ✅ {child_id}.parent를 {holon_id}로 설정")
                        changes += 1
        
        return changes
    
    def sync_related(self) -> int:
        """Related 관계 양방향 동기화"""
        changes = 0
        
        for holon_id, holon in self.holons.items():
            links = holon.get("links", {})
            
            for related_id in links.get("related", []):
                if related_id in self.holons:
                    related = self.holons[related_id]
                    related_links = related.setdefault("links", {})
                    related_related = related_links.setdefault("related", [])
                    
                    if holon_id not in related_related:
                        related_related.append(holon_id)
                        self.update_holon_file(related_id, related)
                        print(f"  ✅ {related_id}.related에 {holon_id} 추가")
                        changes += 1
        
        return changes
    
    def run(self) -> None:
        """전체 동기화 실행"""
        print("=" * 60)
        print("🔗 자동 양방향 링크 업데이트")
        print("=" * 60)
        print()
        
        print("📂 Holon 문서 로드 중...")
        self.load_holons()
        print(f"   로드된 문서: {len(self.holons)}개")
        print()
        
        print("🔄 Parent-Child 동기화...")
        pc_changes = self.sync_parent_child()
        print()
        
        print("🔄 Related 동기화...")
        r_changes = self.sync_related()
        print()
        
        total = pc_changes + r_changes
        print("=" * 60)
        if total > 0:
            print(f"✅ 완료 - {total}개 링크 업데이트")
        else:
            print("✅ 완료 - 모든 링크가 이미 동기화됨")
        print("=" * 60)


def main():
    script_dir = Path(__file__).parent
    linker = AutoLinker(str(script_dir))
    linker.run()


if __name__ == "__main__":
    main()
