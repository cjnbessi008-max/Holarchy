#!/usr/bin/env python3
"""
Holarchy 문서 시스템 검증 스크립트 v3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 90% 완성도 원칙
━━━━━━━━━━━━━━━━━━
- 완성도 100%를 요구하지 않음
- 90% 이상이면 "통과" (나머지 10%는 불확실성 버퍼)
- 개선 제안만 출력, 강제 수정 없음
- 무한 루프 방지, 경직성 완화

📊 스코어 시스템
━━━━━━━━━━━━━━━━━━
- structure: W 구조 완전성 (25%)
- completeness: 내용 채움 정도 (25%)
- resonance: 상위 W와 공명 (25%)
- links: 참조 일관성 (25%)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# 90% 기준
PASS_THRESHOLD = 0.90


@dataclass
class DocumentScore:
    """문서별 완성도 스코어"""
    holon_id: str
    file: str
    structure: float = 0.0      # W 구조 완전성
    completeness: float = 0.0   # 내용 채움 정도 (플레이스홀더 감지)
    resonance: float = 0.0      # 상위 W와 공명
    links: float = 0.0          # 참조 일관성
    
    suggestions: List[str] = field(default_factory=list)
    
    @property
    def total(self) -> float:
        """전체 스코어 (가중 평균)"""
        return (self.structure + self.completeness + self.resonance + self.links) / 4
    
    @property
    def passed(self) -> bool:
        """90% 기준 통과 여부"""
        return self.total >= PASS_THRESHOLD
    
    def to_dict(self) -> dict:
        return {
            "holon_id": self.holon_id,
            "structure": round(self.structure, 2),
            "completeness": round(self.completeness, 2),
            "resonance": round(self.resonance, 2),
            "links": round(self.links, 2),
            "total": round(self.total, 2),
            "passed": self.passed
        }


class HolarchyValidator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.holons: Dict[str, dict] = {}
        self.scores: Dict[str, DocumentScore] = {}
        
    def load_holons(self) -> None:
        """모든 Holon 문서 로드"""
        holons_path = self.base_path / "holons"
        
        for md_file in holons_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
                
            content = md_file.read_text(encoding="utf-8")
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            
            if json_match:
                try:
                    holon = json.loads(json_match.group(1))
                    holon_id = holon.get("holon_id", md_file.stem)
                    holon["_file"] = str(md_file)
                    holon["_content"] = content
                    self.holons[holon_id] = holon
                    self.scores[holon_id] = DocumentScore(holon_id=holon_id, file=str(md_file))
                except json.JSONDecodeError:
                    pass
    
    def score_structure(self) -> None:
        """W 구조 완전성 스코어 (25%)"""
        required_w_fields = {
            "worldview": ["identity", "belief", "value_system"],
            "will": ["drive", "commitment", "non_negotiables"],
            "intention": ["primary", "secondary", "constraints"],
            "goal": ["ultimate", "milestones", "kpi", "okr"],
            "activation": ["triggers", "resonance_check", "drift_detection"]
        }
        
        total_fields = sum(len(fields) + 1 for fields in required_w_fields.values())  # +1 for section itself
        
        for holon_id, holon in self.holons.items():
            w = holon.get("W", {})
            score = self.scores[holon_id]
            
            present_fields = 0
            
            for section, fields in required_w_fields.items():
                if section in w:
                    present_fields += 1
                    for field in fields:
                        if field in w[section]:
                            present_fields += 1
                        else:
                            score.suggestions.append(f"W.{section}.{field} 추가 권장")
                else:
                    score.suggestions.append(f"W.{section} 섹션 추가 권장")
            
            # WXSPERTA will 필드 체크
            slots = ["X", "S", "P", "E", "R", "T", "A"]
            will_present = 0
            for slot in slots:
                if slot in holon and "will" in holon[slot]:
                    will_present += 1
            
            # 구조 스코어 = W 구조 (70%) + WXSPERTA will (30%)
            w_score = present_fields / total_fields if total_fields > 0 else 0
            will_score = will_present / len(slots)
            
            score.structure = w_score * 0.7 + will_score * 0.3
    
    def score_completeness(self) -> None:
        """내용 채움 정도 스코어 - 플레이스홀더 감지 (25%)"""
        placeholder_pattern = re.compile(r'\[.*?\]')  # [...] 패턴
        tbd_pattern = re.compile(r'TBD|TODO|FIXME|XXX', re.IGNORECASE)
        
        for holon_id, holon in self.holons.items():
            score = self.scores[holon_id]
            content = holon.get("_content", "")
            
            # JSON 부분만 추출
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if not json_match:
                score.completeness = 0.0
                continue
            
            json_content = json_match.group(1)
            
            # 플레이스홀더 개수
            placeholders = placeholder_pattern.findall(json_content)
            tbd_matches = tbd_pattern.findall(json_content)
            
            # 총 필드 수 대비 플레이스홀더 비율
            total_strings = len(re.findall(r'"[^"]*"', json_content))
            placeholder_count = len(placeholders) + len(tbd_matches)
            
            if total_strings == 0:
                score.completeness = 0.0
            else:
                # 플레이스홀더가 없으면 100%, 많으면 낮아짐
                placeholder_ratio = placeholder_count / total_strings
                score.completeness = max(0, 1.0 - placeholder_ratio * 3)  # 33% 이상 플레이스홀더면 0점
            
            if placeholder_count > 0:
                score.suggestions.append(f"플레이스홀더 {placeholder_count}개 발견 - 내용 채움 권장")
    
    def score_resonance(self) -> None:
        """상위 W와 공명 스코어 (25%)"""
        critical_keywords = {"시장", "독점", "자동화", "학원", "수학", "ai", "전국"}
        
        for holon_id, holon in self.holons.items():
            score = self.scores[holon_id]
            links = holon.get("links", {})
            parent_id = links.get("parent")
            
            # Root 문서는 100% 공명
            if parent_id is None:
                score.resonance = 1.0
                continue
            
            if parent_id not in self.holons:
                score.resonance = 0.5  # 부모가 없으면 50%
                score.suggestions.append(f"Parent {parent_id}를 찾을 수 없음")
                continue
            
            parent = self.holons[parent_id]
            parent_drive = parent.get("W", {}).get("will", {}).get("drive", "")
            child_drive = holon.get("W", {}).get("will", {}).get("drive", "")
            
            # 키워드 공명 체크
            parent_keywords = set(parent_drive.lower().split()) & critical_keywords
            child_keywords = set(child_drive.lower().split()) & critical_keywords
            
            if not parent_keywords:
                score.resonance = 1.0  # 상위에 키워드 없으면 공명 불필요
            else:
                overlap = parent_keywords & child_keywords
                score.resonance = len(overlap) / len(parent_keywords)
                
                if score.resonance < 0.9:
                    missing = parent_keywords - child_keywords
                    score.suggestions.append(f"상위 키워드 추가 권장: {missing}")
    
    def score_links(self) -> None:
        """참조 일관성 스코어 (25%)"""
        for holon_id, holon in self.holons.items():
            score = self.scores[holon_id]
            links = holon.get("links", {})
            
            checks = []
            
            # Parent-Child 양방향
            parent_id = links.get("parent")
            if parent_id and parent_id in self.holons:
                parent_children = self.holons[parent_id].get("links", {}).get("children", [])
                checks.append(holon_id in parent_children)
                if holon_id not in parent_children:
                    score.suggestions.append(f"Parent {parent_id}의 children에 추가 권장")
            elif parent_id is None:
                checks.append(True)  # Root는 OK
            else:
                checks.append(False)
                score.suggestions.append(f"Parent {parent_id} 존재하지 않음")
            
            # Children 역참조
            for child_id in links.get("children", []):
                if child_id in self.holons:
                    child_parent = self.holons[child_id].get("links", {}).get("parent")
                    checks.append(child_parent == holon_id)
                else:
                    checks.append(False)
                    score.suggestions.append(f"Child {child_id} 존재하지 않음")
            
            # Related 양방향 (가산점)
            for related_id in links.get("related", []):
                if related_id in self.holons:
                    related_links = self.holons[related_id].get("links", {}).get("related", [])
                    if holon_id not in related_links:
                        score.suggestions.append(f"Related {related_id}에 양방향 링크 권장")
            
            if not checks:
                score.links = 1.0
            else:
                score.links = sum(checks) / len(checks)
    
    def run_all_validations(self) -> None:
        """모든 검증 실행"""
        print("=" * 70)
        print("🔍 Holarchy 문서 시스템 검증 v3.0 (90% 완성도 원칙)")
        print("=" * 70)
        print()
        
        print("📂 Holon 문서 로드 중...")
        self.load_holons()
        print(f"   로드된 문서: {len(self.holons)}개")
        print()
        
        print("📊 스코어 계산 중...")
        self.score_structure()
        self.score_completeness()
        self.score_resonance()
        self.score_links()
        print()
        
        # 결과 출력
        passed_docs = []
        needs_improvement = []
        
        print("📋 문서별 스코어:")
        print("-" * 70)
        print(f"{'문서':<30} {'구조':>8} {'완성':>8} {'공명':>8} {'링크':>8} {'총점':>8}")
        print("-" * 70)
        
        for holon_id, score in sorted(self.scores.items()):
            status = "✅" if score.passed else "📝"
            print(f"{status} {holon_id:<28} {score.structure:>7.0%} {score.completeness:>7.0%} "
                  f"{score.resonance:>7.0%} {score.links:>7.0%} {score.total:>7.0%}")
            
            if score.passed:
                passed_docs.append(holon_id)
            else:
                needs_improvement.append((holon_id, score))
        
        print("-" * 70)
        print()
        
        # 개선 제안 (강제 아님)
        if needs_improvement:
            print("💡 개선 제안 (선택사항):")
            print("-" * 70)
            for holon_id, score in needs_improvement:
                print(f"\n📄 {holon_id} (현재 {score.total:.0%})")
                for suggestion in score.suggestions[:5]:  # 최대 5개
                    print(f"   → {suggestion}")
            print()
        
        # 요약
        print("=" * 70)
        avg_score = sum(s.total for s in self.scores.values()) / len(self.scores) if self.scores else 0
        
        if avg_score >= PASS_THRESHOLD:
            print(f"✅ SYSTEM HEALTHY - 평균 완성도 {avg_score:.0%} (기준: {PASS_THRESHOLD:.0%})")
        else:
            print(f"📝 IMPROVEMENT SUGGESTED - 평균 완성도 {avg_score:.0%} (기준: {PASS_THRESHOLD:.0%})")
        
        print("=" * 70)
        print()
        
        # 통계
        print("📊 통계:")
        print(f"   총 문서: {len(self.holons)}개")
        print(f"   통과 (≥90%): {len(passed_docs)}개")
        print(f"   개선 권장 (<90%): {len(needs_improvement)}개")
        print(f"   평균 완성도: {avg_score:.0%}")
        print()
        
        # 90% 원칙 설명
        print("ℹ️  90% 완성도 원칙:")
        print("   • 나머지 10%는 현실 세계 불확실성을 위한 버퍼")
        print("   • 개선 제안은 선택사항 (강제 수정 없음)")
        print("   • 무한 루프 방지, 경직성 완화")


def main():
    script_dir = Path(__file__).parent
    base_path = script_dir.parent
    
    validator = HolarchyValidator(str(base_path))
    validator.run_all_validations()


if __name__ == "__main__":
    main()
