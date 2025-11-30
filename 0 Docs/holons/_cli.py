#!/usr/bin/env python3
"""
Holarchy Self-Healing CLI v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 모든 명령은 "기록만, 중단 없음"
- 시스템은 절대 멈추지 않음
- 수정은 항상 선택사항
"""

import argparse
import sys
from pathlib import Path

# 같은 폴더의 모듈 import
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def cmd_check(args):
    """Self-Healing 검사 (기록만, 중단 없음)"""
    from _validate import HolarchyValidator
    validator = HolarchyValidator(str(script_dir.parent))
    validator.run_all_validations()
    # Self-Healing: 항상 성공


def cmd_risk(args):
    """위험도 점수 확인"""
    import json
    reports_path = script_dir.parent / "reports" / "risk_score.json"
    
    print("=" * 60)
    print("📊 Self-Healing 위험도 점수")
    print("   (참고용 - 낮아도 시스템 정상 작동)")
    print("=" * 60)
    print()
    
    if not reports_path.exists():
        print("⚠️  risk_score.json 없음")
        print("💡 'python _cli.py check' 먼저 실행하세요")
        return
    
    with open(reports_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    score = data.get("overall_score", 0)
    risk_level = data.get("risk_level", "unknown")
    
    emoji = "🟢" if risk_level == "low" else ("🟡" if risk_level == "medium" else "🔴")
    print(f"{emoji} 전체 점수: {score}% ({risk_level.upper()})")
    print()
    
    print("📋 세부 점수:")
    breakdown = data.get("breakdown", {})
    for key, value in breakdown.items():
        print(f"   {key}: {value}%")
    print()
    
    print("ℹ️  " + data.get("system_note", ""))


def cmd_suggest(args):
    """자동 수정 추천 보기"""
    import json
    reports_path = script_dir.parent / "reports" / "suggestions.json"
    
    print("=" * 60)
    print("💡 Self-Healing 수정 추천")
    print("   (선택사항 - 무시해도 시스템 정상 작동)")
    print("=" * 60)
    print()
    
    if not reports_path.exists():
        print("⚠️  suggestions.json 없음")
        print("💡 'python _cli.py check' 먼저 실행하세요")
        return
    
    with open(reports_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    suggestions = data.get("suggestions", [])
    
    if not suggestions:
        print("✅ 수정 추천 없음 - 모든 문서가 양호합니다")
        return
    
    for item in suggestions:
        print(f"📄 {item['holon_id']} (현재 {item['current_score']}% → 목표 {item['target_score']}%)")
        for s in item.get("suggestions", []):
            print(f"   → {s}")
        print()


def cmd_report(args):
    """현재 이슈 리포트 보기"""
    import json
    reports_path = script_dir.parent / "reports" / "issues.json"
    
    print("=" * 60)
    print("📋 Self-Healing 이슈 리포트")
    print("   (기록만 - 시스템 중단 없음)")
    print("=" * 60)
    print()
    
    if not reports_path.exists():
        print("⚠️  issues.json 없음")
        print("💡 'python _cli.py check' 먼저 실행하세요")
        return
    
    with open(reports_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"📅 생성 시각: {data.get('generated_at', 'N/A')}")
    print(f"📊 총 이슈: {data.get('total_issues', 0)}개")
    print()
    
    by_severity = data.get("by_severity", {})
    print("📈 심각도별:")
    print(f"   🔴 error: {by_severity.get('error', 0)}")
    print(f"   🟡 warning: {by_severity.get('warning', 0)}")
    print(f"   ℹ️  info: {by_severity.get('info', 0)}")
    print()
    
    issues = data.get("issues", [])
    if issues:
        print("📋 이슈 목록 (상위 10개):")
        print("-" * 60)
        for issue in issues[:10]:
            severity_emoji = {"error": "🔴", "warning": "🟡", "info": "ℹ️"}.get(issue["severity"], "❓")
            print(f"{severity_emoji} [{issue['holon_id']}] {issue['message']}")
        
        if len(issues) > 10:
            print(f"   ... 외 {len(issues) - 10}개")
    print()
    
    print("ℹ️  " + data.get("system_note", ""))


# 기존 validate 명령어 유지 (check로 리다이렉트)
def cmd_validate(args):
    """검증 실행 (check로 리다이렉트)"""
    print("ℹ️  validate 명령이 check로 변경되었습니다.")
    print("   Self-Healing 모드: 기록만, 시스템 중단 없음")
    print()
    cmd_check(args)


def cmd_link(args):
    """양방향 링크 동기화"""
    from _auto_link import AutoLinker
    linker = AutoLinker(str(script_dir))
    linker.run()


def cmd_create(args):
    """새 Holon 생성"""
    from _create_holon import HolonCreator
    
    print("=" * 60)
    print("📄 새 Holon 문서 생성")
    print("=" * 60)
    print()
    
    creator = HolonCreator(str(script_dir))
    holon_id = creator.create_holon(
        holon_type=args.type,
        title=args.title,
        parent_id=args.parent,
        module=args.module
    )
    
    print()
    print("💡 다음 단계:")
    print("   1. 생성된 파일의 [대괄호] 부분을 채우세요")
    print("   2. python _cli.py link  # 링크 동기화")
    print("   3. python _cli.py validate  # 검증")


def cmd_spawn(args):
    """Meeting에서 Decision/Task 생성"""
    from _spawn_meeting import MeetingSpawner
    spawner = MeetingSpawner(str(script_dir))
    spawner.spawn(args.meeting_id)


def cmd_place(args):
    """문서 자동 배치 - HTE 모듈 폴더에 파일명 규칙 적용"""
    from _document_placer import DocumentPlacer
    
    placer = DocumentPlacer()
    
    if args.file:
        # 파일에서 읽기
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {args.file}")
            return
        text = file_path.read_text(encoding="utf-8")
    elif args.text:
        # 직접 텍스트 입력
        text = args.text
    else:
        # 대화형 입력
        print("=" * 60)
        print("📝 문서 내용을 입력하세요 (빈 줄 2번으로 종료):")
        print("=" * 60)
        lines = []
        empty_count = 0
        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                lines.append(line)
            except EOFError:
                break
        text = "\n".join(lines)
    
    if not text.strip():
        print("❌ 문서 내용이 비어있습니다")
        return
    
    # 배치 및 생성
    result = placer.create_document(text, doc_type=args.type or "auto")
    
    print()
    print("💡 생성 완료!")
    print(f"   모듈: {result['module']}")
    print(f"   파일: {result['filename']}")
    print(f"   경로: {result['filepath']}")


def cmd_status(args):
    """시스템 상태 확인"""
    import json
    import re
    
    print("=" * 60)
    print("📊 Holarchy 시스템 상태")
    print("=" * 60)
    print()
    
    # 문서 카운트
    holons_path = script_dir
    meetings_path = script_dir.parent / "meetings"
    decisions_path = script_dir.parent / "decisions"
    tasks_path = script_dir.parent / "tasks"
    
    def count_holons(path):
        if not path.exists():
            return 0
        return len([f for f in path.glob("*.md") if not f.name.startswith("_")])
    
    holons = count_holons(holons_path)
    meetings = count_holons(meetings_path)
    decisions = count_holons(decisions_path)
    tasks = count_holons(tasks_path)
    
    print("📂 문서 현황:")
    print(f"   holons/    : {holons}개")
    print(f"   meetings/  : {meetings}개")
    print(f"   decisions/ : {decisions}개")
    print(f"   tasks/     : {tasks}개")
    print(f"   ─────────────────")
    print(f"   총계       : {holons + meetings + decisions + tasks}개")
    print()
    
    # 상태별 카운트
    status_count = {"draft": 0, "active": 0, "completed": 0, "archived": 0, "pending": 0}
    
    for folder in [holons_path, meetings_path, decisions_path, tasks_path]:
        if not folder.exists():
            continue
        for md_file in folder.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
            content = md_file.read_text(encoding="utf-8")
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                try:
                    holon = json.loads(json_match.group(1))
                    status = holon.get("meta", {}).get("status", "unknown")
                    status_count[status] = status_count.get(status, 0) + 1
                except:
                    pass
    
    print("📋 상태별 현황:")
    for status, count in status_count.items():
        if count > 0:
            print(f"   {status}: {count}개")
    print()
    
    # 최근 검증 결과 (간단히) - v3.0 API
    from _validate import HolarchyValidator
    validator = HolarchyValidator(str(script_dir.parent))
    validator.load_holons()
    validator.score_structure()
    validator.score_completeness()
    validator.score_resonance()
    validator.score_links()
    
    # 90% 기준 검증
    passed_docs = [s for s in validator.scores.values() if s.passed]
    needs_improvement = [s for s in validator.scores.values() if not s.passed]
    avg_score = sum(s.total for s in validator.scores.values()) / len(validator.scores) if validator.scores else 0
    
    print("🔍 검증 상태:")
    if avg_score >= 0.90:
        print(f"   ✅ 평균 완성도 {avg_score:.0%} (기준 90% 통과)")
    else:
        print(f"   📝 평균 완성도 {avg_score:.0%} (기준 90% 미달)")
        print(f"   ✅ 통과: {len(passed_docs)}개 / 📝 개선권장: {len(needs_improvement)}개")
    print()
    print("=" * 60)


def cmd_meeting(args):
    """회의록 자동 파싱 & Holon 생성"""
    from _meeting_parser import MeetingParser
    
    script_dir = Path(__file__).parent
    parser = MeetingParser(str(script_dir))
    
    if args.file:
        # 파일에서 읽기
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {args.file}")
            return
        text = file_path.read_text(encoding="utf-8")
    elif args.text:
        # 직접 텍스트 입력
        text = args.text
    else:
        # 대화형 입력
        print("=" * 60)
        print("📝 회의록을 입력하세요 (빈 줄 2번으로 종료):")
        print("=" * 60)
        lines = []
        empty_count = 0
        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                lines.append(line)
            except EOFError:
                break
        text = "\n".join(lines)
    
    if not text.strip():
        print("❌ 회의록 내용이 비어있습니다")
        return
    
    # 파싱 및 생성
    result = parser.parse_and_create(text, auto_spawn=not args.no_spawn)
    
    print()
    print("💡 다음 단계:")
    print(f"   1. 생성된 파일 확인: 0 Docs/meetings/{result['meeting_id']}*.md")
    print("   2. python _cli.py link  # 링크 동기화")
    print("   3. python _cli.py check  # 검증")


def cmd_chunk(args):
    """W 기반 Active Chunk 관리"""
    from _chunk_engine import ChunkManager
    
    script_dir = Path(__file__).parent
    manager = ChunkManager(str(script_dir.parent))
    
    if args.action == "generate":
        print("📂 Holon 로드 중...")
        manager.load_holons()
        print(f"   로드된 문서: {len(manager.holons)}개")
        print()
        
        print("🧮 W 기반 Salience 계산 중...")
        manager.generate_chunks()
        manager.save_chunks()
        print(f"   생성된 Chunk: {len(manager.chunks)}개")
        print()
        
        manager.print_report()
    
    else:  # show
        manager.load_holons()
        chunks = manager.load_chunks()
        if chunks:
            manager.chunks = chunks
            manager.root_w = manager.find_root_w()
            manager.print_report()
        else:
            print("❌ 저장된 Chunk 없음")
            print("💡 'python _cli.py chunk generate' 먼저 실행하세요")


def cmd_meta(args):
    """Meta-Research Engine"""
    from _meta_research_engine import MetaResearchEngine
    
    script_dir = Path(__file__).parent
    engine = MetaResearchEngine(str(script_dir.parent))
    
    if args.action == "report":
        result = engine.run_analysis()
        report = engine.generate_report(result)
        report_file = engine.save_report(report)
        
        engine.print_summary(result)
        print(f"📄 리포트 생성: {report_file}")
        print()
        print("🔔 리포트를 검토하고 제안을 승인/거부해주세요.")
    else:  # analyze
        result = engine.run_analysis()
        engine.print_summary(result)
        
        matrix_file = engine.save_matrix()
        print(f"📁 유사도 매트릭스: {matrix_file}")


def cmd_health(args):
    """시스템 건강 점검"""
    from _health_check import HealthCheckEngine
    
    script_dir = Path(__file__).parent
    engine = HealthCheckEngine(str(script_dir.parent))
    
    report = engine.run_all_checks()
    engine.print_report(report)
    
    if args.action == "report":
        report_file = engine.save_report(report)
        print()
        print(f"📄 리포트 저장: {report_file}")


def cmd_help(args):
    """도움말"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║       🔥 Holarchy Self-Healing CLI v2.0 - 명령어 가이드     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⚡ Self-Healing 핵심 명령어 (NEW)                           ║
║  ──────────────────────────────────────────────────────────  ║
║  check              문서 검사 (기록만, 시스템 중단 없음)     ║
║  risk               위험도 점수 확인 (참고용)                ║
║  suggest            자동 수정 추천 보기                      ║
║  report             현재 이슈 리포트 보기                    ║
║                                                              ║
║  * 모든 결과는 0 Docs/reports/에 저장                        ║
║  * 시스템은 절대 멈추지 않음                                 ║
║  * 수정은 항상 선택사항                                      ║
║                                                              ║
║  📋 기본 명령어                                              ║
║  ──────────────────────────────────────────────────────────  ║
║  status              시스템 상태 확인                        ║
║  link                양방향 링크 자동 동기화                 ║
║                                                              ║
║  📄 문서 생성                                                ║
║  ──────────────────────────────────────────────────────────  ║
║  create <type> <title> [--parent ID] [--module M00]          ║
║    type: strategy, structure, feature, meeting,              ║
║          decision, task                                      ║
║                                                              ║
║  🚀 자동 배치 (HTE 모듈)                                     ║
║  ──────────────────────────────────────────────────────────  ║
║  place               문서 → HTE 모듈 자동 배치               ║
║  place -f 파일       파일에서 읽어서 배치                    ║
║  place -t "내용"     텍스트로 직접 배치                      ║
║                                                              ║
║  * 내용 분석 → M00~M21 모듈 자동 선택                        ║
║  * 파일명: HTE_MXX_PYY_TZZ_V00_A00.md                        ║
║                                                              ║
║  🚀 회의 자동화                                              ║
║  ──────────────────────────────────────────────────────────  ║
║  meeting             회의록 자동 파싱 & Holon 생성           ║
║  spawn <meeting_id>  회의에서 Decision/Task 생성             ║
║                                                              ║
║  🧠 Working Memory                                           ║
║  ──────────────────────────────────────────────────────────  ║
║  chunk generate    W 기반 중요도로 Active Chunk 생성         ║
║  chunk show        현재 Active Chunk 표시                    ║
║                                                              ║
║  🔬 Meta-Research                                            ║
║  ──────────────────────────────────────────────────────────  ║
║  meta analyze      프로젝트 간 관계 분석                     ║
║  meta report       정제 제안 리포트 생성                     ║
║                                                              ║
║  🏥 Health (참고용)                                          ║
║  ──────────────────────────────────────────────────────────  ║
║  health check      8개 영역 건강 점검                        ║
║  health report     건강 점검 리포트 저장                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    parser = argparse.ArgumentParser(
        description="Holarchy Self-Healing CLI v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="명령어")
    
    # Self-Healing 핵심 명령어
    # check (NEW - 핵심)
    parser_check = subparsers.add_parser("check", help="문서 검사 (Self-Healing)")
    parser_check.set_defaults(func=cmd_check)
    
    # risk (NEW)
    parser_risk = subparsers.add_parser("risk", help="위험도 점수 확인")
    parser_risk.set_defaults(func=cmd_risk)
    
    # suggest (NEW)
    parser_suggest = subparsers.add_parser("suggest", help="자동 수정 추천 보기")
    parser_suggest.set_defaults(func=cmd_suggest)
    
    # report (NEW)
    parser_report = subparsers.add_parser("report", help="현재 이슈 리포트")
    parser_report.set_defaults(func=cmd_report)
    
    # validate (기존 - check로 리다이렉트)
    parser_validate = subparsers.add_parser("validate", help="검증 (check로 리다이렉트)")
    parser_validate.set_defaults(func=cmd_validate)
    
    # link
    parser_link = subparsers.add_parser("link", help="양방향 링크 동기화")
    parser_link.set_defaults(func=cmd_link)
    
    # create
    parser_create = subparsers.add_parser("create", help="새 Holon 생성")
    parser_create.add_argument("type", choices=["strategy", "structure", "feature", "meeting", "decision", "task"])
    parser_create.add_argument("title", help="문서 제목")
    parser_create.add_argument("--parent", "-p", help="상위 holon_id")
    parser_create.add_argument("--module", "-m", default="M00_Astral", help="모듈")
    parser_create.set_defaults(func=cmd_create)
    
    # spawn
    parser_spawn = subparsers.add_parser("spawn", help="Meeting에서 Decision/Task 생성")
    parser_spawn.add_argument("meeting_id", help="Meeting holon_id")
    parser_spawn.set_defaults(func=cmd_spawn)
    
    # meeting (회의록 자동 파싱)
    parser_meeting = subparsers.add_parser("meeting", help="회의록 자동 파싱 & Holon 생성")
    parser_meeting.add_argument("--file", "-f", help="회의록 파일 경로 (.txt, .md)")
    parser_meeting.add_argument("--text", "-t", help="회의록 텍스트 직접 입력")
    parser_meeting.add_argument("--no-spawn", action="store_true", help="Decision/Task 자동 생성 안함")
    parser_meeting.set_defaults(func=cmd_meeting)
    
    # place (NEW - HTE 모듈 자동 배치)
    parser_place = subparsers.add_parser("place", help="문서 자동 배치 - HTE 모듈 폴더에 생성")
    parser_place.add_argument("--file", "-f", help="문서 파일 경로")
    parser_place.add_argument("--text", "-t", help="문서 내용 직접 입력")
    parser_place.add_argument("--type", choices=["meeting", "strategy", "feature", "task", "decision", "auto"], 
                             default="auto", help="문서 타입")
    parser_place.set_defaults(func=cmd_place)
    
    # chunk
    parser_chunk = subparsers.add_parser("chunk", help="W 기반 Active Chunk 관리")
    parser_chunk.add_argument("action", choices=["generate", "show"], nargs="?", default="show",
                             help="generate: 새로 생성, show: 현재 표시")
    parser_chunk.set_defaults(func=cmd_chunk)
    
    # meta
    parser_meta = subparsers.add_parser("meta", help="Meta-Research Engine")
    parser_meta.add_argument("action", choices=["analyze", "report"], nargs="?", default="analyze",
                            help="analyze: 분석, report: 리포트 생성")
    parser_meta.set_defaults(func=cmd_meta)
    
    # health
    parser_health = subparsers.add_parser("health", help="시스템 건강 점검")
    parser_health.add_argument("action", choices=["check", "report"], nargs="?", default="check",
                              help="check: 점검, report: 리포트 저장")
    parser_health.set_defaults(func=cmd_health)
    
    # status
    parser_status = subparsers.add_parser("status", help="시스템 상태")
    parser_status.set_defaults(func=cmd_status)
    
    # help
    parser_help = subparsers.add_parser("help", help="도움말")
    parser_help.set_defaults(func=cmd_help)
    
    args = parser.parse_args()
    
    if args.command is None:
        cmd_help(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
