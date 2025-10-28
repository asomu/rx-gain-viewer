# Simple Linear Flow - 가장 심플한 워크플로우

**용도**: 간단한 보고서, 빠른 설명
**대상**: 모든 사람

---

## 다이어그램

```mermaid
graph LR
    A[📡 Network Analyzer<br/>SnP Files] --> B[🔄 RF Converter<br/>SnP → CSV]
    B --> C[📊 Django Web Service<br/>Interactive Charts]

    style A fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style B fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style C fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

---

## 설명

가장 간단한 3단계 플로우:

1. **📡 Network Analyzer** - S-parameter 측정 → SnP 파일 생성
2. **🔄 RF Converter** - SnP 파일 → CSV 변환 (주파수 필터링)
3. **📊 Django Web Service** - CSV 데이터 → 인터랙티브 차트

---

## 특징

- ✅ 3박스로 끝
- ✅ 5초만에 이해 가능
- ✅ PPT 1장에 딱 맞음
- ✅ 비기술직도 쉽게 이해

---

**파일명**: `01-simple-linear-flow.md`
**생성일**: 2025-10-27
