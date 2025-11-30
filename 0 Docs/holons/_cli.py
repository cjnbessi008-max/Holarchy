#!/usr/bin/env python3
"""
Holarchy 통합 CLI
- 모든 자동화 도구를 하나의 인터페이스로 통합
"""

import argparse
import sys
from pathlib import Path

# 같은 폴더의 모듈 import
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def cmd_validate(args):
    """검증 실행"""
    from _validate import HolarchyValidator
    validator = HolarchyValidator(str(script_dir.parent))
    validator.run_all_validations()


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


def cmd_help(args):
    """도움말"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           🏛️ Holarchy CLI - 명령어 가이드                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 기본 명령어                                              ║
║  ──────────────────────────────────────────────────────────  ║
║  status              시스템 상태 확인                        ║
║  validate            전체 문서 검증                          ║
║  link                양방향 링크 자동 동기화                 ║
║                                                              ║
║  📄 문서 생성                                                ║
║  ──────────────────────────────────────────────────────────  ║
║  create <type> <title> [--parent ID] [--module M00]          ║
║    type: strategy, structure, feature, meeting,              ║
║          decision, task                                      ║
║                                                              ║
║  예시:                                                       ║
║    create feature "학생 진단 리포트" --parent hte-doc-002    ║
║    create meeting "MVP 기능 논의"                            ║
║                                                              ║
║  🚀 회의 자동화                                              ║
║  ──────────────────────────────────────────────────────────  ║
║  spawn <meeting_id>  회의에서 Decision/Task 자동 생성        ║
║                                                              ║
║  예시:                                                       ║
║    spawn meeting-2025-001                                    ║
║                                                              ║
║  🧠 Working Memory (Chunk 시스템)                            ║
║  ──────────────────────────────────────────────────────────  ║
║  chunk generate    W 기반 중요도로 Active Chunk 생성         ║
║  chunk show        현재 Active Chunk 표시                    ║
║                                                              ║
║  * Chunk는 W(의지)와의 공명도로 중요도 판단                  ║
║  * 항상 Top-7만 유지 (인간 작업기억 모방)                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    parser = argparse.ArgumentParser(
        description="Holarchy 통합 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="명령어")
    
    # validate
    parser_validate = subparsers.add_parser("validate", help="전체 문서 검증")
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
    
    # chunk
    parser_chunk = subparsers.add_parser("chunk", help="W 기반 Active Chunk 관리")
    parser_chunk.add_argument("action", choices=["generate", "show"], nargs="?", default="show",
                             help="generate: 새로 생성, show: 현재 표시")
    parser_chunk.set_defaults(func=cmd_chunk)
    
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
