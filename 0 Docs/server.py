#!/usr/bin/env python3
"""
🔥 Holarchy Dashboard Server
브라우저에서 실제 파일 생성을 가능하게 하는 로컬 서버
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path

# holons 폴더의 모듈 import
sys.path.insert(0, str(Path(__file__).parent / "holons"))

app = Flask(__name__, static_folder='.')
CORS(app)  # 크로스 도메인 허용

# 경로 설정
BASE_PATH = Path(__file__).parent
HOLONS_PATH = BASE_PATH / "holons"


@app.route('/')
def index():
    """대시보드 페이지"""
    return send_from_directory('.', 'dashboard.html')


@app.route('/api/meeting', methods=['POST'])
def create_meeting():
    """회의록 파싱 & Holon 생성 API"""
    try:
        from _meeting_parser import MeetingParser
        
        data = request.json
        text = data.get('text', '')
        auto_spawn = data.get('auto_spawn', True)
        
        if not text.strip():
            return jsonify({"error": "회의록 내용이 비어있습니다"}), 400
        
        parser = MeetingParser(str(HOLONS_PATH))
        result = parser.parse_and_create(text, auto_spawn=auto_spawn)
        
        return jsonify({
            "success": True,
            "meeting_id": result["meeting_id"],
            "file": result["file"],
            "parent": result["parent"],
            "confidence": result["confidence"],
            "decisions": result["decisions"],
            "tasks": result["tasks"],
            "spawned": result["spawned"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/place', methods=['POST'])
def place_document():
    """문서 자동 배치 API - HTE 모듈 폴더에 생성"""
    try:
        from _document_placer import DocumentPlacer
        
        data = request.json
        text = data.get('text', '')
        doc_type = data.get('type', 'auto')
        
        if not text.strip():
            return jsonify({"error": "문서 내용이 비어있습니다"}), 400
        
        placer = DocumentPlacer()
        result = placer.create_document(text, doc_type=doc_type)
        
        return jsonify({
            "success": True,
            "holon_id": result["holon_id"],
            "module": result["module"],
            "filename": result["filename"],
            "filepath": result["filepath"],
            "confidence": result["confidence"],
            "matched_keywords": result["matched_keywords"],
            "title": result["title"],
            "decisions": result["decisions"],
            "tasks": result["tasks"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/check', methods=['POST'])
def run_check():
    """Self-Healing 검증 API"""
    try:
        from _validate import HolarchyValidator
        
        validator = HolarchyValidator(str(BASE_PATH))
        validator.run_all_validations()
        
        # reports에서 결과 읽기
        import json
        issues_path = BASE_PATH / "reports" / "issues.json"
        risk_path = BASE_PATH / "reports" / "risk_score.json"
        
        issues = {}
        risk = {}
        
        if issues_path.exists():
            issues = json.loads(issues_path.read_text(encoding="utf-8"))
        if risk_path.exists():
            risk = json.loads(risk_path.read_text(encoding="utf-8"))
        
        return jsonify({
            "success": True,
            "issues": issues,
            "risk": risk
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/link', methods=['POST'])
def run_link():
    """링크 동기화 API"""
    try:
        from _auto_link import AutoLinker
        
        linker = AutoLinker(str(HOLONS_PATH))
        linker.run()
        
        return jsonify({"success": True, "message": "링크 동기화 완료"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/documents', methods=['GET'])
def get_documents():
    """모든 문서 목록 API"""
    try:
        import json
        import re
        
        documents = {
            "holons": [],
            "meetings": [],
            "decisions": [],
            "tasks": []
        }
        
        # Holons 폴더
        for md_file in HOLONS_PATH.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
            content = md_file.read_text(encoding="utf-8")
            json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                try:
                    holon = json.loads(json_match.group(1))
                    documents["holons"].append({
                        "id": holon.get("holon_id"),
                        "title": holon.get("meta", {}).get("title", md_file.stem),
                        "type": holon.get("type"),
                        "status": holon.get("meta", {}).get("status"),
                        "file": md_file.name
                    })
                except:
                    pass
        
        # Meetings 폴더
        meetings_path = BASE_PATH / "meetings"
        if meetings_path.exists():
            for md_file in meetings_path.glob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    try:
                        holon = json.loads(json_match.group(1))
                        documents["meetings"].append({
                            "id": holon.get("holon_id"),
                            "title": holon.get("meta", {}).get("title", md_file.stem),
                            "date": holon.get("meta", {}).get("created_at"),
                            "status": holon.get("meta", {}).get("status"),
                            "file": md_file.name
                        })
                    except:
                        pass
        
        # Decisions 폴더
        decisions_path = BASE_PATH / "decisions"
        if decisions_path.exists():
            for md_file in decisions_path.glob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    try:
                        holon = json.loads(json_match.group(1))
                        documents["decisions"].append({
                            "id": holon.get("holon_id"),
                            "title": holon.get("meta", {}).get("title", md_file.stem),
                            "status": holon.get("meta", {}).get("status"),
                            "parent": holon.get("links", {}).get("parent"),
                            "file": md_file.name
                        })
                    except:
                        pass
        
        # Tasks 폴더
        tasks_path = BASE_PATH / "tasks"
        if tasks_path.exists():
            for md_file in tasks_path.glob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    try:
                        holon = json.loads(json_match.group(1))
                        documents["tasks"].append({
                            "id": holon.get("holon_id"),
                            "title": holon.get("meta", {}).get("title", md_file.stem),
                            "status": holon.get("meta", {}).get("status"),
                            "parent": holon.get("links", {}).get("parent"),
                            "file": md_file.name
                        })
                    except:
                        pass
        
        return jsonify({
            "success": True,
            "documents": documents,
            "counts": {
                "holons": len(documents["holons"]),
                "meetings": len(documents["meetings"]),
                "decisions": len(documents["decisions"]),
                "tasks": len(documents["tasks"]),
                "total": sum(len(v) for v in documents.values())
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """시스템 통계 API"""
    try:
        import json
        
        # Risk score 읽기
        risk_path = BASE_PATH / "reports" / "risk_score.json"
        risk = {"overall_score": 0}
        if risk_path.exists():
            risk = json.loads(risk_path.read_text(encoding="utf-8"))
        
        # 문서 수 계산
        holons_count = len(list(HOLONS_PATH.glob("*.md"))) - len(list(HOLONS_PATH.glob("_*.md")))
        meetings_count = len(list((BASE_PATH / "meetings").glob("*.md"))) if (BASE_PATH / "meetings").exists() else 0
        decisions_count = len(list((BASE_PATH / "decisions").glob("*.md"))) if (BASE_PATH / "decisions").exists() else 0
        tasks_count = len(list((BASE_PATH / "tasks").glob("*.md"))) if (BASE_PATH / "tasks").exists() else 0
        
        return jsonify({
            "success": True,
            "stats": {
                "holons": holons_count,
                "meetings": meetings_count,
                "decisions": decisions_count,
                "tasks": tasks_count,
                "total": holons_count + meetings_count + decisions_count + tasks_count,
                "health": risk.get("overall_score", 0)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Holarchy Dashboard Server")
    print("=" * 60)
    print()
    print("📌 대시보드 URL: http://localhost:5000")
    print()
    print("💡 종료하려면 Ctrl+C")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

