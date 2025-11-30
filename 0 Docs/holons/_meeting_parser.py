#!/usr/bin/env python3
"""
🔥 회의록 자동 파싱 & Holon 생성기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

기능:
- 회의록 텍스트를 분석하여 자동으로 Holon 문서 생성
- 내용 기반으로 적절한 parent 자동 선택
- Decision, Task 항목 자동 추출
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class MeetingParser:
    """회의록 파싱 및 Holon 자동 생성"""
    
    # 키워드 → parent 매핑
    KEYWORD_PARENT_MAP = {
        # 제품/기술 관련
        "api": "hte-doc-005",
        "시스템": "hte-doc-002",
        "아키텍처": "hte-doc-002",
        "제품": "hte-doc-002",
        "기능": "hte-doc-002",
        "개발": "hte-doc-002",
        
        # 조직 관련
        "조직": "hte-doc-001",
        "팀": "hte-doc-001",
        "인사": "hte-doc-001",
        "채용": "hte-doc-001",
        
        # 전략 관련
        "전략": "hte-doc-003",
        "운영": "hte-doc-003",
        "프로세스": "hte-doc-003",
        
        # 투자/재무
        "투자": "hte-doc-004",
        "재무": "hte-doc-004",
        "비용": "hte-doc-004",
        "예산": "hte-doc-004",
        
        # AI/PM
        "ai": "strategy-2025-001",
        "pm": "strategy-2025-001",
        "자동화": "strategy-2025-001",
        "학생": "strategy-2025-001",
        "진단": "feature-2025-001",
        "시선": "feature-2025-002",
        "집중도": "feature-2025-002",
    }
    
    # Decision/Task 추출 패턴
    DECISION_PATTERNS = [
        r"결정[:\s]*(.+?)(?:\n|$)",
        r"합의[:\s]*(.+?)(?:\n|$)",
        r"확정[:\s]*(.+?)(?:\n|$)",
        r"→\s*결정[:\s]*(.+?)(?:\n|$)",
    ]
    
    TASK_PATTERNS = [
        r"할일[:\s]*(.+?)(?:\n|$)",
        r"TODO[:\s]*(.+?)(?:\n|$)",
        r"액션[:\s]*(.+?)(?:\n|$)",
        r"담당[:\s]*(.+?)(?:\n|$)",
        r"→\s*(.+?)\s*담당",
        r"\[\s*\]\s*(.+?)(?:\n|$)",  # [ ] 체크박스
    ]
    
    def __init__(self, holons_path: str):
        self.holons_path = Path(holons_path)
        self.meetings_path = self.holons_path.parent / "meetings"
        self.decisions_path = self.holons_path.parent / "decisions"
        self.tasks_path = self.holons_path.parent / "tasks"
        
        # 폴더 생성
        self.meetings_path.mkdir(exist_ok=True)
        self.decisions_path.mkdir(exist_ok=True)
        self.tasks_path.mkdir(exist_ok=True)
        
        # 기존 Holon 로드
        self.holons = self._load_holons()
    
    def _load_holons(self) -> Dict[str, dict]:
        """기존 Holon 문서 로드"""
        holons = {}
        for md_file in self.holons_path.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
            content = md_file.read_text(encoding="utf-8")
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                try:
                    holon = json.loads(json_match.group(1))
                    holon_id = holon.get("holon_id")
                    if holon_id:
                        holons[holon_id] = holon
                except:
                    pass
        return holons
    
    def _extract_title(self, text: str) -> str:
        """회의록에서 제목 추출"""
        lines = text.strip().split("\n")
        
        # 첫 줄이 제목일 가능성
        first_line = lines[0].strip()
        
        # # 으로 시작하면 마크다운 제목
        if first_line.startswith("#"):
            return first_line.lstrip("#").strip()
        
        # 제목: 패턴
        title_match = re.search(r"제목[:\s]*(.+?)(?:\n|$)", text)
        if title_match:
            return title_match.group(1).strip()
        
        # 회의명: 패턴
        meeting_match = re.search(r"회의명[:\s]*(.+?)(?:\n|$)", text)
        if meeting_match:
            return meeting_match.group(1).strip()
        
        # 첫 줄 사용 (30자 제한)
        return first_line[:30] if first_line else "회의록"
    
    def _extract_date(self, text: str) -> str:
        """회의록에서 날짜 추출"""
        # YYYY-MM-DD 패턴
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        if date_match:
            return date_match.group(1)
        
        # YYYY.MM.DD 패턴
        date_match = re.search(r"(\d{4})\.(\d{2})\.(\d{2})", text)
        if date_match:
            return f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        
        # 오늘 날짜
        return datetime.now().strftime("%Y-%m-%d")
    
    def _extract_participants(self, text: str) -> List[str]:
        """참석자 추출"""
        participants = []
        
        # 참석자: 패턴
        match = re.search(r"참석자?[:\s]*(.+?)(?:\n|$)", text)
        if match:
            names = re.split(r"[,，、\s]+", match.group(1))
            participants = [n.strip() for n in names if n.strip()]
        
        return participants if participants else ["미지정"]
    
    def _find_best_parent(self, text: str) -> Tuple[str, float]:
        """내용 기반으로 최적의 parent 찾기"""
        text_lower = text.lower()
        
        # 키워드 매칭 점수 계산
        scores = {}
        for keyword, parent_id in self.KEYWORD_PARENT_MAP.items():
            if keyword in text_lower:
                scores[parent_id] = scores.get(parent_id, 0) + 1
        
        if scores:
            best_parent = max(scores, key=scores.get)
            confidence = scores[best_parent] / len(self.KEYWORD_PARENT_MAP)
            return best_parent, min(confidence * 5, 1.0)  # 최대 1.0
        
        # 기본값: strategy-2025-001 (AI PM)
        return "strategy-2025-001", 0.3
    
    def _extract_decisions(self, text: str) -> List[str]:
        """결정 사항 추출"""
        decisions = []
        for pattern in self.DECISION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            decisions.extend([m.strip() for m in matches if m.strip()])
        return list(set(decisions))  # 중복 제거
    
    def _extract_tasks(self, text: str) -> List[str]:
        """할일 추출"""
        tasks = []
        for pattern in self.TASK_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            tasks.extend([m.strip() for m in matches if m.strip()])
        return list(set(tasks))  # 중복 제거
    
    def _extract_agenda(self, text: str) -> List[str]:
        """안건 추출"""
        agenda = []
        
        # 안건: 패턴
        agenda_match = re.search(r"안건[:\s]*\n?((?:.+\n?)+)", text)
        if agenda_match:
            items = agenda_match.group(1).split("\n")
            for item in items:
                item = item.strip()
                if item and not item.startswith(("참석", "일시", "장소")):
                    # 번호/불릿 제거
                    item = re.sub(r"^[\d\.\-\*\•]+\s*", "", item)
                    if item:
                        agenda.append(item)
        
        return agenda[:5]  # 최대 5개
    
    def _generate_meeting_id(self) -> str:
        """회의 ID 생성"""
        today = datetime.now()
        year = today.strftime("%Y")
        
        # 기존 meeting 개수 확인
        existing = list(self.meetings_path.glob(f"meeting-{year}-*.md"))
        next_num = len(existing) + 1
        
        return f"meeting-{year}-{next_num:03d}"
    
    def _create_meeting_holon(self, text: str) -> dict:
        """회의록 텍스트로 Meeting Holon 생성"""
        title = self._extract_title(text)
        date = self._extract_date(text)
        participants = self._extract_participants(text)
        parent_id, confidence = self._find_best_parent(text)
        decisions = self._extract_decisions(text)
        tasks = self._extract_tasks(text)
        agenda = self._extract_agenda(text)
        meeting_id = self._generate_meeting_id()
        
        # Root W 가져오기
        root_w = self.holons.get("hte-doc-000", {}).get("W", {})
        root_drive = root_w.get("will", {}).get("drive", "")
        
        holon = {
            "holon_id": meeting_id,
            "slug": title.replace(" ", "-").lower()[:30],
            "type": "meeting",
            "module": "M02_TimelineGenesis",
            "meta": {
                "title": title,
                "owner": participants[0] if participants else "미지정",
                "created_at": date,
                "updated_at": date,
                "priority": "high",
                "status": "active"
            },
            "W": {
                "worldview": {
                    "identity": "회의를 통해 의사결정과 방향 정렬을 수행하는 협업 세션",
                    "belief": "효과적인 회의는 명확한 결정과 실행 가능한 태스크를 만들어낸다",
                    "value_system": "시간 효율, 결정 명확성, 실행 연결"
                },
                "will": {
                    "drive": f"이 회의를 통해 {title} 관련 명확한 결정을 내리고 다음 단계로 진행한다. {root_drive[:50]}...",
                    "commitment": "모든 안건에 대해 결론을 내리고 담당자를 지정한다",
                    "non_negotiables": ["결정 사항 문서화", "담당자 지정", "기한 설정"]
                },
                "intention": {
                    "primary": title,
                    "secondary": agenda[:3] if agenda else ["안건 논의"],
                    "constraints": ["시간 제한", "참석자 일정"]
                },
                "goal": {
                    "ultimate": f"{title} 완료 및 후속 조치 확정",
                    "milestones": ["안건 논의", "결정", "액션 아이템 도출"],
                    "kpi": [f"결정 {len(decisions)}건", f"태스크 {len(tasks)}건"],
                    "okr": {
                        "objective": title,
                        "key_results": decisions[:3] if decisions else ["결정 사항 도출"]
                    }
                },
                "activation": {
                    "triggers": ["회의 시작"],
                    "resonance_check": f"상위 목표({parent_id})와 정렬 확인됨 (신뢰도: {confidence:.0%})",
                    "drift_detection": "회의 목적에서 벗어나는 논의 감지"
                }
            },
            "X": {
                "context": text[:500] + "..." if len(text) > 500 else text,
                "current_state": "회의 완료",
                "heartbeat": "once",
                "signals": ["회의록 작성됨"],
                "constraints": ["참석자 일정", "시간 제한"],
                "will": "회의 맥락을 정확히 기록하여 후속 조치에 활용한다"
            },
            "S": {
                "resources": [
                    {"type": "human", "id": p, "role": "참석자"} for p in participants
                ],
                "dependencies": [parent_id],
                "access_points": ["이 문서"],
                "structure_model": "회의 → 결정 → 태스크",
                "ontology_ref": ["M02_TimelineGenesis"],
                "readiness_score": 1.0,
                "will": "필요한 리소스를 확보하여 회의 목적을 달성한다"
            },
            "P": {
                "procedure_steps": [
                    {"step_id": "p001", "description": "안건 검토", "status": "done"},
                    {"step_id": "p002", "description": "논의 진행", "status": "done"},
                    {"step_id": "p003", "description": "결정 도출", "status": "done"},
                    {"step_id": "p004", "description": "후속 조치 확정", "status": "done"}
                ],
                "optimization_logic": "효율적인 회의 진행",
                "will": "체계적인 절차로 생산적인 회의를 수행한다"
            },
            "E": {
                "execution_plan": [
                    {
                        "action_id": "e001",
                        "description": f"결정사항 {len(decisions)}건 실행",
                        "role": participants[0] if participants else "담당자",
                        "eta": "TBD"
                    }
                ],
                "tooling": ["회의실", "화상회의"],
                "edge_case_handling": ["불참 시 회의록 공유"],
                "will": "결정된 사항을 실제로 실행한다"
            },
            "R": {
                "reflection_notes": ["회의 완료"],
                "lessons_learned": [],
                "success_path_inference": "명확한 결정 → 실행 → 성과",
                "future_prediction": "후속 회의 필요 여부 판단",
                "will": "회의 결과를 되돌아보고 개선점을 찾는다"
            },
            "T": {
                "impact_channels": ["참석자", "관련 팀"],
                "traffic_model": "회의록 공유 → 액션 실행",
                "viral_mechanics": "결정 사항의 팀 전파",
                "bottleneck_points": ["실행 지연"],
                "will": "회의 결과를 관련자에게 효과적으로 전파한다"
            },
            "A": {
                "abstraction": "반복 가능한 회의 템플릿화",
                "modularization": ["안건 모듈", "결정 모듈", "태스크 모듈"],
                "automation_opportunities": ["회의록 자동 생성", "태스크 자동 추출"],
                "integration_targets": [parent_id],
                "resonance_logic": f"상위 목표와 정렬 (신뢰도: {confidence:.0%})",
                "will": "회의 패턴을 고도화하여 효율성을 높인다"
            },
            "links": {
                "parent": parent_id,
                "children": [],
                "related": [],
                "supersedes": None
            },
            "_parsed": {
                "decisions": decisions,
                "tasks": tasks,
                "agenda": agenda,
                "participants": participants,
                "confidence": confidence
            }
        }
        
        return holon
    
    def parse_and_create(self, text: str, auto_spawn: bool = True) -> dict:
        """회의록 파싱 후 Holon 파일 생성"""
        print("=" * 60)
        print("🔥 회의록 자동 파싱 & Holon 생성")
        print("=" * 60)
        print()
        
        # Meeting Holon 생성
        print("📝 회의록 분석 중...")
        holon = self._create_meeting_holon(text)
        
        meeting_id = holon["holon_id"]
        title = holon["meta"]["title"]
        parent_id = holon["links"]["parent"]
        confidence = holon["_parsed"]["confidence"]
        decisions = holon["_parsed"]["decisions"]
        tasks = holon["_parsed"]["tasks"]
        
        print(f"   제목: {title}")
        print(f"   ID: {meeting_id}")
        print(f"   상위 연결: {parent_id} (신뢰도: {confidence:.0%})")
        print(f"   결정 사항: {len(decisions)}건")
        print(f"   할일: {len(tasks)}건")
        print()
        
        # _parsed 제거 후 저장
        parsed_info = holon.pop("_parsed")
        
        # Meeting 파일 저장
        filename = f"{meeting_id}-{holon['slug']}.md"
        filepath = self.meetings_path / filename
        
        content = f"""```json
{json.dumps(holon, ensure_ascii=False, indent=2)}
```

---

# 📋 {title}

## 원본 회의록

{text}

---

## 자동 추출 정보

### 결정 사항
{chr(10).join(f"- {d}" for d in decisions) if decisions else "- (추출된 결정 없음)"}

### 할일
{chr(10).join(f"- [ ] {t}" for t in tasks) if tasks else "- (추출된 할일 없음)"}

---

*🔥 Self-Healing 모드로 자동 생성됨*
"""
        
        filepath.write_text(content, encoding="utf-8")
        print(f"✅ Meeting 생성: {filepath}")
        
        result = {
            "meeting_id": meeting_id,
            "file": str(filepath),
            "parent": parent_id,
            "confidence": confidence,
            "decisions": decisions,
            "tasks": tasks,
            "spawned": []
        }
        
        # Decision/Task 자동 생성
        if auto_spawn and (decisions or tasks):
            print()
            print("🚀 Decision/Task 자동 생성 중...")
            spawned = self._spawn_from_meeting(meeting_id, decisions, tasks)
            result["spawned"] = spawned
        
        print()
        print("=" * 60)
        print(f"🔥 완료! Meeting + {len(result['spawned'])}개 하위 문서 생성")
        print("=" * 60)
        
        return result
    
    def _spawn_from_meeting(self, meeting_id: str, decisions: List[str], tasks: List[str]) -> List[str]:
        """Meeting에서 Decision/Task 생성"""
        spawned = []
        today = datetime.now().strftime("%Y-%m-%d")
        year = datetime.now().strftime("%Y")
        
        # Decision 생성
        for i, decision in enumerate(decisions[:5], 1):  # 최대 5개
            decision_id = f"decision-{year}-{len(list(self.decisions_path.glob('*.md'))) + i:03d}"
            
            decision_holon = {
                "holon_id": decision_id,
                "slug": decision[:20].replace(" ", "-").lower(),
                "type": "decision",
                "meta": {
                    "title": decision[:50],
                    "created_at": today,
                    "status": "active"
                },
                "W": {
                    "will": {
                        "drive": f"'{decision}'을 실행에 옮긴다"
                    }
                },
                "links": {
                    "parent": meeting_id,
                    "children": [],
                    "related": []
                }
            }
            
            filepath = self.decisions_path / f"{decision_id}.md"
            content = f"""```json
{json.dumps(decision_holon, ensure_ascii=False, indent=2)}
```

# ✅ {decision[:50]}

*{meeting_id}에서 자동 생성됨*
"""
            filepath.write_text(content, encoding="utf-8")
            spawned.append(decision_id)
            print(f"   ✅ Decision: {decision_id}")
        
        # Task 생성
        for i, task in enumerate(tasks[:5], 1):  # 최대 5개
            task_id = f"task-{year}-{len(list(self.tasks_path.glob('*.md'))) + i:03d}"
            
            task_holon = {
                "holon_id": task_id,
                "slug": task[:20].replace(" ", "-").lower(),
                "type": "task",
                "meta": {
                    "title": task[:50],
                    "created_at": today,
                    "status": "pending"
                },
                "W": {
                    "will": {
                        "drive": f"'{task}'를 완료한다"
                    }
                },
                "links": {
                    "parent": meeting_id,
                    "children": [],
                    "related": []
                }
            }
            
            filepath = self.tasks_path / f"{task_id}.md"
            content = f"""```json
{json.dumps(task_holon, ensure_ascii=False, indent=2)}
```

# ⬜ {task[:50]}

- [ ] 완료

*{meeting_id}에서 자동 생성됨*
"""
            filepath.write_text(content, encoding="utf-8")
            spawned.append(task_id)
            print(f"   ⬜ Task: {task_id}")
        
        return spawned


def main():
    """테스트용"""
    sample = """
# 2025년 AI 튜터 개발 킥오프 회의

일시: 2025-11-30
참석자: 김철수, 이영희, 박민수

## 안건
1. AI 튜터 MVP 범위 확정
2. 개발 일정 논의
3. 담당자 배정

## 논의 내용
학생 진단 기능을 먼저 개발하기로 함.
시선 추적 기능은 2단계로 진행.

## 결정 사항
- 결정: MVP는 진단 리포트 기능으로 한정
- 결정: 2월 말 베타 출시 목표

## 할일
- TODO: 김철수 - UI 디자인 초안 (12/15까지)
- TODO: 이영희 - 백엔드 API 설계
- 박민수 담당 - 데이터 모델 설계
"""
    
    parser = MeetingParser(str(Path(__file__).parent))
    result = parser.parse_and_create(sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

