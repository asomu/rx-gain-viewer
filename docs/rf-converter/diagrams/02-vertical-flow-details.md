# Vertical Flow with Details - 세부 정보 포함

**용도**: 상세 보고서, 프로세스 문서
**대상**: 기술팀, 프로젝트 매니저

---

## 다이어그램

```mermaid
graph TD
    A[📡 Network Analyzer] -->|S-parameter<br/>Measurement| B[SnP Files<br/>.s1p ~ .s12p]
    B -->|Upload| C[🔄 RF Converter]
    C -->|Frequency<br/>Filtering| D[CSV File<br/>Rx Gain Data]
    D -->|Import| E[📊 Django Web<br/>Service]
    E -->|Plotly.js| F[Interactive<br/>Charts]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style C fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style D fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    style E fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style F fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
```

---

## 설명

세부 단계별 처리 과정:

1. **📡 Network Analyzer** - S-parameter 측정
2. **SnP Files** - .s1p ~ .s12p 형식 파일 생성
3. **🔄 RF Converter** - 파일 업로드 및 파싱
4. **CSV File** - Frequency Filtering 후 Rx Gain 데이터 추출
5. **📊 Django Web Service** - 데이터 Import
6. **Interactive Charts** - Plotly.js로 인터랙티브 차트 생성

---

## 특징

- ✅ 파일 형식 명시
- ✅ 각 단계별 처리 내용 표시
- ✅ 데이터 변환 과정 추적 가능
- ✅ 기술 문서에 적합

---

**파일명**: `02-vertical-flow-details.md`
**생성일**: 2025-10-27
