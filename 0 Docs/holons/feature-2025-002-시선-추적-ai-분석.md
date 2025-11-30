```json
{
  "holon_id": "feature-2025-002",
  "slug": "시선-추적-ai-분석",
  "type": "feature",
  "module": "M16_AIMindArchitecture",
  "meta": {
    "title": "시선 추적 AI 분석",
    "created_at": "2025-11-29",
    "updated_at": "2025-11-30",
    "status": "active",
    "owner": "AI Research Team"
  },
  "W": {
    "worldview": {
      "identity": "전국 수학 학원 학생들의 학습 집중도와 이해도를 시선 추적 AI로 실시간 분석하는 혁신 기능",
      "belief": "시선 데이터는 학생의 인지 상태를 가장 정확하게 반영하며, 이를 통해 진정한 1:1 맞춤 교육이 가능해진다",
      "value_system": "실시간 분석, 비침습적 측정, 과학적 근거 기반 교육"
    },
    "will": {
      "drive": "전국 수학 학원에서 웹캠 기반 시선 추적 AI로 학생의 학습 집중도를 실시간 자동 분석한다",
      "commitment": "Bloom's 2-Sigma 문제를 기술로 해결하여 1:1 과외 효과를 대규모로 재현한다",
      "non_negotiables": [
        "개인정보 보호 철저 준수",
        "분석 정확도 85% 이상"
      ]
    },
    "intention": {
      "primary": "웹캠 시선 추적으로 학생 집중도/이해도 실시간 파악",
      "secondary": [
        "최적 개입 타이밍 자동 감지",
        "학습 효율 극대화"
      ],
      "constraints": [
        "웹캠 품질 의존성",
        "조명 환경 영향"
      ]
    },
    "goal": {
      "ultimate": "시선 추적 AI가 전국 수학 학원의 표준 학습 모니터링 도구가 되어 시장 자동화 독점에 기여",
      "milestones": [
        "시선 추적 알고리즘 개발",
        "웹 기반 실시간 분석 구현",
        "파일럿 학원 테스트"
      ],
      "kpi": [
        "시선 추적 정확도 85%+",
        "집중도 예측 정확도 80%+",
        "개입 타이밍 적중률 75%+"
      ],
      "okr": {
        "objective": "시선 추적 AI를 학원 학습 모니터링 핵심 도구로 정착",
        "key_results": [
          "Q1: 알고리즘 개발 및 검증",
          "Q2: 50개 학원 파일럿",
          "Q3: 전국 확대 및 자동화 완료"
        ]
      }
    },
    "activation": {
      "triggers": [
        "온라인 수업 시작 시",
        "학생 집중도 저하 감지 시",
        "정기 학습 분석 요청 시"
      ],
      "resonance_check": "상위 제품 아키텍처(hte-doc-002)의 AI Tutor 비전과 정렬되는가?",
      "drift_detection": "단순 출석 체크 용도로 퇴화하면 의지 약화 신호"
    }
  },
  "X": {
    "context": "현재 온라인/오프라인 수업에서 학생의 실제 집중도를 파악할 방법이 없음. 교사의 직관에만 의존하여 개입 타이밍을 놓치는 경우가 많음",
    "current_state": "연구 단계 - 시선 추적 알고리즘 프로토타입 개발 중",
    "heartbeat": "weekly",
    "signals": [
      "시선 이탈 빈도",
      "응시 패턴 변화",
      "집중도 점수 추이"
    ],
    "constraints": [
      "저사양 기기 지원 필요",
      "다양한 조명 환경 대응"
    ],
    "will": "학생의 실제 학습 상태를 과학적으로 파악하여 교육 품질을 혁신한다"
  },
  "S": {
    "resources": [
      "웹캠 영상 스트림",
      "시선 추적 ML 모델",
      "실시간 분석 서버"
    ],
    "dependencies": [
      "hte-doc-002"
    ],
    "access_points": [
      "학생 학습 화면 (웹)",
      "교사 모니터링 대시보드",
      "관리자 분석 포털"
    ],
    "structure_model": "웹캠 → 시선 추적 → 집중도 분석 → 개입 신호 → 교사/AI 알림",
    "ontology_ref": [
      "M16_AIMindArchitecture",
      "M17_NervousSystem"
    ],
    "readiness_score": 0.4,
    "will": "최첨단 AI 기술을 교육 현장에 적용 가능한 형태로 구현한다"
  },
  "P": {
    "procedure_steps": [
      {
        "step_id": "p001",
        "description": "웹캠 영상에서 얼굴/눈 감지",
        "inputs": [
          "실시간 웹캠 스트림"
        ],
        "expected_outputs": [
          "얼굴 랜드마크",
          "눈 위치 좌표"
        ],
        "tools_required": [
          "MediaPipe",
          "OpenCV"
        ]
      },
      {
        "step_id": "p002",
        "description": "시선 방향 및 응시점 추적",
        "inputs": [
          "눈 위치 좌표"
        ],
        "expected_outputs": [
          "화면 내 응시점",
          "시선 벡터"
        ],
        "tools_required": [
          "Gaze Estimation Model"
        ]
      },
      {
        "step_id": "p003",
        "description": "집중도 점수 계산 및 패턴 분석",
        "inputs": [
          "응시점 시계열 데이터"
        ],
        "expected_outputs": [
          "집중도 점수",
          "이탈 알림"
        ],
        "tools_required": [
          "Time-series Analysis",
          "ML Classifier"
        ]
      }
    ],
    "optimization_logic": "경량 모델로 클라이언트 처리, 100ms 이내 응답",
    "will": "실시간 분석으로 즉각적인 피드백이 가능한 시스템을 구축한다"
  },
  "E": {
    "execution_plan": [
      {
        "action_id": "e001",
        "action": "시선 추적 알고리즘 연구 및 프로토타입",
        "eta_hours": 80,
        "role": "ML Research Engineer"
      },
      {
        "action_id": "e002",
        "action": "웹 기반 실시간 처리 파이프라인 구축",
        "eta_hours": 60,
        "role": "Backend Engineer"
      },
      {
        "action_id": "e003",
        "action": "교사용 모니터링 UI 개발",
        "eta_hours": 40,
        "role": "Frontend Engineer"
      }
    ],
    "tooling": [
      "TensorFlow.js",
      "WebRTC",
      "Python",
      "React"
    ],
    "edge_case_handling": [
      "카메라 미작동 시 대체 분석",
      "저조도 환경 보정"
    ],
    "will": "기술적 도전을 극복하여 실용적인 제품을 완성한다"
  },
  "R": {
    "reflection_notes": [
      "기존 시선 추적 연구 논문 분석 완료"
    ],
    "lessons_learned": [
      "정확도와 속도의 트레이드오프 관리 필요"
    ],
    "success_path_inference": "정확한 집중도 파악 → 적시 개입 → 학습 효율 상승 → 학원 경쟁력 강화",
    "future_prediction": "시선 추적이 모든 온라인 교육의 기본 기능이 될 것",
    "will": "지속적인 연구와 개선으로 기술 리더십을 유지한다"
  },
  "T": {
    "impact_channels": [
      "학생 화면 → AI 분석 → 교사 알림",
      "분석 결과 → 학부모 리포트"
    ],
    "traffic_model": "수업 중 실시간 분석, 수업 후 종합 리포트",
    "viral_mechanics": "혁신 기술 → 학원 마케팅 → 학부모 관심 → 시장 확대",
    "bottleneck_points": [
      "동시 접속자 증가 시 서버 부하"
    ],
    "will": "시선 추적 AI를 학원의 핵심 차별화 요소로 확산한다"
  },
  "A": {
    "abstraction": "다른 교육 플랫폼에도 적용 가능한 범용 시선 분석 SDK",
    "modularization": [
      "얼굴 감지 모듈",
      "시선 추적 모듈",
      "집중도 분석 모듈",
      "알림 모듈"
    ],
    "automation_opportunities": [
      "집중도 저하 시 자동 AI 개입",
      "자동 휴식 권장"
    ],
    "integration_targets": [
      "학생 진단 리포트",
      "AI Tutor 시스템",
      "LMS"
    ],
    "resonance_logic": "상위 W(hte-doc-002)의 'AI 기반 실시간 학습 지원' 비전과 완전히 정렬",
    "will": "확장 가능하고 재사용 가능한 기술로 미래 성장을 대비한다"
  },
  "links": {
    "parent": "strategy-2025-001",
    "children": [],
    "related": [
      "feature-2025-001"
    ],
    "supersedes": null
  }
}
```

---

# 시선 추적 AI 분석

## 개요

전국 수학 학원 학생들의 학습 집중도를 웹캠 기반 시선 추적 AI로 실시간 분석하는 혁신 기능입니다. Bloom's 2-Sigma 문제를 기술로 해결하여 1:1 과외 효과를 대규모로 재현합니다.

## 핵심 기술

- **시선 추적**: 웹캠만으로 학생의 응시점을 실시간 추적
- **집중도 분석**: AI가 시선 패턴을 분석하여 집중도 점수 산출
- **자동 개입**: 집중도 저하 감지 시 교사/AI에 알림

## 기대 효과

1. 학생 집중도 30% 향상 (조기 개입 효과)
2. 교사 개입 효율성 50% 증가
3. 학습 효율 극대화로 학원 경쟁력 강화

---

## 🔗 Holonic Links

### ⬆️ Parent
- [hte-doc-002](02-product-architecture.md) - Product Architecture

### ↔️ Related
- [feature-2025-001](feature-2025-001-학생-진단-리포트.md) - 학생 진단 리포트
