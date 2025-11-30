```json
{
  "holon_id": "hte-doc-001",
  "slug": "organizational-structure",
  "type": "structure",
  "module": "M02_TimelineGenesis",

  "meta": {
    "title": "Holonic Organizational Structure (WXSPERTA Model)",
    "owner": "HTE",
    "created_at": "2025-11-29",
    "updated_at": "2025-11-29",
    "priority": "high",
    "status": "active"
  },

  "W": {
    "worldview": {
      "identity": "자율적이면서 전체 미션에 정렬된 홀론 기반 조직",
      "belief": "분산된 자율성과 중앙 집중된 목적이 공존할 수 있다",
      "value_system": "각 부서는 홀론으로서 자기완결적이며 동시에 전체에 기여한다"
    },
    "will": {
      "drive": "전국 수학 학원 시장 독점을 위해 모든 부서와 팀을 홀론으로 설계하여 자율성과 전체 미션 정렬을 반드시 달성한다",
      "commitment": "전통적 계층 구조의 한계를 돌파하고 진정한 자기진화 조직을 만든다",
      "non_negotiables": ["부서 자율성", "전체 미션 정렬", "WXSPERTA 일관성"]
    },
    "intention": {
      "primary": "모든 부서가 WXSPERTA 구조로 운영되며 자기진화 가능하게 만든다",
      "secondary": ["부서간 협업 최적화", "분산 의사결정 체계 구축"],
      "constraints": ["기존 조직 문화 존중", "점진적 변화", "학습 곡선 관리"]
    },
    "goal": {
      "ultimate": "홀론 기반 완전 자율 조직 구조 완성",
      "milestones": ["부서별 WXSPERTA 정의", "부서간 API 정의", "분산 의사결정 체계"],
      "kpi": ["부서별 목표 달성률", "부서간 협업 효율", "적응 속도"],
      "okr": {
        "objective": "홀론 기반 조직 구조 완성",
        "key_results": ["전 부서 WXSPERTA 정의 완료", "부서간 API 인터페이스 정의", "분산 의사결정 체계 구축"]
      }
    },
    "activation": {
      "triggers": ["부서 목표 미달", "협업 효율 저하", "변화 저항 감지"],
      "resonance_check": "모든 부서 홀론이 상위 W(시장 독점)와 공명하는가?",
      "drift_detection": "부서 이기주의, 전체 미션 이탈은 경고 신호"
    }
  },

  "X": {
    "context": "전통적 계층 구조는 변화에 느리고 혁신을 저해함",
    "current_state": "홀론 기반 조직 설계 완료, 부서별 적용 진행 중",
    "heartbeat": "weekly",
    "signals": ["부서 성과 지표", "협업 효율", "직원 만족도"],
    "constraints": ["기존 조직 문화", "변화 저항", "학습 곡선"],
    "will": "조직의 현재 상태를 정확히 파악하고 적응 전략을 수립하려는 의지"
  },

  "S": {
    "resources": [
      "Content Holon (컨텐츠 팀)",
      "AI Tutor Holon (AI 팀)",
      "Platform Holon (플랫폼 팀)",
      "Marketing Holon",
      "Operations Holon"
    ],
    "dependencies": ["hte-doc-000"],
    "access_points": ["부서별 WXSPERTA 문서", "조직도"],
    "structure_model": "Holarchy: Company → Departments → Teams → Individuals",
    "ontology_ref": ["McKinsey Haier Model", "Holonic Manufacturing"],
    "readiness_score": 0.7,
    "will": "각 부서가 필요로 하는 모든 구조적 리소스를 체계화하려는 의지"
  },

  "P": {
    "procedure_steps": [
      {
        "step_id": "org-p001",
        "description": "각 부서의 W(목적) 정의",
        "inputs": ["회사 미션", "부서 역할"],
        "expected_outputs": ["부서별 목적 선언문"],
        "tools_required": ["워크샵", "템플릿"]
      },
      {
        "step_id": "org-p002",
        "description": "부서별 WXSPERTA 8요소 작성",
        "inputs": ["목적", "현황", "리소스"],
        "expected_outputs": ["부서별 Holon JSON"],
        "tools_required": ["Holon 템플릿"]
      },
      {
        "step_id": "org-p003",
        "description": "부서간 인터페이스 정의",
        "inputs": ["부서별 Holon"],
        "expected_outputs": ["협업 API 명세"],
        "tools_required": ["문서화 도구"]
      }
    ],
    "optimization_logic": "중첩된 거버넌스로 의사결정을 가장 가까운 수준에서 처리",
    "will": "명확하고 효율적인 절차로 조직 변환을 가속화하려는 의지"
  },

  "E": {
    "execution_plan": [
      {
        "action_id": "org-e001",
        "action": "부서장 대상 WXSPERTA 교육",
        "eta_hours": 16,
        "role": "PM"
      },
      {
        "action_id": "org-e002",
        "action": "부서별 Holon 정의 워크샵",
        "eta_hours": 40,
        "role": "PM"
      },
      {
        "action_id": "org-e003",
        "action": "Holon 기반 OKR 설정",
        "eta_hours": 24,
        "role": "PM"
      }
    ],
    "tooling": ["Miro", "Notion", "Holon Template"],
    "edge_case_handling": [
      "저항하는 부서: 파일럿 성공 사례로 설득",
      "이해 부족: 추가 교육 제공"
    ],
    "will": "계획을 즉시 실행으로 전환하여 조직 변화를 실현하려는 의지"
  },

  "R": {
    "reflection_notes": [
      "Haier의 렌단헤이 모델이 자기진화 조직의 좋은 사례",
      "홀론 구조는 자기 유사성으로 확장이 용이",
      "분산 의사결정이 적응 속도를 높임"
    ],
    "lessons_learned": [
      "목적(W) 정렬이 가장 중요한 첫 단계",
      "의지(Will)가 명확해야 실행력이 생김"
    ],
    "success_path_inference": "작은 팀부터 시작하여 성공 사례를 만들고 확산",
    "future_prediction": "AI Agent가 각 부서 홀론의 보조자로 작동하는 미래",
    "will": "지속적 성찰로 조직 설계를 개선하려는 의지"
  },

  "T": {
    "impact_channels": ["전체 조직", "HR", "경영진"],
    "traffic_model": "Top-down 전략 + Bottom-up 실행 피드백",
    "viral_mechanics": "성공한 팀의 사례를 내부 공유",
    "bottleneck_points": ["변화 저항", "기존 프로세스와 충돌"],
    "will": "홀론 조직 모델을 전 조직에 확산하려는 의지"
  },

  "A": {
    "abstraction": "부서 홀론 모델을 표준화하여 새 부서 생성 시 즉시 적용 가능",
    "modularization": ["부서 템플릿", "팀 템플릿", "개인 역할 템플릿"],
    "automation_opportunities": [
      "부서 성과 자동 집계",
      "협업 효율 자동 측정",
      "OKR 진행률 자동 추적"
    ],
    "integration_targets": ["hte-doc-003"],
    "resonance_logic": "상위 홀론의 목적이 하위 홀론에 공명하여 일관된 방향성 유지",
    "will": "조직 설계를 고도화하여 자동화된 자기진화 조직을 만들려는 의지"
  },

  "links": {
    "parent": "hte-doc-000",
    "children": [],
    "related": ["hte-doc-002", "hte-doc-003"],
    "supersedes": null
  }
}
```

---

# Holonic Organizational Structure (WXSPERTA Model)

## 개요

홀론 기반 조직 설계에서 모든 부서와 팀은 **홀론**입니다 — 자체 목표와 프로세스를 가진 자율적 단위이면서 동시에 더 큰 회사 미션에 기여합니다.

## 조직 홀라키 구조

```
Company (최상위 홀론)
├── Content Department (홀론)
│   ├── Math Team (홀론)
│   ├── Science Team (홀론)
│   └── Language Team (홀론)
├── AI Department (홀론)
│   ├── ML Research Team
│   └── AI Product Team
├── Platform Department (홀론)
│   ├── Frontend Team
│   └── Backend Team
└── Operations Department (홀론)
```

## 부서별 WXSPERTA 적용

### Content Holon 예시

| Element | 내용 |
|---------|------|
| **W** | 가장 효과적이고 매력적인 K-12 콘텐츠 제공, 학습자 피드백으로 지속 개선 |
| **X** | 현재 커리큘럼 상태, 학생 성과 데이터, 시장 트렌드 |
| **S** | 과목별 팀, 콘텐츠 저장소, 분석 도구 |
| **P** | 설계 → 배포 → 데이터 수집 → 개선 루프 |
| **E** | 콘텐츠 제작, A/B 테스트, 품질 검토 |
| **R** | 학생 성과 분석, 콘텐츠 효과성 평가 |
| **T** | 다른 부서와 협업, 외부 파트너십 |
| **A** | 콘텐츠 생성 자동화, 개인화 알고리즘 |

### AI Tutor Holon 예시

| Element | 내용 |
|---------|------|
| **W** | 학생 상호작용에서 지속 학습하는 지능형 튜터링 시스템 개발 |
| **X** | 현재 AI 모델 성능, 학생 데이터, 기술 트렌드 |
| **S** | ML 연구팀, 데이터 엔지니어링팀, 컴퓨팅 리소스 |
| **P** | 데이터 수집 → 모델 훈련 → 배포 → 모니터링 |
| **E** | 모델 개발, A/B 테스트, 성능 최적화 |
| **R** | 학습 효과 분석, 모델 개선 방향 도출 |
| **T** | Platform, Content 팀과 통합 |
| **A** | 자체 학습 AI, 자동화된 개인화 |

## 핵심 원칙

1. **분산된 의사결정**: 문제에 가장 가까운 수준에서 결정
2. **목적 정렬**: 모든 팀의 W가 상위 홀론과 연결
3. **피드백 루프**: 지속적 성찰과 개선
4. **자기 유사성**: 모든 수준에서 동일한 WXSPERTA 구조

---

## 🔗 Holonic Links

### ⬆️ Parent (상위 문서)
- [00-holarchy-overview](./00-holarchy-overview.md) — 전체 아키텍처 개요

### ↔️ Related (관련 문서)
- [03-operations-strategy](./03-operations-strategy.md) — 운영 전략

